# Fine-tuning the clinical note model

Two versions of the same notebook — both fine-tune a small Llama model with LoRA (via
[Unsloth](https://unsloth.ai)) on the training examples you've collected through the app, then
export a GGUF file to run locally in Ollama. Training runs on a free cloud GPU — nothing about your
laptop or Docker setup needs GPU support for this step.

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
4. At the end, it copies the `.gguf` file + an auto-generated Ollama `Modelfile` to your Google
   Drive (asks you to authorize Drive access) — download both from drive.google.com, or they'll
   already be local if you have Google Drive Desktop syncing.
5. Put both files together in one folder in your project, e.g. `V2textDoc\models\edhkl_clinical_notes\`, then:
   ```
   ollama create edhkl-clinical-notes -f Modelfile
   ```
6. In `backend/.env`, set `OLLAMA_MODEL=edhkl-clinical-notes`, then
   `docker compose down && docker compose up` (no rebuild needed).

## How to run it — Kaggle (alternative when Colab's quota is exhausted)

1. Go to [kaggle.com/code](https://www.kaggle.com/code), create a new notebook, and upload
   `clinical_notes_lora_kaggle.ipynb` (File → Import Notebook).
2. In the right-hand settings panel: **Accelerator → GPU T4 x2**, and **Internet → On**.
3. Click **+ Add Input** (right panel) → Upload → add both `training_examples.jsonl` and
   `clinical_note_prompt.py` as a new dataset (any name — the notebook finds them automatically
   under `/kaggle/input/`).
4. Run all cells. At the end, open the file browser panel (folder icon, right side), navigate into
   `edhkl_clinical_notes`, and download the `.gguf` file and `Modelfile` directly — no zip, no
   Drive step needed, Kaggle's own download handles large files fine.
5. Continue with the same `ollama create` / `.env` steps as the Colab version above.

## Notes

- **Only synthetic/de-identified examples should go into this pipeline** — the dataset leaves your
  laptop to reach Colab's GPU. Fine, since the collected examples are marked de-identified at save
  time; don't skip that checkbox once real patient-derived text is involved.
- **Dataset size**: with only a handful of examples, expect the fine-tune to nudge style/format
  more than fix reasoning gaps. If the model starts outputting near-identical text regardless of
  input (overfitting), that means too few examples for the number of training epochs — add more
  examples or lower `num_train_epochs` in the notebook.
- Default base model is `unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit`, matching the `llama3.1:8b`
  you've already been testing. Swap to a smaller Unsloth 4-bit model name in the notebook if you'd
  rather fine-tune a lighter one.
