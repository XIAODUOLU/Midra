from __future__ import annotations

import random

from music_agent.core.music_theory import chord_to_midi_notes


def generate_chords(song_plan: dict, track: dict) -> list[dict]:
    total_bars = song_plan["song_plan"]["total_bars"]
    prog = song_plan["song_plan"]["chord_progression"]

    motif_len = 8
    motif = [random.choice([0, 1, 2, 3, 4, 5, 6]) for _ in range(motif_len)]
    motif[0] = 0
    motif[-1] = random.choice([0, 2, 4])

    events: list[dict] = []
    for bar in range(total_bars):
        chord = prog[bar % len(prog)]["chord"]
        base_octave = 2 if motif[bar % motif_len] in (0, 1, 2) else 3
        notes = chord_to_midi_notes(chord, base_octave=base_octave)
        base = bar * 4.0
        pattern_type = "block" if motif[bar % motif_len] in (0, 3, 6) else "arp"

        for p in notes:
            if pattern_type == "block":
                events.append(
                    {
                        "type": "note",
                        "pitch": p,
                        "start_beat": base,
                        "duration_beat": random.choice([2.0, 3.0, 4.0]),
                        "velocity": random.randint(54, 78),
                    }
                )
            else:
                step = 0.0
                while step < 4.0:
                    events.append(
                        {
                            "type": "note",
                            "pitch": p,
                            "start_beat": base + step,
                            "duration_beat": random.choice([0.25, 0.5, 0.75]),
                            "velocity": random.randint(52, 74),
                        }
                    )
                    step += 1.0
    return events
