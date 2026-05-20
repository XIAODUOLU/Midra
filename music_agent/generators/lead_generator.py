from __future__ import annotations

import random

from music_agent.core.music_theory import get_scale, note_name_to_midi


def generate_lead(song_plan: dict, track: dict) -> list[dict]:
    root = song_plan["song_plan"]["key"]["root"]
    scale = get_scale(root, "natural_minor")

    # Create a fresh motif per run so melodic contour can evolve instead of staying fixed.
    # Resume mode remains stable because track_events are checkpointed.
    motif_len = 8
    motif = [random.choice([0, 1, 2, 3, 4, 5, 6]) for _ in range(motif_len)]
    # Keep phrase anchor to improve musicality.
    motif[0] = 0
    motif[-1] = random.choice([0, 2, 4])

    # Optional contour movement, small interval steps preferred.
    for i in range(1, motif_len - 1):
        if random.random() < 0.65:
            step = random.choice([-2, -1, 1, 2])
            motif[i] = max(0, min(6, motif[i - 1] + step))

    total_bars = song_plan["song_plan"]["total_bars"]
    events: list[dict] = []
    for bar in range(total_bars):
        base = bar * 4.0
        for i, step in enumerate(motif):
            pitch = note_name_to_midi(f"{scale[step % len(scale)]}5")
            velocity = random.randint(84, 108)
            duration = random.choice([0.25, 0.4, 0.5, 0.75])
            events.append(
                {
                    "type": "note",
                    "pitch": pitch,
                    "start_beat": base + i * 0.5,
                    "duration_beat": duration,
                    "velocity": velocity,
                }
            )
    return events
