# Green Zone EDHKL — Voice Clinical Notes Assistant

A doctor-facing tool: confirm PDPA consent → click Start → talk through the clerking
(and paste in vitals/lab text) → get a draft clinical note in the Malaysian MOH
Emergency Department clerking format for the doctor to review and sign.

## How it works

- **Speech-to-text**: runs in the browser (Chrome/Edge Web Speech API) — no audio
  file is uploaded anywhere. Only the resulting text transcript is sent to the backend.
- **Note generation**: the backend sends the transcript + any pasted documents to the
  Claude API (Anthropic), using a system prompt (`backend/clinical_note_prompt.py`)
  that encodes the MOH ED clerking section order and a worked example. This is a
  cloud call — see "Data & compliance" below before using with real patient data.
- **No fine-tuning**: Claude does not currently offer customer fine-tuning, so
  "familiarizing" the model is done via prompt engineering (the system prompt +
  few-shot example). Swap in EDHKL's real clerking sheet / sample notes in
  `clinical_note_prompt.py` to sharpen the format match.

## Run it

```bash
cp backend/.env.example backend/.env
# edit backend/.env and set ANTHROPIC_API_KEY

docker compose up --build
```

Open http://localhost:8000 on the clinic PC.

## Data & compliance — read before real use

This MVP was built as "cloud-first, to see the interface" per initial request.
Before using with real patient data, decide:

1. **PDPA / data residency**: the transcript text currently leaves the machine
   to reach the Claude API. Confirm this is acceptable under EDHKL/hospital IT
   policy and PDPA, or switch to a fully local pipeline (local Whisper for
   speech-to-text is already local; swap the Claude call for a locally-hosted
   LLM, e.g. via Ollama, and this becomes fully offline).
2. **Speech-to-text vendor**: the browser's built-in recognizer (Chrome/Edge)
   sends audio to Google's servers for transcription. If that's not acceptable,
   this needs to be replaced with a local Whisper model instead.
3. **Clinical sign-off**: every generated note is a draft. The UI reminds the
   doctor to review/edit before it becomes part of the medical record — this
   should stay a hard requirement, not just a UI hint.
4. **Real clerking template**: `clinical_note_prompt.py` currently uses a
   generic MOH ED structure. Replace the worked example with EDHKL's actual
   clerking sheet layout and 2-3 real (de-identified) sample notes for a much
   closer format match.

## Project layout

```
backend/
  main.py                  FastAPI app: /api/generate-note, /api/health, serves frontend
  clinical_note_prompt.py  MOH ED format system prompt + worked example
  requirements.txt
  Dockerfile
  .env.example
frontend/
  index.html               Consent → Record → Draft note, 3-step UI
  app.js                   Web Speech API recording + calls backend
  style.css
docker-compose.yml
```

## Next steps to discuss

- Local/offline STT + LLM (see compliance section)
- Real EDHKL clerking template + sample notes
- Persisting notes to an EHR / hospital system instead of copy-paste
- Multi-user auth (currently single-PC, no login)
