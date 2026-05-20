from __future__ import annotations

NOTE_TO_SEMITONE = {
    "C": 0,
    "C#": 1,
    "Db": 1,
    "D": 2,
    "D#": 3,
    "Eb": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "Gb": 6,
    "G": 7,
    "G#": 8,
    "Ab": 8,
    "A": 9,
    "A#": 10,
    "Bb": 10,
    "B": 11,
}

SEMITONE_TO_NOTE = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def note_name_to_midi(note_name: str) -> int:
    name = note_name[:-1]
    octave = int(note_name[-1])
    return (octave + 1) * 12 + NOTE_TO_SEMITONE[name]


def midi_to_note_name(midi_note: int) -> str:
    octave = midi_note // 12 - 1
    note = SEMITONE_TO_NOTE[midi_note % 12]
    return f"{note}{octave}"


def _rotate_scale(root: str, intervals: list[int]) -> list[str]:
    root_semi = NOTE_TO_SEMITONE[root]
    return [SEMITONE_TO_NOTE[(root_semi + i) % 12] for i in intervals]


def get_scale(root: str, scale: str) -> list[str]:
    if scale == "major":
        return _rotate_scale(root, [0, 2, 4, 5, 7, 9, 11])
    if scale in {"natural_minor", "minor"}:
        return _rotate_scale(root, [0, 2, 3, 5, 7, 8, 10])
    raise ValueError(f"Unsupported scale: {scale}")


def parse_chord(chord: str) -> list[str]:
    root = chord[:-1] if chord.endswith("m") else chord
    is_minor = chord.endswith("m")
    root_semi = NOTE_TO_SEMITONE[root]
    third = (root_semi + (3 if is_minor else 4)) % 12
    fifth = (root_semi + 7) % 12
    return [SEMITONE_TO_NOTE[root_semi], SEMITONE_TO_NOTE[third], SEMITONE_TO_NOTE[fifth]]


def chord_to_midi_notes(chord: str, base_octave: int = 3) -> list[int]:
    notes = parse_chord(chord)
    result = []
    for n in notes:
        result.append(note_name_to_midi(f"{n}{base_octave}"))
    return result

