import os
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from llm_backends import generate_note_text

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")

app = FastAPI(title="Green Zone EDHKL Voice Clinical Notes Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


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

    try:
        note_text, model_used = generate_note_text(req.transcript, req.additional_docs)
    except RuntimeError as exc:  # missing config / unreachable local model
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:  # surfaces API errors (auth, rate limit, etc.) to the UI
        raise HTTPException(status_code=502, detail=f"AI service error: {exc}") from exc

    return GenerateNoteResponse(
        note=note_text,
        generated_at=datetime.now(timezone.utc).isoformat(),
        model=model_used,
    )


@app.get("/api/health")
def health():
    return {"status": "ok"}


app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
