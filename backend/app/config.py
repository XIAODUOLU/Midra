from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class AppConfig:
    host: str
    port: int
    cors_origins: list[str]
    data_dir: Path
    outputs_dir: Path
    stage_retry_count: int
    daily_task_limit: int
    max_music_duration_seconds: int
    global_single_active_task: bool
    project_name_prefix: str
    soundfont_path: str
    mp3_bitrate: str
    note_mode: str
    out_of_bounds_mode: str
    openai_api_key: str
    openai_base_url: str
    openai_model: str


def load_config(path: str = "backend/config.yaml") -> AppConfig:
    payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    app = payload["app"]
    runtime = payload["runtime"]
    music_defaults = payload["music_defaults"]
    llm = payload["llm"]
    return AppConfig(
        host=str(app.get("host", "0.0.0.0")),
        port=int(app.get("port", 8000)),
        cors_origins=list(app.get("cors_origins", ["*"])),
        data_dir=Path(runtime.get("data_dir", "backend/data")),
        outputs_dir=Path(runtime.get("outputs_dir", "outputs/projects")),
        stage_retry_count=int(runtime.get("stage_retry_count", 3)),
        daily_task_limit=int(runtime.get("daily_task_limit", 100)),
        max_music_duration_seconds=int(runtime.get("max_music_duration_seconds", 120)),
        global_single_active_task=bool(runtime.get("global_single_active_task", True)),
        project_name_prefix=str(music_defaults.get("project_name_prefix", "web")),
        soundfont_path=str(music_defaults.get("soundfont_path", "/usr/share/sounds/sf2/FluidR3_GM.sf2")),
        mp3_bitrate=str(music_defaults.get("mp3_bitrate", "192k")),
        note_mode=str(music_defaults.get("note_mode", "llm")),
        out_of_bounds_mode=str(music_defaults.get("out_of_bounds_mode", "drop")),
        openai_api_key=str(os.getenv("OPENAI_API_KEY", llm.get("openai_api_key", ""))),
        openai_base_url=str(os.getenv("OPENAI_BASE_URL", llm.get("openai_base_url", "https://api.openai.com/v1"))),
        openai_model=str(os.getenv("OPENAI_MODEL", llm.get("openai_model", "gpt-5.5"))),
    )

