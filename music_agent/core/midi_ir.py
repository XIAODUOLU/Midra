from __future__ import annotations

from music_agent.core.schema import MidiIR, NoteEvent, TrackIR


def assemble_midi_ir(song_plan: dict, arrangement: dict, track_events: list[dict]) -> MidiIR:
    arrangement_tracks = arrangement.get("tracks")
    if arrangement_tracks is None:
        arrangement_tracks = arrangement.get("arrangement", {}).get("tracks", {})

    event_map = {x["track_id"]: x.get("events", []) for x in track_events}
    tracks: list[TrackIR] = []
    for track_id, t in arrangement_tracks.items():
        if not t.get("enabled", True):
            continue
        events = [NoteEvent(**e) for e in event_map.get(track_id, [])]
        tracks.append(
            TrackIR(
                id=track_id,
                name=t["name"],
                role=t["role"],
                channel=t["midi"]["channel"],
                program=t["midi"].get("program"),
                volume=t["mix"].get("volume", 100),
                pan=t["mix"].get("pan", 64),
                enabled=t.get("enabled", True),
                is_core_track=t.get("is_core_track", False),
                events=events,
            )
        )

    bpm = song_plan["song_plan"]["bpm"]
    time_sig = song_plan["song_plan"]["time_signature"]
    total_bars = song_plan["song_plan"]["total_bars"]
    beats_per_bar = time_sig["numerator"]
    meta = {
        "title": song_plan["song_plan"]["title"],
        "bpm": bpm,
        "ticks_per_beat": 480,
        "time_signature": time_sig,
        "key_signature": f"{song_plan['song_plan']['key']['root']} {song_plan['song_plan']['key']['mode']}",
        "total_bars": total_bars,
        "beats_per_bar": beats_per_bar,
        "total_beats": total_bars * beats_per_bar,
        "loopable": song_plan["song_plan"].get("loopable", True),
    }
    return MidiIR(meta=meta, tracks=tracks)
