from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from .config import load_config
from .models import CreateTaskRequest
from .runner import GlobalRuntime, run_task_async
from .store import TaskStore

config = load_config()
store = TaskStore(config.data_dir)
runtime = GlobalRuntime()

app = FastAPI(title="Midra Backend", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _client_id(x_midra_client_id: str | None, client_id: str | None = None) -> str:
    resolved = x_midra_client_id or client_id
    if not resolved:
        raise HTTPException(status_code=400, detail="Missing X-Midra-Client-Id")
    return resolved


@app.get("/api/health")
def health() -> dict:
    return {"ok": True}


@app.get("/api/runtime")
def get_runtime() -> dict:
    day, count = store.today_quota()
    snap = runtime.snapshot()
    snap.update(
        {
            "quota": {
                "day": day,
                "count": count,
                "limit": config.daily_task_limit,
                "remaining": max(0, config.daily_task_limit - count),
            }
        }
    )
    return snap


@app.get("/api/tasks")
def list_tasks(x_midra_client_id: str | None = Header(default=None)) -> dict:
    owner_id = _client_id(x_midra_client_id)
    return {"tasks": store.list_tasks_by_owner(owner_id)}


@app.get("/api/tasks/{task_id}")
def get_task(task_id: str, x_midra_client_id: str | None = Header(default=None)) -> dict:
    owner_id = _client_id(x_midra_client_id)
    task = store.get_task(task_id)
    if task is None or task.get("owner_id") != owner_id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/api/tasks")
def create_task(req: CreateTaskRequest, x_midra_client_id: str | None = Header(default=None)) -> dict:
    owner_id = _client_id(x_midra_client_id)
    if store.has_running_task_for_owner(owner_id):
        raise HTTPException(status_code=409, detail="You already have a running task")

    day, count = store.today_quota()
    if count >= config.daily_task_limit:
        raise HTTPException(status_code=429, detail=f"Daily task limit reached for {day}")

    if config.global_single_active_task and runtime.busy():
        raise HTTPException(status_code=409, detail={"message": "Another user task is running", **runtime.snapshot()})

    task = store.create_task(owner_id=owner_id, prompt=req.prompt)
    store.inc_today_quota()
    if not runtime.acquire(task["id"], owner_id):
        raise HTTPException(status_code=409, detail={"message": "Another user task is running", **runtime.snapshot()})
    run_task_async(store=store, config=config, runtime=runtime, task_id=task["id"], owner_id=owner_id, retry=False)
    return task


@app.post("/api/tasks/{task_id}/retry")
def retry_task(task_id: str, x_midra_client_id: str | None = Header(default=None)) -> dict:
    owner_id = _client_id(x_midra_client_id)
    task = store.get_task(task_id)
    if task is None or task.get("owner_id") != owner_id:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.get("status") != "failed":
        raise HTTPException(status_code=400, detail="Only failed tasks can be retried")
    if config.global_single_active_task and runtime.busy():
        raise HTTPException(status_code=409, detail={"message": "Another user task is running", **runtime.snapshot()})

    if not runtime.acquire(task_id, owner_id):
        raise HTTPException(status_code=409, detail={"message": "Another user task is running", **runtime.snapshot()})
    run_task_async(store=store, config=config, runtime=runtime, task_id=task_id, owner_id=owner_id, retry=True)
    return {"ok": True, "task_id": task_id}


def _artifact_path(task: dict, key: str) -> Path:
    p = task.get("artifacts", {}).get(key)
    if not p:
        raise HTTPException(status_code=404, detail="Artifact not ready")
    path = Path(p)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Artifact file missing")
    return path


@app.get("/api/tasks/{task_id}/download/mid")
def dl_mid(
    task_id: str,
    x_midra_client_id: str | None = Header(default=None),
    client_id: str | None = Query(default=None),
) -> FileResponse:
    owner_id = _client_id(x_midra_client_id, client_id)
    task = store.get_task(task_id)
    if task is None or task.get("owner_id") != owner_id:
        raise HTTPException(status_code=404, detail="Task not found")
    return FileResponse(_artifact_path(task, "mid"), media_type="audio/midi", filename=f"{task_id}.mid")


@app.get("/api/tasks/{task_id}/download/wav")
def dl_wav(
    task_id: str,
    x_midra_client_id: str | None = Header(default=None),
    client_id: str | None = Query(default=None),
) -> FileResponse:
    owner_id = _client_id(x_midra_client_id, client_id)
    task = store.get_task(task_id)
    if task is None or task.get("owner_id") != owner_id:
        raise HTTPException(status_code=404, detail="Task not found")
    return FileResponse(_artifact_path(task, "wav"), media_type="audio/wav", filename=f"{task_id}.wav")


@app.get("/api/tasks/{task_id}/download/mp3")
def dl_mp3(
    task_id: str,
    x_midra_client_id: str | None = Header(default=None),
    client_id: str | None = Query(default=None),
) -> FileResponse:
    owner_id = _client_id(x_midra_client_id, client_id)
    task = store.get_task(task_id)
    if task is None or task.get("owner_id") != owner_id:
        raise HTTPException(status_code=404, detail="Task not found")
    return FileResponse(_artifact_path(task, "mp3"), media_type="audio/mpeg", filename=f"{task_id}.mp3")
