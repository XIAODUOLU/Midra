from __future__ import annotations

from music_agent.agents.llm_client import llm_json
from music_agent.prompts import build_arrangement_planner_prompt


def plan_arrangement(intent_result: dict, song_plan: dict) -> dict:
    prompt = build_arrangement_planner_prompt(intent_result["intent"], song_plan["song_plan"])
    data = llm_json(prompt)
    data.setdefault("_meta", {})
    data["_meta"]["source"] = "llm"
    return data
