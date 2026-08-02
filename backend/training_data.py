"""Appends doctor-approved (transcript, docs, final note) triples to a local
JSONL file, to be used later as a fine-tuning dataset. Never leaves the
machine on its own — this module only writes to local disk.
"""
import json
import os
import threading
import uuid
from datetime import datetime, timezone

DATA_DIR = os.environ.get("TRAINING_DATA_DIR", os.path.join(os.path.dirname(__file__), "data"))
EXAMPLES_FILE = os.path.join(DATA_DIR, "training_examples.jsonl")

_lock = threading.Lock()


def save_example(transcript: str, additional_docs: str, final_note: str, deidentified_confirmed: bool) -> int:
    """Appends one training example and returns the new total count."""
    os.makedirs(DATA_DIR, exist_ok=True)
    record = {
        "id": str(uuid.uuid4()),
        "saved_at": datetime.now(timezone.utc).isoformat(),
        "deidentified_confirmed": deidentified_confirmed,
        "transcript": transcript,
        "additional_docs": additional_docs,
        "final_note": final_note,
    }
    with _lock:
        with open(EXAMPLES_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        return count_examples()


def count_examples() -> int:
    if not os.path.exists(EXAMPLES_FILE):
        return 0
    with open(EXAMPLES_FILE, "r", encoding="utf-8") as f:
        return sum(1 for _ in f)
