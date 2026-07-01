import argparse
import time
import pandas as pd
from docx import Document

from src.final_ranker import rank_candidates
from src.explainer import generate_reason


def read_docx(path):
    """Read Job Description from DOCX."""
    doc = Document(path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text


def validate_submission(df):
    """Validate submission according to Redrob specification."""

    required_columns = [
        "candidate_id",
        "rank",
        "score",
        "reasoning"
    ]

    # Correct columns
    assert list(df.columns) == required_columns, \
        "Invalid column order."

    # Exactly 100 rows
    assert len(df) == 100, \
        f"Submission has {len(df)} rows. Expected 100."

    # Unique candidate ids
    assert df["candidate_id"].is_unique, \
        "Duplicate candidate IDs found."

    # Rank 1-100
    assert list(df["rank"]) == list(range(1, 101)), \
        "Ranks must be exactly 1-100."

    # Scores must decrease
    scores = df["score"].tolist()

    for i in range(len(scores) - 1):
        assert scores[i] >= scores[i + 1], \
            "Scores are not monotonically decreasing."

    print("Submission validation passed.")


def main():

    parser = argparse.ArgumentParser(
        description="Generate Redrob Submission CSV"
    )

    parser.add_argument(
        "--jd",
        required=True,
        help="Path to Job Description (.docx)"
    )

    parser.add_argument(
        "--out",
        default="submission.csv",
        help="Output CSV"
    )

    args = parser.parse_args()

    start = time.time()

    print("=" * 60)
    print("Recruiter AI Submission Generator")
    print("=" * 60)

    print("\nReading Job Description...")
    jd = read_docx(args.jd)

    print("Ranking Candidates...")

    # IMPORTANT:
    # rank_candidates should return the Top-100 candidates.
    results = rank_candidates(
        jd_text=jd,
        top_k=100
    )

    print(f"Top {len(results)} candidates selected.")

    rows = []

    for candidate in results:

        reason = generate_reason(candidate)

        rows.append({

            "candidate_id": candidate["candidate_id"],

            "score": float(candidate["final"]),

            "reasoning": reason

        })

    submission = pd.DataFrame(rows)

    # Sort deterministically
    submission = submission.sort_values(
        by=["score", "candidate_id"],
        ascending=[False, True]
    ).reset_index(drop=True)

    # Assign ranks
    submission["rank"] = submission.index + 1

    # Correct column order
    submission = submission[
        [
            "candidate_id",
            "rank",
            "score",
            "reasoning"
        ]
    ]

    # Round scores AFTER sorting
    submission["score"] = submission["score"].round(6)

    # Validate
    validate_submission(submission)

    # Save
    submission.to_csv(
        args.out,
        index=False,
        encoding="utf-8"
    )

    elapsed = time.time() - start

    print("\nSubmission saved successfully!")
    print(f"Output File : {args.out}")
    print(f"Candidates  : {len(submission)}")
    print(f"Time Taken  : {elapsed:.2f} seconds")


if __name__ == "__main__":
    main()