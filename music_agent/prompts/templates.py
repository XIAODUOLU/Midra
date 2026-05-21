from __future__ import annotations

from pathlib import Path

from music_agent.core.music_theory import NOTE_TO_SEMITONE, SEMITONE_TO_NOTE


def _load_instrument_knowledge() -> str:
    knowledge_path = Path(__file__).resolve().parent.parent / "knowledges" / "instruments.md"
    try:
        return knowledge_path.read_text(encoding="utf-8").strip()
    except Exception:
        return ""


def _load_chord_knowledge() -> str:
    knowledge_path = Path(__file__).resolve().parent.parent / "knowledges" / "chords.md"
    try:
        return knowledge_path.read_text(encoding="utf-8").strip()
    except Exception:
        return ""


def _load_note_knowledge() -> str:
    knowledge_path = Path(__file__).resolve().parent.parent / "knowledges" / "notes.md"
    try:
        return knowledge_path.read_text(encoding="utf-8").strip()
    except Exception:
        return ""


def build_intent_parser_prompt(user_prompt: str, enforce_core_tracks: bool = True) -> str:
    track_rule = (
        "- requested_tracks must include at least drums,bass,chords,lead."
        if enforce_core_tracks
        else "- requested_tracks should be decided by musical intent; do not force fixed instrument sets."
    )
    return f"""
You are an Intent Parser for a MIDI music generation pipeline.
Return JSON only. No markdown, no explanations.

User prompt: {user_prompt}

Output fields:
- task_type
- user_prompt
- intent.style (list)
- intent.mood (list)
- intent.use_case
- intent.duration_seconds (number)
- intent.loopable (bool)
- intent.complexity
- intent.requested_tracks (list)
- intent.tempo_preference (slow|medium|fast|very_fast)
- intent.must_have (list)
- intent.avoid (list)

Rules:
- Output must follow this exact nested JSON shape (no dotted keys):
{{
  "task_type": "generate_music",
  "user_prompt": "...",
  "intent": {{
    "style": ["..."],
    "mood": ["..."],
    "use_case": "...",
    "duration_seconds": 30,
    "loopable": true,
    "complexity": "medium",
    "requested_tracks": ["drums", "bass", "chords", "lead"],
    "tempo_preference": "fast",
    "must_have": ["drums", "bass", "chords", "lead"],
    "avoid": []
  }}
}}
- Never output keys like "intent.style" or "intent.mood".
{track_rule}
- Fill missing values with reasonable defaults.
""".strip()


def build_song_planner_prompt(intent: dict) -> str:
    chord_knowledge = _load_chord_knowledge()
    return f"""
You are a Song Planner for a MIDI music generation pipeline.
Return JSON only. No markdown, no explanations.

Input intent: {intent}

Chord progression knowledge:
{chord_knowledge}

Output top-level key: song_plan
Required song_plan fields:
title,bpm,time_signature,key,total_bars,estimated_duration_seconds,
loopable,global_style,sections,chord_progression

Constraints:
- time_signature must be 4/4 in MVP
- bpm should match tempo_preference in intent
- total_bars must be one of 8,12,16,24,32
- chord_progression should contain at least 4 bars and be loopable
- Do not repeat exactly the same melodic contour template across runs.
- Create a fresh composition each run while keeping style consistency.
- Vary harmonic rhythm, section contrast, and motif development naturally.
- Chord symbol compatibility is strict for current parser:
  - Allowed chord form: root major or root minor only, e.g. C, Dm, Bb, F#m
  - NOT allowed: slash chords (e.g. Eb/G), extensions (maj7, m7, sus4, add9), altered chords
  - Chord roots must come from this map: {NOTE_TO_SEMITONE}
  - Canonical note names used by the system: {SEMITONE_TO_NOTE}
- Use the chord progression knowledge above as the primary decision guide:
  - infer major/minor mode from intent style, mood, and use_case
  - choose a chord-degree template that matches the requested style and emotion
  - convert roman-numeral degrees into concrete chord symbols in the selected key
  - keep chord_progression section-aware and loopable
  - if the knowledge suggests unsupported chords, adapt them to parser-compatible major/minor triads
- chord_progression must contain concrete chord symbols only, not roman numerals.
- Output must follow this exact JSON shape:
{{
  "song_plan": {{
    "title": "...",
    "bpm": 140,
    "time_signature": {{"numerator": 4, "denominator": 4}},
    "key": {{"root": "D", "mode": "minor", "scale": "natural_minor"}},
    "total_bars": 16,
    "estimated_duration_seconds": 27.4,
    "loopable": true,
    "global_style": {{"primary": "cyberpunk", "energy": 0.8, "darkness": 0.7, "brightness": 0.3}},
    "sections": [{{"id": "intro", "name": "Intro", "start_bar": 0, "length_bars": 4, "energy": 0.4}}],
    "chord_progression": [{{"bar": 0, "chord": "Dm"}}, {{"bar": 1, "chord": "Bb"}}, {{"bar": 2, "chord": "C"}}, {{"bar": 3, "chord": "A"}}]
  }}
}}
""".strip()


def build_arrangement_planner_prompt(
    intent: dict,
    song_plan: dict,
    enforce_core_tracks: bool = True,
) -> str:
    arrangement_track_rule = (
        "- tracks must include core tracks: drums,bass,chords,lead"
        if enforce_core_tracks
        else "- tracks should be decided by style and user intent; do not force fixed core instruments"
    )
    instrument_knowledge = _load_instrument_knowledge()
    return f"""Instrument knowledge:
{instrument_knowledge}

You are an Arrangement Planner for a MIDI music generation pipeline.
Return JSON only. No markdown, no explanations.

Input intent: {intent}
Input song_plan: {song_plan}

Output format:
{{"arrangement": {{"tracks": {{...}} }} }}

Rules:
{arrangement_track_rule}
- extra tracks are allowed when needed by style or user request
- drums must use channel=9 and program=null
- non-drum tracks must not use channel=9
- each track must include:
  id,name,role,enabled,is_core_track,generation_strategy,midi,mix,style,sections
- Encourage compositional variation across runs:
  - Do not lock to one fixed melodic direction.
  - Prefer different section-level density and role interaction per run.
  - Keep requested style, but allow creative arrangement decisions.
- Output must follow this exact nested shape:
{{
  "arrangement": {{
    "tracks": {{
      "drums": {{
        "id": "drums",
        "name": "Drums",
        "role": "rhythm",
        "enabled": true,
        "is_core_track": true,
        "generation_strategy": "drum_generator",
        "midi": {{"channel": 9, "program": null}},
        "mix": {{"volume": 105, "pan": 64}},
        "style": {{"pattern_type": "driving_electronic", "density": "high"}},
        "sections": {{"intro": {{"active": true, "density": "low"}}, "main_a": {{"active": true, "density": "medium"}}, "main_b": {{"active": true, "density": "high"}}}}
      }}
    }}
  }}
}}
""".strip()


def build_track_note_generator_prompt(song_plan: dict, arrangement_track: dict) -> str:
    total_bars = song_plan["total_bars"]
    beats_per_bar = song_plan["time_signature"]["numerator"]
    total_beats = total_bars * beats_per_bar
    track_id = arrangement_track.get("id", "unknown")
    role = arrangement_track.get("role", "unknown")
    note_knowledge = _load_note_knowledge()
    return f"""
You are a MIDI note event generator.
Return JSON only. No markdown, no explanations.

Input song_plan: {song_plan}
Input track: {arrangement_track}

Note generation knowledge:
{note_knowledge}

Output format (exact):
{{
  "events": [
    {{"type":"note","pitch":60,"start_beat":0.0,"duration_beat":0.5,"velocity":96}}
  ]
}}

Constraints:
- track_id: {track_id}
- role: {role}
- total_bars: {total_bars}
- beats_per_bar: {beats_per_bar}
- total_beats: {total_beats}
- Keep style coherence with song_plan and track.style.
- Generate fresh musical content for this run.
- Use the note generation knowledge above as the primary decision guide:
  - derive note choices from the active chord at each beat/bar
  - choose register, duration, density, velocity, and rhythm according to track role, instrument, style, and section energy
  - keep bass, chords, pad, lead, arpeggio, drums, strings, brass, guitar, piano, ethnic instruments, and FX behavior role-appropriate
  - avoid all tracks using the same rhythmic density or all tracks playing full chords
  - make loop endings lead naturally back to the beginning when song_plan.loopable is true
- Respect harmonic compatibility with current chord parser:
  - Chord symbols in song_plan are major/minor triads only
  - Do not invent slash chords or extended symbols in any output text
  - Allowed roots are constrained by: {NOTE_TO_SEMITONE}
- 0 <= pitch <= 127
- 1 <= velocity <= 127
- start_beat >= 0
- duration_beat > 0
- start_beat + duration_beat <= total_beats
- Output key must be exactly "events".
""".strip()
