from __future__ import annotations

import random

from music_agent.core.drum_map import DRUM_MAP


def generate_drums(song_plan: dict, track: dict) -> list[dict]:
    total_bars = song_plan["song_plan"]["total_bars"]

    motif_len = 8
    hat_motif = [random.choice([0, 1]) for _ in range(motif_len)]
    hat_motif[0] = 1
    hat_motif[-1] = random.choice([0, 1])

    kick_candidates = [0.0, 0.75, 1.5, 2.0, 2.75, 3.5]
    kick_motif = [random.choice(kick_candidates) for _ in range(2)]

    events: list[dict] = []
    for bar in range(total_bars):
        base = bar * 4.0

        for beat in sorted(set([0.0, 2.0] + kick_motif)):
            events.append(
                {
                    "type": "note",
                    "pitch": DRUM_MAP["kick"],
                    "drum_name": "kick",
                    "start_beat": base + beat,
                    "duration_beat": 0.1,
                    "velocity": random.randint(98, 116),
                }
            )

        for beat in [1.0, 3.0]:
            events.append(
                {
                    "type": "note",
                    "pitch": DRUM_MAP["snare"],
                    "drum_name": "snare",
                    "start_beat": base + beat,
                    "duration_beat": 0.1,
                    "velocity": random.randint(94, 110),
                }
            )

        for i in range(8):
            if hat_motif[i % motif_len] == 0:
                continue
            events.append(
                {
                    "type": "note",
                    "pitch": DRUM_MAP["closed_hat"],
                    "drum_name": "closed_hat",
                    "start_beat": base + i * 0.5,
                    "duration_beat": 0.1,
                    "velocity": random.randint(70, 96),
                }
            )
    return events
