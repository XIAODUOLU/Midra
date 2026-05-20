from __future__ import annotations

import random

from music_agent.core.music_theory import NOTE_TO_SEMITONE


def _root_pitch(chord: str) -> int:
    root = chord[:-1] if chord.endswith("m") else chord
    # C1 = 24
    return 24 + NOTE_TO_SEMITONE[root]


def generate_bass(song_plan: dict, track: dict) -> list[dict]:
    total_bars = song_plan["song_plan"]["total_bars"]
    prog = song_plan["song_plan"]["chord_progression"]

    motif_len = 8
    motif = [random.choice([0, 1, 2, 3, 4, 5, 6]) for _ in range(motif_len)]
    motif[0] = 0
    motif[-1] = random.choice([0, 2, 4])

    events: list[dict] = []
    for bar in range(total_bars):
        chord = prog[bar % len(prog)]["chord"]
        root = _root_pitch(chord)
        base = bar * 4.0
        beat_positions = [0.0, 1.0, 2.0, 3.0]
        for idx, beat in enumerate(beat_positions):
            m = motif[(bar * 2 + idx) % motif_len]
            octave = 0 if m in (0, 1, 2) else 12
            if m in (5, 6):
                octave = 24
            pitch = root + octave
            events.append(
                {
                    "type": "note",
                    "pitch": pitch,
                    "start_beat": base + beat,
                    "duration_beat": random.choice([0.5, 0.75, 1.0]),
                    "velocity": random.randint(82, 104),
                }
            )
    return events
