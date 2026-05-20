from __future__ import annotations

import json
import os
import re
from typing import Any

from dotenv import load_dotenv
import httpx


load_dotenv()


def _extract_error_detail(exc: Exception) -> str:
    details: dict[str, Any] = {
        "type": exc.__class__.__name__,
        "message": str(exc),
    }

    for attr in ("status_code", "request_id", "code", "param"):
        value = getattr(exc, attr, None)
        if value is not None:
            details[attr] = value

    response = getattr(exc, "response", None)
    if response is not None:
        details["response_status_code"] = getattr(response, "status_code", None)

        response_text = None
        try:
            response_text = response.text
        except Exception:
            response_text = None
        if response_text:
            details["response_text"] = response_text

        try:
            response_json = response.json()
        except Exception:
            response_json = None
        if response_json is not None:
            details["response_json"] = response_json

    body = getattr(exc, "body", None)
    if body is not None:
        details["body"] = body

    return json.dumps(details, ensure_ascii=False)


def llm_json(prompt: str) -> dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")

    try:
        from openai import OpenAI
    except Exception as e:
        raise RuntimeError("openai SDK is not installed") from e

    model = os.getenv("OPENAI_MODEL", "gpt-5.5")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    client = OpenAI(api_key=api_key, base_url=base_url)
    try:
        resp = client.responses.create(
            model=model,
            input=[
                {"role": "system", "content": "You are a strict JSON generator. Return JSON only."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
    except Exception as e:
        raise RuntimeError(f"LLM request failed: {_extract_error_detail(e)}") from e
    content = getattr(resp, "output_text", "")
    if not content:
        raise RuntimeError("LLM returned empty content")

    # Best-effort parsing: raw JSON, fenced JSON, or first JSON object span.
    if content.startswith("```json"):
        content = content.replace("```json", "")
    if content.endswith("```"):
        content = content.replace("```", "")
    content = content.strip()

    try:
        return json.loads(content)
    except Exception:
        raise RuntimeError("Failed to parse JSON from LLM response")
