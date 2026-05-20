from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class NoteEvent:
    type: str
    pitch: int
    start_beat: float
    duration_beat: float
    velocity: int
    note_name: str | None = None
    drum_name: str | None = None


@dataclass
class TrackIR:
    id: str
    name: str
    role: str
    channel: int
    program: int | None
    volume: int
    pan: int
    enabled: bool
    is_core_track: bool
    events: list[NoteEvent] = field(default_factory=list)


@dataclass
class MidiIR:
    meta: dict[str, Any]
    tracks: list[TrackIR]


@dataclass
class ArrangementTrack:
    id: str
    name: str
    role: str
    enabled: bool
    is_core_track: bool
    generation_strategy: str
    midi: dict[str, Any]
    mix: dict[str, Any]
    style: dict[str, Any]
    sections: dict[str, Any]
    description: str | None = None


def to_dict(data: Any) -> Any:
    if hasattr(data, "__dataclass_fields__"):
        return asdict(data)
    if isinstance(data, list):
        return [to_dict(x) for x in data]
    if isinstance(data, dict):
        return {k: to_dict(v) for k, v in data.items()}
    return data

