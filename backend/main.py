import os
from datetime import datetime, timezone

from anthropic import Anthropic
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from clinical_note_prompt import MOH_ED_SYSTEM_PROMPT, build_user_message

ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")

app = FastAPI(title="Green Zone EDHKL Voice Clinical Notes Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_client: Anthropic | None = None


def get_client() -> Anthropic:
    global _client
    if _client is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=500,
                detail="ANTHROPIC_API_KEY is not set on the server. Add it to backend/.env",
            )
        _client = Anthropic(api_key=api_key)
    return _client


class ConsentRecord(BaseModel):
    patient_agreed_pdpa: bool
    ai_disclosed_to_patient: bool
    clerking_doctor: str = ""


class GenerateNoteRequest(BaseModel):
    transcript: str
    additional_docs: str = ""
    consent: ConsentRecord


class GenerateNoteResponse(BaseModel):
    note: str
    generated_at: str
    model: str


@app.post("/api/generate-note", response_model=GenerateNoteResponse)
def generate_note(req: GenerateNoteRequest):
    if not req.consent.patient_agreed_pdpa or not req.consent.ai_disclosed_to_patient:
        raise HTTPException(
            status_code=400,
            detail="PDPA consent and AI-use disclosure must both be confirmed before generating a note.",
        )
    if not req.transcript.strip():
        raise HTTPException(status_code=400, detail="Transcript is empty.")

    client = get_client()
    try:
        response = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=2000,
            system=MOH_ED_SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": build_user_message(req.transcript, req.additional_docs),
                }
            ],
        )
    except Exception as exc:  # surfaces API errors (auth, rate limit, etc.) to the UI
        raise HTTPException(status_code=502, detail=f"AI service error: {exc}") from exc

    note_text = "".join(
        block.text for block in response.content if getattr(block, "type", None) == "text"
    )
    return GenerateNoteResponse(
        note=note_text,
        generated_at=datetime.now(timezone.utc).isoformat(),
        model=ANTHROPIC_MODEL,
    )


@app.get("/api/health")
def health():
    return {"status": "ok"}


app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
