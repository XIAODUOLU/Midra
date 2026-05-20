from __future__ import annotations

from music_agent.agents.llm_client import llm_json
from music_agent.prompts import build_song_planner_prompt


def plan_song(intent_result: dict) -> dict:
    prompt = build_song_planner_prompt(intent_result["intent"])
    data = llm_json(prompt)
    data.setdefault("_meta", {})
    data["_meta"]["source"] = "llm"
    return data
