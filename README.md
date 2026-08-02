# Green Zone EDHKL — Voice Clinical Notes Assistant

A doctor-facing tool: confirm PDPA consent → click Start → talk through the clerking
(and paste in vitals/lab text) → get a draft clinical note in the Malaysian MOH
Emergency Department clerking format for the doctor to review and sign.

## How it works

- **Speech-to-text**: runs in the browser (Chrome/Edge Web Speech API) — no audio
  file is uploaded anywhere. Only the resulting text transcript is sent to the backend.
- **Note generation**: the backend sends the transcript + any pasted documents to an
  LLM, using a system prompt (`backend/clinical_note_prompt.py`) that encodes the
  MOH ED clerking section order and a worked example. The LLM backend is pluggable
  (`backend/llm_backends.py`), switched via the `LLM_PROVIDER` env var:
  - `anthropic` (default) — cloud call to the Claude API. Costs a few cents per note,
    highest quality, needs an API key with billing set up.
  - `ollama` — local call to a model running on your own machine via
    [Ollama](https://ollama.com). Free, works offline, no API key, but needs decent
    hardware and generally drafts lower-quality notes than Claude.
- **No fine-tuning**: neither Claude nor most local models offer easy customer
  fine-tuning for this use case, so "familiarizing" the model is done via prompt
  engineering (the system prompt + few-shot example). Swap in EDHKL's real clerking
  sheet / sample notes in `clinical_note_prompt.py` to sharpen the format match.

## Run it — cloud (Claude API)

```bash
cp backend/.env.example backend/.env
# edit backend/.env: leave LLM_PROVIDER=anthropic, set ANTHROPIC_API_KEY

docker compose up --build
```

Open http://localhost:8000 on the clinic PC.

## Run it — local/offline (Ollama, free)

1. Install Ollama from [ollama.com](https://ollama.com) (Windows/Mac/Linux installer).
2. Pull a model, e.g.:
   ```bash
   ollama pull llama3.1:8b
   ```
3. Make sure Ollama is running (the installer starts it as a background service;
   `ollama list` should work in a terminal without errors).
4. In `backend/.env`, set:
   ```
   LLM_PROVIDER=ollama
   OLLAMA_MODEL=llama3.1:8b
   ```
5. `docker compose up --build`, then open http://localhost:8000.

The container reaches Ollama on the host via `host.docker.internal` (already wired
up in `docker-compose.yml`) — no extra networking setup needed on Windows/Mac.

Note: local models are noticeably slower per note and more likely to miss details
or drift from the requested format than Claude — worth comparing both before
deciding which to run day-to-day.

## Data & compliance — read before real use

This MVP was built as "cloud-first, to see the interface" per initial request.
Before using with real patient data, decide:

1. **PDPA / data residency**: with `LLM_PROVIDER=anthropic`, the transcript text
   leaves the machine to reach the Claude API — confirm this is acceptable under
   EDHKL/hospital IT policy and PDPA. Switching to `LLM_PROVIDER=ollama` (see "Run
   it — local/offline" above) keeps note generation fully on-machine; the only
   remaining external call is the browser's built-in speech-to-text (see next point).
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
  llm_backends.py          Pluggable note generation: Anthropic (cloud) or Ollama (local)
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
