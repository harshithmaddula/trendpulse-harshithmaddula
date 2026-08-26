"""
TrendPulse - Task 3: Analysis with Pandas & NumPy
Loads the clean CSV, computes statistics with NumPy, adds engagement columns,
and saves the result for Task 4.
"""

import pandas as pd
import numpy as np
import os

DATA_DIR = "data"
INPUT_FILE = os.path.join(DATA_DIR, "trends_clean.csv")
OUTPUT_FILE = os.path.join(DATA_DIR, "trends_analysed.csv")


def load_and_explore():
    """Load the clean CSV and print a quick overview."""
    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded data: {df.shape}\n")

    print("First 5 rows:")
    print(df.head(), "\n")

    print(f"Average score   : {df['score'].mean():,.0f}")
    print(f"Average comments: {df['num_comments'].mean():,.0f}")

    return df


def numpy_stats(df):
    """Compute and print core statistics using NumPy."""
    scores = df["score"].to_numpy()

    mean_score = np.mean(scores)
    median_score = np.median(scores)
    std_score = np.std(scores)
    max_score = np.max(scores)
    min_score = np.min(scores)

    print("\n--- NumPy Stats ---")
    print(f"Mean score   : {mean_score:,.0f}")
    print(f"Median score : {median_score:,.0f}")
    print(f"Std deviation: {std_score:,.0f}")
    print(f"Max score    : {max_score:,.0f}")
    print(f"Min score    : {min_score:,.0f}")

    # Category with the most stories
    top_category = df["category"].value_counts().idxmax()
    top_category_count = df["category"].value_counts().max()
    print(f"\nMost stories in: {top_category} ({top_category_count} stories)")

    # Story with the most comments
    top_story = df.loc[df["num_comments"].idxmax()]
    print(f'\nMost commented story: "{top_story["title"]}" — {top_story["num_comments"]:,} comments')

    return mean_score


def add_new_columns(df, mean_score):
    """Add engagement and is_popular columns."""
    df["engagement"] = df["num_comments"] / (df["score"] + 1)
    df["is_popular"] = df["score"] > mean_score
    return df


def save_result(df):
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved to {OUTPUT_FILE}")


if __name__ == "__main__":
    df = load_and_explore()
    mean_score = numpy_stats(df)
    df = add_new_columns(df, mean_score)
    save_result(df)
