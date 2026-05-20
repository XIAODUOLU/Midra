from __future__ import annotations

import argparse
import json
import time
import traceback
import uuid
from pathlib import Path

from music_agent.agents.arrangement_planner import plan_arrangement
from music_agent.agents.intent_parser import parse_intent
from music_agent.agents.note_generator import generate_notes
from music_agent.agents.song_planner import plan_song
from music_agent.core.midi_ir import assemble_midi_ir
from music_agent.core.mido_renderer import render_midi
from music_agent.core.schema import to_dict
from music_agent.core.validator import validate_midi_ir
from music_agent.utils.audio import midi_to_wav, wav_to_mp3


def _project_dir(project_id: str, project_name: str) -> Path:
    safe_name = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in project_name).strip("_")
    if not safe_name:
        safe_name = "untitled"
    return Path("outputs") / "projects" / f"{safe_name}_{project_id}"


def _save_stage(stage_path: Path, payload: dict) -> None:
    stage_path.parent.mkdir(parents=True, exist_ok=True)
    stage_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _load_stage(stage_path: Path) -> dict:
    if not stage_path.exists():
        raise FileNotFoundError(f"Missing checkpoint file: {stage_path}")
    return json.loads(stage_path.read_text(encoding="utf-8"))


def generate_music(
    user_prompt: str,
    output_path: str | None = None,
    selected_tracks: list[str] | None = None,
    project_name: str = "default_project",
    project_id: str | None = None,
    resume: bool = False,
    soundfont_path: str = "/usr/share/sounds/sf2/FluidR3_GM.sf2",
    mp3_bitrate: str = "192k",
    note_generation_mode: str = "llm",
    out_of_bounds_mode: str = "drop",
) -> dict:
    pid = project_id or uuid.uuid4().hex[:8]
    pdir = _project_dir(pid, project_name)

    intent_path = pdir / "01_intent.json"
    song_plan_path = pdir / "02_song_plan.json"
    arrangement_path = pdir / "03_arrangement.json"
    track_events_path = pdir / "04_track_events.json"
    midi_ir_path = pdir / "05_midi_ir.json"
    wav_stage_path = pdir / "06_wav.json"
    mp3_stage_path = pdir / "07_mp3.json"
    pipeline_path = pdir / "pipeline_result.json"
    if output_path is None:
        output_path = str(pdir / "generated.mid")

    t0 = time.perf_counter()
    print("[Stage] intent: start")
    if resume and intent_path.exists():
        intent = _load_stage(intent_path)
    else:
        intent = parse_intent(user_prompt)
        _save_stage(intent_path, intent)
    t1 = time.perf_counter()
    print(f"[Stage] intent: done in {t1 - t0:.3f}s")

    t0 = time.perf_counter()
    print("[Stage] song_plan: start")
    if resume and song_plan_path.exists():
        song_plan = _load_stage(song_plan_path)
    else:
        song_plan = plan_song(intent)
        _save_stage(song_plan_path, song_plan)
    t1 = time.perf_counter()
    print(f"[Stage] song_plan: done in {t1 - t0:.3f}s")

    t0 = time.perf_counter()
    print("[Stage] arrangement: start")
    if resume and arrangement_path.exists():
        arrangement = _load_stage(arrangement_path)
    else:
        arrangement = plan_arrangement(intent, song_plan)
        _save_stage(arrangement_path, arrangement)
    t1 = time.perf_counter()
    print(f"[Stage] arrangement: done in {t1 - t0:.3f}s")

    t0 = time.perf_counter()
    print("[Stage] track_events: start")
    if resume and track_events_path.exists():
        track_events = _load_stage(track_events_path)
    else:
        track_events = generate_notes(
            song_plan,
            arrangement,
            note_generation_mode=note_generation_mode,
            checkpoint_path=str(track_events_path),
        )
        _save_stage(track_events_path, track_events)
    t1 = time.perf_counter()
    print(f"[Stage] track_events: done in {t1 - t0:.3f}s")

    t0 = time.perf_counter()
    print("[Stage] midi_ir: start")
    if resume and midi_ir_path.exists():
        midi_ir_dict = _load_stage(midi_ir_path)
        from music_agent.core.schema import MidiIR, NoteEvent, TrackIR

        tracks = []
        for t in midi_ir_dict["tracks"]:
            tracks.append(
                TrackIR(
                    id=t["id"],
                    name=t["name"],
                    role=t["role"],
                    channel=t["channel"],
                    program=t.get("program"),
                    volume=t.get("volume", 100),
                    pan=t.get("pan", 64),
                    enabled=t.get("enabled", True),
                    is_core_track=t.get("is_core_track", False),
                    events=[NoteEvent(**e) for e in t.get("events", [])],
                )
            )
        midi_ir = MidiIR(meta=midi_ir_dict["meta"], tracks=tracks)
    else:
        midi_ir = assemble_midi_ir(song_plan, arrangement, track_events["track_events"])
        _save_stage(midi_ir_path, to_dict(midi_ir))
    t1 = time.perf_counter()
    print(f"[Stage] midi_ir: done in {t1 - t0:.3f}s")

    t0 = time.perf_counter()
    print("[Stage] validation: start")
    validation = validate_midi_ir(
        midi_ir,
        selected_tracks=selected_tracks,
        out_of_bounds_mode=out_of_bounds_mode,
    )
    if not validation["passed"]:
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "; ".join(validation["errors"]),
                "module": "validator",
            },
            "validation": validation,
        }
    t1 = time.perf_counter()
    print(f"[Stage] validation: done in {t1 - t0:.3f}s")

    t0 = time.perf_counter()
    print("[Stage] midi_render: start")
    render_result = render_midi(midi_ir, output_path=output_path, selected_tracks=selected_tracks)
    t1 = time.perf_counter()
    print(f"[Stage] midi_render: done in {t1 - t0:.3f}s")

    wav_path = str(Path(render_result["output_path"]).with_suffix(".wav"))
    mp3_path = str(Path(render_result["output_path"]).with_suffix(".mp3"))

    t0 = time.perf_counter()
    print("[Stage] wav_render: start")
    if resume and wav_stage_path.exists():
        wav_result = _load_stage(wav_stage_path)
    else:
        wav_output = midi_to_wav(render_result["output_path"], wav_path, soundfont_path=soundfont_path)
        wav_result = {
            "success": True,
            "input_midi": render_result["output_path"],
            "output_wav": wav_output,
            "soundfont_path": soundfont_path,
            "sample_rate": 44100,
        }
        _save_stage(wav_stage_path, wav_result)
    t1 = time.perf_counter()
    print(f"[Stage] wav_render: done in {t1 - t0:.3f}s")

    t0 = time.perf_counter()
    print("[Stage] mp3_render: start")
    if resume and mp3_stage_path.exists():
        mp3_result = _load_stage(mp3_stage_path)
    else:
        mp3_output = wav_to_mp3(wav_result["output_wav"], mp3_path=mp3_path, bitrate=mp3_bitrate, overwrite=True)
        mp3_result = {
            "success": True,
            "input_wav": wav_result["output_wav"],
            "output_mp3": mp3_output,
            "bitrate": mp3_bitrate,
        }
        _save_stage(mp3_stage_path, mp3_result)
    t1 = time.perf_counter()
    print(f"[Stage] mp3_render: done in {t1 - t0:.3f}s")

    final_output = {
        "success": True,
        "midi_file": render_result["output_path"],
        "wav_file": wav_result["output_wav"],
        "mp3_file": mp3_result["output_mp3"],
        "metadata": {
            "title": midi_ir.meta["title"],
            "bpm": midi_ir.meta["bpm"],
            "key": midi_ir.meta["key_signature"],
            "time_signature": f"{midi_ir.meta['time_signature']['numerator']}/{midi_ir.meta['time_signature']['denominator']}",
            "duration_seconds": render_result["duration_seconds"],
            "total_bars": midi_ir.meta["total_bars"],
            "loopable": midi_ir.meta["loopable"],
        },
        "tracks": [
            {"id": t.id, "name": t.name, "role": t.role, "description": "generated"}
            for t in midi_ir.tracks
            if t.enabled and (selected_tracks is None or t.id in selected_tracks)
        ],
        "validation": {"passed": validation["passed"], "score": validation["score"]},
        "default_render_result": {
            "output_path": render_result["output_path"],
            "selected_tracks": selected_tracks,
        },
    }

    result = {
        "project": {
            "project_name": project_name,
            "project_id": pid,
            "project_dir": str(pdir),
            "resume": resume,
        },
        "intent": intent,
        "song_plan": song_plan,
        "arrangement": arrangement,
        "track_events": track_events,
        "midi_ir": to_dict(midi_ir),
        "render_result": render_result,
        "wav_result": wav_result,
        "mp3_result": mp3_result,
        "validation": validation,
        "final_output": final_output,
    }
    _save_stage(pipeline_path, result)
    return result


def export_tracks(midi_ir: dict, selected_tracks: list[str], output_path: str) -> dict:
    from music_agent.core.schema import MidiIR, NoteEvent, TrackIR

    tracks = []
    for t in midi_ir["tracks"]:
        events = [NoteEvent(**e) for e in t.get("events", [])]
        tracks.append(
            TrackIR(
                id=t["id"],
                name=t["name"],
                role=t.get("role", "unknown"),
                channel=t["channel"],
                program=t.get("program"),
                volume=t.get("volume", 100),
                pan=t.get("pan", 64),
                enabled=t.get("enabled", True),
                is_core_track=t.get("is_core_track", False),
                events=events,
            )
        )
    obj = MidiIR(meta=midi_ir["meta"], tracks=tracks)
    return render_midi(obj, output_path=output_path, selected_tracks=selected_tracks)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", type=str)
    parser.add_argument("--tracks", type=str, default=None)
    parser.add_argument("--output", type=str, default=None)
    parser.add_argument("--project-name", type=str, default="default_project")
    parser.add_argument("--project-id", type=str, default=None)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--soundfont", type=str, default="/usr/share/sounds/sf2/FluidR3_GM.sf2")
    parser.add_argument("--mp3-bitrate", type=str, default="192k")
    parser.add_argument("--note-mode", type=str, choices=["llm", "rule"], default="llm")
    parser.add_argument("--out-of-bounds-mode", type=str, choices=["drop", "ignore"], default="ignore")
    args = parser.parse_args()

    selected_tracks = None
    if args.tracks:
        selected_tracks = [x.strip() for x in args.tracks.split(",") if x.strip()]

    try:
        result = generate_music(
            args.prompt,
            output_path=args.output,
            selected_tracks=selected_tracks,
            project_name=args.project_name,
            project_id=args.project_id,
            resume=args.resume,
            soundfont_path=args.soundfont,
            mp3_bitrate=args.mp3_bitrate,
            note_generation_mode=args.note_mode,
            out_of_bounds_mode=args.out_of_bounds_mode,
        )
    except Exception as e:
        tb = traceback.format_exc()
        print(
            json.dumps(
                {
                    "success": False,
                    "error": {
                        "type": "llm_error",
                        "message": f"{str(e)}\n\n{tb}",
                        "module": "planner",
                    },
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return
    if result.get("success") is False:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    out_json = Path(result["project"]["project_dir"]) / "generated.json"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Generated MIDI: {result['render_result']['output_path']}")
    print(f"Generated WAV: {result['wav_result']['output_wav']}")
    print(f"Generated MP3: {result['mp3_result']['output_mp3']}")
    print(f"Generated JSON: {out_json}")
    print(f"Project checkpoint dir: {result['project']['project_dir']}")
    print(f"Validation: {'passed' if result['validation']['passed'] else 'failed'}")


if __name__ == "__main__":
    main()
