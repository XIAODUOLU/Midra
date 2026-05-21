from __future__ import annotations

from music_agent.core.schema import MidiIR


CORE_TRACKS = {"drums", "bass", "chords", "lead"}


def validate_midi_ir(
    midi_ir: MidiIR,
    selected_tracks: list[str] | None = None,
    out_of_bounds_mode: str = "drop",
    enforce_core_tracks: bool = True,
) -> dict:
    errors: list[str] = []
    warnings: list[dict] = []
    if out_of_bounds_mode not in {"drop", "ignore"}:
        errors.append(f"Invalid out_of_bounds_mode: {out_of_bounds_mode}")
        out_of_bounds_mode = "drop"
    tracks = [t for t in midi_ir.tracks if t.enabled]
    track_map = {t.id: t for t in tracks}

    bpm = midi_ir.meta.get("bpm", 0)
    if not (40 <= bpm <= 220):
        errors.append("BPM is out of range 40-220")

    ts = midi_ir.meta.get("time_signature", {})
    if ts.get("numerator", 0) <= 0 or ts.get("denominator", 0) <= 0:
        errors.append("Invalid time signature")

    if selected_tracks is None and enforce_core_tracks:
        for c in CORE_TRACKS:
            if c not in track_map:
                errors.append(f"Missing core track: {c}")
            elif len(track_map[c].events) == 0:
                errors.append(f"Core track is empty: {c}")
    else:
        if not selected_tracks is None:
            for tid in selected_tracks:
                if tid not in track_map:
                    errors.append(f"Selected track does not exist or is disabled: {tid}")

    total_beats = float(midi_ir.meta.get("total_beats", 0))
    dropped_out_of_bounds_events = 0
    for t in tracks:
        if t.channel == 9 and t.id != "drums":
            errors.append(f"Non-drum track uses channel 9: {t.id}")
        if t.id == "drums" and t.channel != 9:
            errors.append("Drum track is not on channel 9")
        if t.enabled and len(t.events) == 0:
            errors.append(f"Enabled track is empty: {t.id}")
        kept_events = []
        for e in t.events:
            if not (0 <= e.pitch <= 127):
                errors.append(f"Pitch out of range: {t.id}")
            if not (1 <= e.velocity <= 127):
                errors.append(f"Velocity out of range: {t.id}")
            if e.duration_beat <= 0:
                errors.append(f"Invalid duration: {t.id}")
            if e.start_beat < 0:
                errors.append(f"Invalid start_beat: {t.id}")
            if e.start_beat + e.duration_beat > total_beats + 1e-6:
                if out_of_bounds_mode == "drop":
                    dropped_out_of_bounds_events += 1
                    continue
            kept_events.append(e)
        if len(kept_events) != len(t.events):
            t.events = kept_events

    if dropped_out_of_bounds_events > 0:
        warnings.append(
            {
                "code": "dropped_out_of_bounds_events",
                "message": f"Dropped {dropped_out_of_bounds_events} event(s) that exceeded total_beats={total_beats}",
                "count": dropped_out_of_bounds_events,
            }
        )

    return {
        "passed": len(errors) == 0,
        "score": 1.0 if len(errors) == 0 else 0.0,
        "checks": {
            "valid_bpm": 40 <= bpm <= 220,
            "valid_time_signature": ts.get("numerator", 0) > 0 and ts.get("denominator", 0) > 0,
            "no_empty_tracks": all((not t.enabled) or len(t.events) > 0 for t in tracks),
            "valid_channels": all(0 <= t.channel <= 15 for t in tracks),
        },
        "warnings": warnings,
        "errors": errors,
    }
