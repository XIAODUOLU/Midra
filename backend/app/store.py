from __future__ import annotations

import json
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path


class TaskStore:
    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir
        self.tasks_dir = self.data_dir / "tasks"
        self.quota_dir = self.data_dir / "quota"
        self.index_path = self.data_dir / "task_index.json"
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self.quota_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        if not self.index_path.exists():
            self.index_path.write_text(json.dumps({"owners": {}}, ensure_ascii=False, indent=2), encoding="utf-8")

    def _task_dir(self, task_id: str) -> Path:
        return self.tasks_dir / task_id

    def _task_json(self, task_id: str) -> Path:
        return self._task_dir(task_id) / "task.json"

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _load_index(self) -> dict:
        if not self.index_path.exists():
            return {"owners": {}}
        try:
            data = json.loads(self.index_path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                return {"owners": {}}
            data.setdefault("owners", {})
            return data
        except Exception:
            return {"owners": {}}

    def _save_index(self, payload: dict) -> None:
        self.index_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def _upsert_index_entry(self, task: dict) -> None:
        idx = self._load_index()
        owners = idx.setdefault("owners", {})
        owner_id = str(task.get("owner_id", ""))
        if not owner_id:
            return
        entries = owners.setdefault(owner_id, [])
        simplified = {
            "id": task["id"],
            "created_at": task.get("created_at"),
            "updated_at": task.get("updated_at"),
            "status": task.get("status"),
        }
        replaced = False
        for i, entry in enumerate(entries):
            if entry.get("id") == task["id"]:
                entries[i] = simplified
                replaced = True
                break
        if not replaced:
            entries.append(simplified)
        entries.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        self._save_index(idx)

    def _rebuild_index(self) -> dict:
        owners: dict[str, list[dict]] = {}
        for p in self.tasks_dir.glob("*/task.json"):
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                continue
            owner_id = data.get("owner_id")
            task_id = data.get("id")
            if not owner_id or not task_id:
                continue
            owners.setdefault(owner_id, []).append(
                {
                    "id": task_id,
                    "created_at": data.get("created_at"),
                    "updated_at": data.get("updated_at"),
                    "status": data.get("status"),
                }
            )
        for owner_id in owners:
            owners[owner_id].sort(key=lambda x: x.get("created_at", ""), reverse=True)
        payload = {"owners": owners}
        self._save_index(payload)
        return payload

    def create_task(self, owner_id: str, prompt: str) -> dict:
        with self._lock:
            task_id = uuid.uuid4().hex
            tdir = self._task_dir(task_id)
            tdir.mkdir(parents=True, exist_ok=True)
            task = {
                "id": task_id,
                "owner_id": owner_id,
                "prompt": prompt,
                "status": "pending",
                "created_at": self._now(),
                "updated_at": self._now(),
                "stage_index": 0,
                "stage_total": 9,
                "stage_name": "pending",
                "track_total": 0,
                "track_completed": 0,
                "error": None,
                "project_id": None,
                "project_dir": None,
                "artifacts": {"mid": None, "wav": None, "mp3": None},
            }
            self._task_json(task_id).write_text(json.dumps(task, ensure_ascii=False, indent=2), encoding="utf-8")
            self._upsert_index_entry(task)
            return task

    def save_task(self, task: dict) -> None:
        with self._lock:
            task["updated_at"] = self._now()
            self._task_json(task["id"]).write_text(json.dumps(task, ensure_ascii=False, indent=2), encoding="utf-8")
            self._upsert_index_entry(task)

    def get_task(self, task_id: str) -> dict | None:
        path = self._task_json(task_id)
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def list_tasks_by_owner(self, owner_id: str) -> list[dict]:
        with self._lock:
            idx = self._load_index()
            entries = idx.get("owners", {}).get(owner_id)
            if entries is None:
                idx = self._rebuild_index()
                entries = idx.get("owners", {}).get(owner_id, [])

            out: list[dict] = []
            for entry in entries:
                task_id = entry.get("id")
                if not task_id:
                    continue
                task = self.get_task(task_id)
                if task is not None and task.get("owner_id") == owner_id:
                    out.append(task)
            out.sort(key=lambda x: x.get("created_at", ""), reverse=True)
            return out

    def has_running_task_for_owner(self, owner_id: str) -> bool:
        return any(t.get("status") == "running" for t in self.list_tasks_by_owner(owner_id))

    def today_quota(self) -> tuple[str, int]:
        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        path = self.quota_dir / f"{day}.json"
        if not path.exists():
            return day, 0
        data = json.loads(path.read_text(encoding="utf-8"))
        return day, int(data.get("count", 0))

    def inc_today_quota(self) -> int:
        with self._lock:
            day, count = self.today_quota()
            count += 1
            path = self.quota_dir / f"{day}.json"
            path.write_text(json.dumps({"day": day, "count": count}, ensure_ascii=False, indent=2), encoding="utf-8")
            return count
