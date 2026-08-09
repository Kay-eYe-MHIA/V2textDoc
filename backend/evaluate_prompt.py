"""Batch-runs the 10 synthetic sample cases through the actual note-generation
pipeline (whatever LLM_PROVIDER / model is currently configured in .env) and
prints each result next to its reference note, for judging prompt/model
quality across a range of presentations in one go.

Run inside the container:
    docker compose exec app python evaluate_prompt.py
    # or, to save a copy for later review:
    docker compose exec app python evaluate_prompt.py > eval_output.txt
"""
from llm_backends import generate_note_text
from seed_training_data import CASES


def main():
    for i, case in enumerate(CASES, 1):
        print("=" * 80)
        print(f"CASE {i}/{len(CASES)}: {case['label']}")
        print("=" * 80)
        try:
            note, model_used = generate_note_text(
                case["transcript"], case["additional_docs"], mode="summary"
            )
        except Exception as exc:
            print(f"ERROR generating note: {exc}")
            continue

        print(f"\n--- MODEL OUTPUT ({model_used}) ---\n")
        print(note)
        print("\n--- REFERENCE (ideal) NOTE ---\n")
        print(case["final_note"])
        print()


if __name__ == "__main__":
    main()
