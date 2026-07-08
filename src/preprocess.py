import json
import re

import pandas as pd


def clean_text(text):
    """
    Normalize a social caption before vectorization.
    """
    if pd.isna(text):
        return ""

    cleaned = str(text).lower()

    # Remove links and user mentions because they add noise to topic labels.
    cleaned = re.sub(r"http\S+|www\.\S+", " ", cleaned)
    cleaned = re.sub(r"@\w+", " ", cleaned)

    # Keep hashtag words but remove the symbol, e.g. #skincare -> skincare.
    cleaned = cleaned.replace("#", "")

    # Keep letters, numbers, spaces, and apostrophes.
    cleaned = re.sub(r"[^a-z0-9\s']", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned


def load_posts(path="data/posts.csv"):
    """
    Load posts and add a clean_caption column used by the pipeline.
    """
    posts = pd.read_csv(path)

    required_columns = {"post_id", "creator_handle", "caption"}
    missing_columns = sorted(required_columns - set(posts.columns))
    if missing_columns:
        raise ValueError(f"posts.csv is missing required columns: {missing_columns}")

    posts["caption"] = posts["caption"].fillna("")
    posts["clean_caption"] = posts["caption"].apply(clean_text)

    return posts


def load_creators(path="data/creators.csv"):
    """
    Load optional creator metadata.
    """
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        # The project can still run if creator metadata is unavailable.
        return pd.DataFrame()


def load_target_niche(path="data/target_niche.json"):
    """
    Load the target niche definition from JSON.
    """
    with open(path, "r", encoding="utf-8") as input_file:
        return json.load(input_file)


def target_niche_to_text(target_niche):
    """
    Flatten a nested niche JSON into one lowercase text string.
    """
    values = []

    def collect_values(item):
        if isinstance(item, dict):
            for nested_value in item.values():
                collect_values(nested_value)
        elif isinstance(item, list):
            for nested_item in item:
                collect_values(nested_item)
        else:
            values.append(str(item))

    collect_values(target_niche)
    return " ".join(values).lower()