# Fine-tuning the clinical note model

Two versions of the same notebook — both fine-tune a small Llama model with LoRA (via
[Unsloth](https://unsloth.ai)) on the training examples you've collected through the app, then
export just the small LoRA adapter for Ollama to load on top of your existing `llama3.1:8b`. Training
runs on a free cloud GPU — nothing about your laptop or Docker setup needs GPU support for this step.

Earlier versions of these notebooks merged the LoRA into the full 8B model and converted the whole
thing to GGUF (building llama.cpp from source, processing a ~16GB merged model) — that step
repeatedly hung, ran out of disk, or timed out in testing. Ollama can load a LoRA adapter directly
on top of a base model via the Modelfile `ADAPTER` instruction (safetensors, no GGUF conversion
needed, tens of MB instead of gigabytes), so that fragile step is gone entirely.

- `clinical_notes_lora_colab.ipynb` — Google Colab (free T4, daily quota)
- `clinical_notes_lora_kaggle.ipynb` — Kaggle Notebooks (free T4 x2, ~30 hrs/week quota, separate
  from Colab's — use this one when Colab's quota is exhausted)

## How to run it — Colab

1. Open [colab.research.google.com](https://colab.research.google.com), upload
   `clinical_notes_lora_colab.ipynb` (File → Upload notebook).
2. Runtime → Change runtime type → **T4 GPU**.
3. Run cells top to bottom (Runtime → Run all works too). You'll be prompted partway through to
   upload two files from your `V2textDoc` project:
   - `backend/data/training_examples.jsonl`
   - `backend/clinical_note_prompt.py`

   (Uploading `clinical_note_prompt.py` — rather than pasting the prompt text into the notebook —
   means training always uses the exact same system prompt the app sends at inference time, even
   after you edit it.)
4. At the end, it copies the small LoRA adapter folder to your Google Drive (asks you to authorize
   Drive access) — download it from drive.google.com, or it'll already be local if you have Google
   Drive Desktop syncing.
5. Put the folder inside your project, e.g. `V2textDoc\models\edhkl_clinical_notes\`. In
   `V2textDoc\models\`, create a plain text file named `Modelfile` containing exactly:
   ```
   FROM llama3.1:8b
   ADAPTER ./edhkl_clinical_notes
   ```
6. From a terminal in `V2textDoc\models\`:
   ```
   ollama create edhkl-clinical-notes -f Modelfile
   ```
7. In `backend/.env`, set `OLLAMA_MODEL=edhkl-clinical-notes`, then
   `docker compose down && docker compose up` (no rebuild needed).

## How to run it — Kaggle (alternative when Colab's quota is exhausted)

1. Go to [kaggle.com/code](https://www.kaggle.com/code), create a new notebook, and upload
   `clinical_notes_lora_kaggle.ipynb` (File → Import Notebook).
2. In the right-hand settings panel: **Accelerator → GPU T4 x2**, and **Internet → On**.
3. Click **+ Add Input** (right panel) → Upload → add both `training_examples.jsonl` and
   `clinical_note_prompt.py` as a new dataset (any name — the notebook finds them automatically
   under `/kaggle/input/`).
4. Run all cells. At the end, open the file browser panel (folder icon, right side), navigate into
   `edhkl_clinical_notes`, and download the small adapter files directly.
5. Continue with the same `Modelfile` / `ollama create` / `.env` steps as the Colab version above.

## Known issue: Ollama's `ADAPTER <folder>` fails on Windows

If `ollama create` errors with `no Modelfile or safetensors files found` even though the folder and
files clearly exist, that's a known unresolved Ollama bug on Windows
([ollama/ollama#13314](https://github.com/ollama/ollama/issues/13314)) — not something wrong with
your files. Neither relative nor absolute paths fix it, and putting the Modelfile inside the
adapter folder with `ADAPTER .` doesn't help either.

**Workaround**: convert the adapter to a single GGUF file instead of a safetensors folder — use
`convert_adapter_to_gguf_colab.ipynb`. It doesn't need a GPU (pure CPU tensor conversion), so no
quota to worry about; just re-upload the adapter files you already downloaded. One gotcha: point
`--base-model-id` at the **non-quantized** model (`unsloth/Meta-Llama-3.1-8B-Instruct`, no
`-bnb-4bit` suffix) — llama.cpp's conversion tooling can't dequantize bitsandbytes models and will
fail with `NotImplementedError: Quant method is not yet supported: 'bitsandbytes'` if you point it
at the same `-bnb-4bit` ID used for training. The resulting `edhkl_clinical_notes.gguf` goes in the
Modelfile as `ADAPTER ./edhkl_clinical_notes.gguf` (a single file, not a folder) — this uses a
different Ollama code path that isn't affected by the directory-scanning bug.

## Lessons learned from the first real fine-tune attempt

15 examples (10 synthetic + 5 messy/garbled-transcription), 5 epochs, on `llama3.1:8b`. Result: it
made one case genuinely better (correctly connecting a head injury's LOC+vomiting to a missing CT
brain plan), but got *worse* on several others — most notably, it started inserting a
"lactate/blood cultures not mentioned" flag into completely unrelated cases (a STEMI, an asthma
exacerbation, a head injury) with zero clinical basis for it. That phrase came from the 2-3
sepsis-related training examples; the model memorized the surface phrasing rather than learning
when it actually applies. Classic overfitting on too little, too-similar data, made worse by too
many epochs.

**Before trying again:**
- Grow the dataset well past 15 — aim for 50+ examples, deliberately varied (don't let any one
  presentation type like sepsis dominate a large fraction of the set).
- Keep `num_train_epochs` low (2, the current default) until the dataset is much bigger.
- Re-run `evaluate_prompt.py` against the fine-tuned model the same way as the stock model, and
  compare case-by-case against the reference notes — don't just eyeball one or two outputs. This is
  exactly what caught the regression above.
- If a fine-tune makes things worse, reverting `OLLAMA_MODEL` back to `llama3.1:8b` in
  `backend/.env` is instant and lossless — the base model and your training data are both still
  there.

## Other notes

- **Only synthetic/de-identified examples should go into this pipeline** — the dataset leaves your
  laptop to reach Colab's GPU. Fine, since the collected examples are marked de-identified at save
  time; don't skip that checkbox once real patient-derived text is involved.
- Default base model is `unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit`, matching the `llama3.1:8b`
  you've already been testing. Swap to a smaller Unsloth 4-bit model name in the notebook if you'd
  rather fine-tune a lighter one.
