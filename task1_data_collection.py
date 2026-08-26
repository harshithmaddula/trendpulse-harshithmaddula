"""
TrendPulse - Task 1: Fetch Data from HackerNews API
Fetches top stories from HackerNews, categorises them by keyword matching,
and saves up to 25 stories per category (125 total) to a JSON file.
"""

import requests
import time
import json
import os
from datetime import datetime

# --- Configuration ---

HEADERS = {"User-Agent": "TrendPulse/1.0"}
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

STORIES_PER_CATEGORY = 25
NUM_IDS_TO_FETCH = 500

# Keywords used to assign each story to a category (case-insensitive match)
CATEGORY_KEYWORDS = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"],
}


def get_top_story_ids(limit=NUM_IDS_TO_FETCH):
    """Fetch the list of top story IDs from HackerNews."""
    try:
        response = requests.get(TOP_STORIES_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()[:limit]
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch top story IDs: {e}")
        return []


def get_story_details(story_id):
    """Fetch a single story's details by ID. Returns None on failure."""
    try:
        url = ITEM_URL.format(story_id)
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch story {story_id}: {e}")
        return None


def categorise(title):
    """Return the first category whose keywords appear in the title (case-insensitive)."""
    if not title:
        return None
    title_lower = title.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in title_lower:
                return category
    return None


def collect_stories():
    """Main collection loop: fetch stories and bucket them by category."""
    story_ids = get_top_story_ids()
    if not story_ids:
        print("No story IDs retrieved. Exiting.")
        return []

    collected = {cat: [] for cat in CATEGORY_KEYWORDS}
    all_stories = []

    # Loop through categories one at a time, sleeping once per category
    for category in CATEGORY_KEYWORDS:
        for story_id in story_ids:
            if len(collected[category]) >= STORIES_PER_CATEGORY:
                break  # this category is full, move to the next one

            details = get_story_details(story_id)
            if details is None:
                continue  # request failed, skip and move on

            title = details.get("title", "")
            assigned_category = categorise(title)

            if assigned_category == category:
                story_record = {
                    "post_id": details.get("id"),
                    "title": title,
                    "category": category,
                    "score": details.get("score", 0),
                    "num_comments": details.get("descendants", 0),
                    "author": details.get("by", "unknown"),
                    "collected_at": datetime.now().isoformat(),
                }
                collected[category].append(story_record)
                all_stories.append(story_record)

        # Wait 2 seconds once per category loop (not per story)
        time.sleep(2)

    return all_stories


def save_to_json(stories):
    """Save the collected stories to data/trends_YYYYMMDD.json."""
    os.makedirs("data", exist_ok=True)
    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(stories, f, indent=2, ensure_ascii=False)

    print(f"Collected {len(stories)} stories. Saved to {filename}")
    return filename


if __name__ == "__main__":
    stories = collect_stories()
    save_to_json(stories)
