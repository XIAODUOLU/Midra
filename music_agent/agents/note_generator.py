from __future__ import annotations

import json
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from music_agent.agents.llm_client import llm_json
from music_agent.prompts import build_track_note_generator_prompt
from music_agent.generators.bass_generator import generate_bass
from music_agent.generators.chord_generator import generate_chords
from music_agent.generators.drum_generator import generate_drums
from music_agent.generators.lead_generator import generate_lead


def _generate_generic(song_plan: dict, track: dict) -> list[dict]:
    total_bars = song_plan["song_plan"]["total_bars"]
    channel = track["midi"]["channel"]
    base_pitch = 60 + min(channel, 12)
    events: list[dict] = []
    for bar in range(total_bars):
        start = bar * 4.0
        events.append(
            {
                "type": "note",
                "pitch": base_pitch,
                "start_beat": start,
                "duration_beat": 1.0,
                "velocity": 72,
            }
        )
        events.append(
            {
                "type": "note",
                "pitch": base_pitch + 7,
                "start_beat": start + 2.0,
                "duration_beat": 1.0,
                "velocity": 68,
            }
        )
    return events


def _generate_track_llm(song_plan: dict, arrangement_track: dict) -> list[dict]:
    plan = song_plan["song_plan"]
    prompt = build_track_note_generator_prompt(plan, arrangement_track)
    data = llm_json(prompt)
    events = data.get("events")
    if not isinstance(events, list):
        raise ValueError("Invalid LLM track output: missing events list")
    return events


def generate_notes(
    song_plan: dict,
    arrangement: dict,
    note_generation_mode: str = "llm",
    checkpoint_path: str | None = None,
) -> dict:
    enabled_tracks = [
        (track_id, track)
        for track_id, track in arrangement["arrangement"]["tracks"].items()
        if track.get("enabled", True)
    ]

    def _track_checkpoint_path(track_id: str) -> Path | None:
        if not checkpoint_path:
            return None
        path = Path(checkpoint_path)
        return path.with_name(f"{path.stem}.{track_id}{path.suffix}")

    def _save_track_checkpoint(track_event: dict) -> None:
        path = _track_checkpoint_path(track_event["track_id"])
        if path is None:
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(track_event, ensure_ascii=False, indent=2), encoding="utf-8")

    def _generate_one_track(track_id: str, track: dict) -> dict:
        t0 = time.perf_counter()
        print(f"[Track] note_generation start: {track_id} (mode={note_generation_mode})")

        if note_generation_mode == "llm":
            events = _generate_track_llm(song_plan, track)
        elif track_id == "drums":
            events = generate_drums(song_plan, track)
        elif track_id == "bass":
            events = generate_bass(song_plan, track)
        elif track_id == "chords":
            events = generate_chords(song_plan, track)
        elif track_id == "lead":
            events = generate_lead(song_plan, track)
        else:
            events = _generate_generic(song_plan, track)

        # Small per-track event perturbation to avoid fully static replay for rule-generated tracks.
        if note_generation_mode != "llm" and track_id in {"drums", "bass", "chords"}:
            for e in events:
                if e.get("type") == "note":
                    e["velocity"] = max(1, min(127, int(e.get("velocity", 90) + random.randint(-4, 4))))

        track_event = {"track_id": track_id, "events": events}
        _save_track_checkpoint(track_event)
        t1 = time.perf_counter()
        print(f"[Track] note_generation done: {track_id} in {t1 - t0:.3f}s, events={len(events)}")
        return track_event

    results_by_track: dict[str, dict] = {}
    max_workers = max(1, min(len(enabled_tracks), 8))
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_track_id = {
            executor.submit(_generate_one_track, track_id, track): track_id
            for track_id, track in enabled_tracks
        }
        for future in as_completed(future_to_track_id):
            track_id = future_to_track_id[future]
            results_by_track[track_id] = future.result()

    out = [results_by_track[track_id] for track_id, _ in enabled_tracks]
    if checkpoint_path:
        path = Path(checkpoint_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"track_events": out}, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"track_events": out}
