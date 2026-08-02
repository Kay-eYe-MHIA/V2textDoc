"""Pluggable note-generation backends, selected via LLM_PROVIDER env var:

  - "anthropic" (default): cloud call to the Claude API. Costs per request.
  - "ollama": local call to an Ollama server (free, offline, no API key).
"""
import os

import httpx
from anthropic import Anthropic

from clinical_note_prompt import MOH_ED_SYSTEM_PROMPT, build_user_message

ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.1:8b")

_anthropic_client: Anthropic | None = None


def _get_anthropic_client() -> Anthropic:
    global _anthropic_client
    if _anthropic_client is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set on the server. Add it to backend/.env")
        _anthropic_client = Anthropic(api_key=api_key)
    return _anthropic_client


def _generate_with_anthropic(transcript: str, additional_docs: str) -> str:
    client = _get_anthropic_client()
    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=2000,
        system=MOH_ED_SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": build_user_message(transcript, additional_docs)}
        ],
    )
    return "".join(
        block.text for block in response.content if getattr(block, "type", None) == "text"
    )


def _generate_with_ollama(transcript: str, additional_docs: str) -> str:
    try:
        resp = httpx.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": [
                    {"role": "system", "content": MOH_ED_SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": build_user_message(transcript, additional_docs),
                    },
                ],
                "stream": False,
            },
            timeout=180.0,
        )
        resp.raise_for_status()
    except httpx.ConnectError as exc:
        raise RuntimeError(
            f"Could not reach Ollama at {OLLAMA_BASE_URL}. Is Ollama running on the host "
            f"machine, and has the model been pulled (`ollama pull {OLLAMA_MODEL}`)?"
        ) from exc
    except httpx.HTTPStatusError as exc:
        raise RuntimeError(f"Ollama returned an error: {exc.response.text}") from exc

    data = resp.json()
    return data["message"]["content"]


def generate_note_text(transcript: str, additional_docs: str) -> tuple[str, str]:
    """Returns (note_text, model_name_used)."""
    provider = os.environ.get("LLM_PROVIDER", "anthropic").strip().lower()
    if provider == "ollama":
        return _generate_with_ollama(transcript, additional_docs), OLLAMA_MODEL
    return _generate_with_anthropic(transcript, additional_docs), ANTHROPIC_MODEL
