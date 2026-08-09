"""Seeds the 5 messy/garbled-transcription cases from sample_cases_messy.py
into data/training_examples.jsonl, on top of the original 10 from
seed_training_data.py. Safe to run once after that script — appends only
these 5, no duplication of the original 10.

Run inside the container:
    docker compose exec app python seed_messy_cases.py
"""
from sample_cases_messy import CASES
from training_data import save_example


def main():
    total = 0
    for case in CASES:
        total = save_example(
            transcript=case["transcript"],
            additional_docs=case["additional_docs"],
            final_note=case["final_note"],
            deidentified_confirmed=True,
        )
        print(f"Seeded: {case['label']} (total examples now: {total})")
    print(f"\nDone. {total} total training examples in data/training_examples.jsonl")


if __name__ == "__main__":
    main()
