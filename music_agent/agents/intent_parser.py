from __future__ import annotations

from music_agent.agents.llm_client import llm_json
from music_agent.prompts import build_intent_parser_prompt

def parse_intent(user_prompt: str) -> dict:
    prompt = build_intent_parser_prompt(user_prompt)
    data = llm_json(prompt)
    if "intent" not in data or not isinstance(data["intent"], dict):
        raise ValueError("Invalid intent JSON shape: missing nested 'intent' object")
    data.setdefault("_meta", {})
    data["_meta"]["source"] = "llm"
    return data
