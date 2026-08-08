# Green Zone EDHKL — Voice Clinical Notes Assistant

A doctor-facing tool: confirm PDPA consent → click Start → talk through the clerking
(and paste in vitals/lab text) → get a draft clinical note in the Malaysian MOH
Emergency Department clerking format for the doctor to review and sign.

## How it works

- **Recording modes**: the doctor picks one before starting each case —
  - **Dictate a summary after clerking** — the original flow: the doctor speaks a
    clean summary alone.
  - **Record the live consultation** — the mic stays open during the actual
    doctor-patient conversation, capturing both voices; the note is then generated
    from that raw transcript instead of a curated summary. This is more sensitive
    (it captures the patient's own voice/words), so the UI shows an extra warning
    to get separate patient buy-in for this mode specifically.
- **Speech-to-text**: [faster-whisper](https://github.com/SYSTRAN/faster-whisper)
  (local Whisper) running in the backend container — audio never leaves the machine.
  The browser records audio (`MediaRecorder`) and uploads it to `/api/transcribe`;
  the backend writes it to a temp file just long enough to transcribe, then deletes
  it immediately — raw audio is never written to permanent storage. First run
  downloads the model weights automatically (needs internet once; cached after).
- **Note generation**: the backend sends the transcript + any pasted documents to an
  LLM, using a system prompt (`backend/clinical_note_prompt.py`) that encodes the
  MOH ED clerking section order and a worked example. The LLM backend is pluggable
  (`backend/llm_backends.py`), switched via the `LLM_PROVIDER` env var:
  - `anthropic` (default) — cloud call to the Claude API. Costs a few cents per note,
    highest quality, needs an API key with billing set up.
  - `ollama` — local call to a model running on your own machine via
    [Ollama](https://ollama.com). Free, works offline, no API key, but needs decent
    hardware and generally drafts lower-quality notes than Claude.
- **No fine-tuning yet**: Claude doesn't offer customer fine-tuning for this use
  case, so its "familiarization" is done via prompt engineering (the system prompt
  + few-shot example in `clinical_note_prompt.py`). Local Llama models *can* be
  fine-tuned (e.g. via LoRA/QLoRA, see "Building a training dataset" below) — the
  app now has a built-in way to collect the training data for that as you use it.

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

## Building a training dataset (for future fine-tuning)

Every time you review a generated note (Step 3), you can tick "I confirm this
transcript/note has been de-identified" and click **Save as Training Example**.
This appends the transcript + supporting docs + your final (possibly edited)
note as one line to `data/training_examples.jsonl` on your own machine — never
uploaded anywhere by this app.

- The `data/` folder is git-ignored on purpose — it will contain clinical text,
  so it must never be committed to this repo.
- **Only save de-identified examples** — the checkbox is a reminder, not a
  guarantee; it's still on the doctor to actually strip patient names/IC numbers
  from the transcript before saving. This matters even more if the resulting
  dataset is later moved to a rented cloud GPU for fine-tuning a larger model
  (see "is it doable" discussion — QLoRA fine-tuning, export to GGUF, then run
  the fine-tuned model locally via Ollama exactly as today).
- Once there are enough examples (aim for 50-200+ covering a range of
  presentations), they're ready to feed into a fine-tuning pipeline — see
  `training/` for a ready-to-run Colab notebook that fine-tunes a local Llama
  model with LoRA on this dataset and exports it for Ollama.

## Data & compliance — read before real use

This MVP was built as "cloud-first, to see the interface" per initial request.
Before using with real patient data, decide:

1. **PDPA / data residency**: speech-to-text is fully local (Whisper) regardless
   of `LLM_PROVIDER`. With `LLM_PROVIDER=anthropic`, the *text* transcript (not
   audio) leaves the machine to reach the Claude API — confirm this is acceptable
   under EDHKL/hospital IT policy and PDPA. Switching to `LLM_PROVIDER=ollama`
   (see "Run it — local/offline" above) keeps everything, audio and text, fully
   on-machine.
2. **Live consultation recording** (the "Record the live consultation" mode) is a
   meaningfully bigger privacy step than dictating a summary — it captures the
   patient's own voice and words directly, not just what the doctor chooses to
   summarize. The UI's extra warning before this mode is a minimum, not a
   substitute for an actual hospital-approved consent process for this specific
   use case. Also note Whisper does not distinguish speakers (no diarization) —
   the system prompt asks the model to infer patient-reported vs. doctor-observed
   from context, but that's inherently imperfect; ambiguous cases are meant to
   land in the note's "FLAGS FOR DOCTOR" section rather than being guessed.
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
  main.py                  FastAPI app: /api/generate-note, /api/transcribe, /api/health, serves frontend
  transcription.py         Local Whisper (faster-whisper) speech-to-text
  llm_backends.py          Pluggable note generation: Anthropic (cloud) or Ollama (local)
  clinical_note_prompt.py  MOH ED format system prompt + worked example (summary + conversation modes)
  training_data.py         Appends approved examples to data/training_examples.jsonl
  requirements.txt
  Dockerfile
  .env.example
frontend/
  index.html               Consent → Record (mode select) → Draft note, 3-step UI
  app.js                   MediaRecorder audio capture + calls backend
  style.css
docker-compose.yml
data/                      (git-ignored) collected training examples, created at runtime
```

## Next steps to discuss

- Voice-based note editing (speak a correction after the draft is generated)
- Patient biodata form ahead of consent
- Fine-tuning a local model on the collected `data/training_examples.jsonl`
  (see `training/` — RunPod pipeline in progress)
- Real EDHKL clerking template + sample notes
- Persisting notes to an EHR / hospital system instead of copy-paste
- Multi-user auth (currently single-PC, no login)
