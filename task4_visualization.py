"""
TrendPulse - Task 4: Visualisations
Loads the analysed CSV and produces 3 charts plus a combined dashboard.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

DATA_FILE = os.path.join("data", "trends_analysed.csv")
OUTPUT_DIR = "outputs"


def shorten(title, max_len=50):
    """Shorten a title to max_len characters, adding '...' if truncated."""
    return title if len(title) <= max_len else title[: max_len - 3] + "..."


def setup():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = pd.read_csv(DATA_FILE)
    return df


def chart1_top_stories(df):
    """Horizontal bar chart of the top 10 stories by score."""
    top10 = df.sort_values("score", ascending=False).head(10)
    labels = [shorten(t) for t in top10["title"]]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(labels[::-1], top10["score"][::-1], color="steelblue")
    ax.set_title("Top 10 Stories by Score")
    ax.set_xlabel("Score")
    ax.set_ylabel("Story Title")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "chart1_top_stories.png"))
    plt.close(fig)


def chart2_categories(df):
    """Bar chart of story counts per category."""
    counts = df["category"].value_counts()
    colors = plt.cm.Set2.colors[: len(counts)]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(counts.index, counts.values, color=colors)
    ax.set_title("Stories per Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Number of Stories")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "chart2_categories.png"))
    plt.close(fig)


def chart3_scatter(df):
    """Scatter plot of score vs num_comments, coloured by is_popular."""
    fig, ax = plt.subplots(figsize=(8, 6))

    popular = df[df["is_popular"] == True]
    not_popular = df[df["is_popular"] == False]

    ax.scatter(not_popular["score"], not_popular["num_comments"],
               color="gray", label="Not Popular", alpha=0.6)
    ax.scatter(popular["score"], popular["num_comments"],
               color="crimson", label="Popular", alpha=0.6)

    ax.set_title("Score vs Comments")
    ax.set_xlabel("Score")
    ax.set_ylabel("Number of Comments")
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "chart3_scatter.png"))
    plt.close(fig)


def dashboard(df):
    """Combine all 3 charts into a single dashboard figure."""
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))

    # Panel 1: top 10 stories
    top10 = df.sort_values("score", ascending=False).head(10)
    labels = [shorten(t, 30) for t in top10["title"]]
    axes[0].barh(labels[::-1], top10["score"][::-1], color="steelblue")
    axes[0].set_title("Top 10 Stories by Score")
    axes[0].set_xlabel("Score")

    # Panel 2: stories per category
    counts = df["category"].value_counts()
    colors = plt.cm.Set2.colors[: len(counts)]
    axes[1].bar(counts.index, counts.values, color=colors)
    axes[1].set_title("Stories per Category")
    axes[1].tick_params(axis="x", rotation=45)

    # Panel 3: scatter
    popular = df[df["is_popular"] == True]
    not_popular = df[df["is_popular"] == False]
    axes[2].scatter(not_popular["score"], not_popular["num_comments"],
                     color="gray", label="Not Popular", alpha=0.6)
    axes[2].scatter(popular["score"], popular["num_comments"],
                     color="crimson", label="Popular", alpha=0.6)
    axes[2].set_title("Score vs Comments")
    axes[2].legend()

    fig.suptitle("TrendPulse Dashboard", fontsize=16, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "dashboard.png"))
    plt.close(fig)


if __name__ == "__main__":
    df = setup()
    chart1_top_stories(df)
    chart2_categories(df)
    chart3_scatter(df)
    dashboard(df)
    print("All charts saved to outputs/")
