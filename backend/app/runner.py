from __future__ import annotations

import os
import threading
import traceback
from pathlib import Path

from music_agent.main import generate_music

from .config import AppConfig
from .store import TaskStore


class GlobalRuntime:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.running_task_id: str | None = None
        self.running_owner_id: str | None = None
        self.stage_index: int = 0
        self.stage_total: int = 9
        self.stage_name: str = "idle"
        self.track_total: int = 0
        self.track_completed: int = 0

    def busy(self) -> bool:
        return self.running_task_id is not None

    def snapshot(self) -> dict:
        with self._lock:
            return {
                "busy": self.busy(),
                "task_id": self.running_task_id,
                "stage_index": self.stage_index,
                "stage_total": self.stage_total,
                "stage_name": self.stage_name,
                "track_total": self.track_total,
                "track_completed": self.track_completed,
            }

    def acquire(self, task_id: str, owner_id: str) -> bool:
        with self._lock:
            if self.running_task_id is not None:
                return False
            self.running_task_id = task_id
            self.running_owner_id = owner_id
            self.stage_index = 0
            self.stage_total = 9
            self.stage_name = "starting"
            self.track_total = 0
            self.track_completed = 0
            return True

    def release(self) -> None:
        with self._lock:
            self.running_task_id = None
            self.running_owner_id = None
            self.stage_index = 0
            self.stage_name = "idle"
            self.track_total = 0
            self.track_completed = 0

    def update(self, event: dict) -> None:
        with self._lock:
            if event.get("type") == "stage":
                self.stage_index = int(event.get("stage_index", self.stage_index))
                self.stage_total = int(event.get("stage_total", self.stage_total))
                self.stage_name = str(event.get("stage_name", self.stage_name))
            if event.get("type") == "track_progress":
                self.track_total = int(event.get("track_total", self.track_total))
                self.track_completed = int(event.get("track_completed", self.track_completed))


def run_task_async(
    *,
    store: TaskStore,
    config: AppConfig,
    runtime: GlobalRuntime,
    task_id: str,
    owner_id: str,
    retry: bool,
) -> threading.Thread:
    task = store.get_task(task_id)
    if task is None:
        raise ValueError("Task not found")

    def _target() -> None:
        local_task = store.get_task(task_id)
        if local_task is None:
            runtime.release()
            return
        local_task["status"] = "running"
        local_task["error"] = None
        store.save_task(local_task)

        os.environ["OPENAI_API_KEY"] = config.openai_api_key
        os.environ["OPENAI_BASE_URL"] = config.openai_base_url
        os.environ["OPENAI_MODEL"] = config.openai_model
        os.environ["MAX_MUSIC_DURATION_SECONDS"] = str(config.max_music_duration_seconds)

        project_id = local_task.get("project_id") or local_task["id"][:8]
        local_task["project_id"] = project_id

        def _progress(event: dict) -> None:
            runtime.update(event)
            t = store.get_task(task_id)
            if t is None:
                return
            if event.get("type") == "stage":
                t["stage_index"] = int(event.get("stage_index", t.get("stage_index", 0)))
                t["stage_total"] = int(event.get("stage_total", t.get("stage_total", 9)))
                t["stage_name"] = str(event.get("stage_name", t.get("stage_name", "running")))
            elif event.get("type") == "track_progress":
                t["track_total"] = int(event.get("track_total", t.get("track_total", 0)))
                t["track_completed"] = int(event.get("track_completed", t.get("track_completed", 0)))
            store.save_task(t)

        attempts = max(1, config.stage_retry_count)
        try:
            last_exc: Exception | None = None
            for _ in range(attempts):
                try:
                    result = generate_music(
                        local_task["prompt"],
                        project_name=f"{config.project_name_prefix}_{owner_id[:8]}",
                        project_id=project_id,
                        resume=retry,
                        soundfont_path=config.soundfont_path,
                        mp3_bitrate=config.mp3_bitrate,
                        note_generation_mode=config.note_mode,
                        out_of_bounds_mode=config.out_of_bounds_mode,
                        progress_callback=_progress,
                    )
                    if result.get("success") is False:
                        raise RuntimeError(result.get("error", {}).get("message", "generation failed"))
                    local_task["status"] = "succeeded"
                    local_task["project_dir"] = result["project"]["project_dir"]
                    local_task["artifacts"] = {
                        "mid": result["render_result"]["output_path"],
                        "wav": result["wav_result"]["output_wav"],
                        "mp3": result["mp3_result"]["output_mp3"],
                    }
                    store.save_task(local_task)
                    runtime.release()
                    return
                except Exception as exc:  # noqa: BLE001
                    last_exc = exc
            raise RuntimeError(str(last_exc) if last_exc else "generation failed")
        except Exception as exc:  # noqa: BLE001
            local_task["status"] = "failed"
            local_task["error"] = {
                "message": str(exc),
                "traceback": traceback.format_exc(),
            }
            store.save_task(local_task)
            runtime.release()

    th = threading.Thread(target=_target, daemon=True)
    th.start()
    return th

