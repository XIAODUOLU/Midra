from __future__ import annotations

from pathlib import Path

from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo

from music_agent.core.schema import MidiIR


def beat_to_tick(beat: float, ticks_per_beat: int = 480) -> int:
    return int(round(beat * ticks_per_beat))


def _absolute_to_delta(events: list[dict]) -> list[Message]:
    events = sorted(events, key=lambda e: (e["tick"], e["kind"] == "off"))
    last_tick = 0
    out: list[Message] = []
    for e in events:
        delta = e["tick"] - last_tick
        out.append(e["msg"].copy(time=delta))
        last_tick = e["tick"]
    return out


def render_midi(midi_ir: MidiIR, output_path: str, selected_tracks: list[str] | None = None) -> dict:
    if selected_tracks is not None and len(selected_tracks) == 0:
        raise ValueError("selected_tracks cannot be empty")

    all_tracks = [t for t in midi_ir.tracks if t.enabled]
    if selected_tracks is None:
        tracks = all_tracks
    else:
        selected_set = set(selected_tracks)
        track_ids = {t.id for t in all_tracks}
        missing = selected_set - track_ids
        if missing:
            raise ValueError(f"selected_tracks contains unknown tracks: {sorted(missing)}")
        tracks = [t for t in all_tracks if t.id in selected_set]

    mid = MidiFile(ticks_per_beat=midi_ir.meta.get("ticks_per_beat", 480))
    meta_track = MidiTrack()
    mid.tracks.append(meta_track)
    bpm = midi_ir.meta["bpm"]
    tempo = bpm2tempo(bpm)
    ts = midi_ir.meta["time_signature"]
    meta_track.append(MetaMessage("set_tempo", tempo=tempo, time=0))
    meta_track.append(
        MetaMessage(
            "time_signature",
            numerator=ts["numerator"],
            denominator=ts["denominator"],
            clocks_per_click=24,
            notated_32nd_notes_per_beat=8,
            time=0,
        )
    )

    total_note_events = 0
    for tr in tracks:
        t = MidiTrack()
        mid.tracks.append(t)
        t.append(MetaMessage("track_name", name=tr.name, time=0))
        if tr.program is not None and tr.channel != 9:
            t.append(Message("program_change", channel=tr.channel, program=tr.program, time=0))
        t.append(Message("control_change", channel=tr.channel, control=7, value=tr.volume, time=0))
        t.append(Message("control_change", channel=tr.channel, control=10, value=tr.pan, time=0))

        abs_events = []
        for ev in tr.events:
            total_note_events += 1
            start_tick = beat_to_tick(ev.start_beat, mid.ticks_per_beat)
            dur_tick = beat_to_tick(ev.duration_beat, mid.ticks_per_beat)
            abs_events.append(
                {
                    "tick": start_tick,
                    "kind": "on",
                    "msg": Message("note_on", channel=tr.channel, note=ev.pitch, velocity=ev.velocity, time=0),
                }
            )
            abs_events.append(
                {
                    "tick": start_tick + max(dur_tick, 1),
                    "kind": "off",
                    "msg": Message("note_off", channel=tr.channel, note=ev.pitch, velocity=0, time=0),
                }
            )

        for msg in _absolute_to_delta(abs_events):
            t.append(msg)

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    mid.save(str(out))

    return {
        "success": True,
        "output_path": str(out),
        "selected_tracks": selected_tracks,
        "ticks_per_beat": mid.ticks_per_beat,
        "total_tracks": len(tracks),
        "total_note_events": total_note_events,
        "duration_seconds": midi_ir.meta["total_beats"] * (60.0 / bpm),
        "warnings": [],
    }
