"""
TrendPulse - Task 2: Clean the Data & Save as CSV
Loads the raw JSON from Task 1, cleans it with Pandas, and saves a tidy CSV.
"""

import pandas as pd
import glob
import os

DATA_DIR = "data"


def find_latest_json():
    """Find the most recent trends_*.json file in the data folder."""
    files = sorted(glob.glob(os.path.join(DATA_DIR, "trends_*.json")))
    if not files:
        raise FileNotFoundError("No trends_*.json file found in data/. Run Task 1 first.")
    return files[-1]


def load_data(filepath):
    """Load the JSON file into a DataFrame."""
    df = pd.read_json(filepath)
    print(f"Loaded {len(df)} stories from {filepath}")
    return df


def clean_data(df):
    """Remove duplicates, nulls, bad types, low-quality rows, and whitespace."""

    # Remove duplicate stories (same post_id)
    df = df.drop_duplicates(subset="post_id")

    # Drop rows missing essential fields
    df = df.dropna(subset=["post_id", "title", "score"])

    # Make sure score and num_comments are integers
    df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0).astype(int)
    df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce").fillna(0).astype(int)

    print(f"After removing duplicates: {len(df)}")

    # Drop nulls again after type coercion (any that failed to convert cleanly)
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")

    # Strip extra whitespace from titles
    df["title"] = df["title"].astype(str).str.strip()

    # Remove low-quality stories (score < 5)
    df = df[df["score"] >= 5]
    print(f"After removing low scores: {len(df)}")

    return df.reset_index(drop=True)


def save_clean_csv(df):
    """Save cleaned DataFrame to CSV and print a summary."""
    out_path = os.path.join(DATA_DIR, "trends_clean.csv")
    df.to_csv(out_path, index=False)
    print(f"\nSaved {len(df)} rows to {out_path}")

    print("\nStories per category:")
    print(df["category"].value_counts().to_string())

    return out_path


if __name__ == "__main__":
    input_file = find_latest_json()
    df = load_data(input_file)
    df_clean = clean_data(df)
    save_clean_csv(df_clean)
