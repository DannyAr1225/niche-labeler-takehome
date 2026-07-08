import pandas as pd


def normalize_text(text):
    """
    Convert missing values to empty strings and lowercase everything else.
    """
    if pd.isna(text):
        return ""
    return str(text).lower()


def count_keyword_matches(text, keywords):
    """
    Count how many keywords appear in a text block.
    """
    normalized_text = normalize_text(text)
    match_count = 0

    for keyword in keywords:
        normalized_keyword = normalize_text(keyword)
        if normalized_keyword and normalized_keyword in normalized_text:
            match_count += 1

    return match_count


def get_primary_topic(group):
    """
    Return the most common topic_id for one creator.
    """
    if group.empty:
        return None

    return int(group["topic_id"].mode().iloc[0])


def build_creator_text(group):
    """
    Combine all captions from one creator into one searchable text block.
    """
    creator_captions = group["clean_caption"].fillna("").tolist()
    return " ".join(creator_captions)


def score_creators(
    posts,
    creators,
    target_niche,
    topics,
    output_path="outputs/creator_niche_scores.csv",
):
    """
    Score each creator using keyword alignment with the target niche.
    """
    on_niche_keywords = (
        target_niche.get("core_keywords", [])
        or target_niche.get("on_niche_keywords", [])
        or []
    )
    off_niche_keywords = target_niche.get("off_niche_keywords", []) or []

    # Map topic IDs to readable topic names for the output notes
    topic_names = {
        int(topic["topic_id"]): topic["name"]
        for topic in topics
    }

    score_rows = []

    for creator_handle, creator_posts in posts.groupby("creator_handle"):
        creator_text = build_creator_text(creator_posts)

        on_match_count = count_keyword_matches(creator_text, on_niche_keywords)
        off_match_count = count_keyword_matches(creator_text, off_niche_keywords)

        aligned_posts = 0
        off_niche_posts = 0

        # Count posts that contain at least one positive or negative niche signal
        for _, post in creator_posts.iterrows():
            caption = normalize_text(post["clean_caption"])

            if count_keyword_matches(caption, on_niche_keywords) > 0:
                aligned_posts += 1

            if count_keyword_matches(caption, off_niche_keywords) > 0:
                off_niche_posts += 1

        post_count = len(creator_posts)
        aligned_ratio = aligned_posts / post_count
        off_niche_ratio = off_niche_posts / post_count

        # Reward coverage of target keywords, capped after eight matches
        keyword_score = min(1.0, on_match_count / 8)

        # Penalize off-niche language without letting the penalty dominate
        penalty = min(0.40, off_match_count * 0.05 + off_niche_ratio * 0.20)

        final_score = (
            0.55 * keyword_score
            + 0.45 * aligned_ratio
            - penalty
        )
        final_score = max(0, min(1, final_score))

        primary_topic_id = get_primary_topic(creator_posts)
        primary_topic = topic_names.get(primary_topic_id, f"Topic {primary_topic_id}")

        if final_score >= 0.60:
            fit_label = "high"
        elif final_score >= 0.30:
            fit_label = "medium"
        else:
            fit_label = "low"

        notes = (
            f"{fit_label.capitalize()} fit. Creator has {post_count} posts. "
            f"Dominant topic: '{primary_topic}'. "
            f"Matched {on_match_count} on-niche keywords and "
            f"{off_match_count} off-niche keywords. "
            f"{aligned_posts}/{post_count} posts directly matched the target skincare niche."
        )

        score_rows.append(
            {
                "creator_handle": creator_handle,
                "niche_fit_score": round(final_score, 3),
                "fit_label": fit_label,
                "primary_topic": primary_topic,
                "post_count": post_count,
                "on_niche_keyword_matches": on_match_count,
                "off_niche_keyword_matches": off_match_count,
                "aligned_post_ratio": round(aligned_ratio, 3),
                "off_niche_post_ratio": round(off_niche_ratio, 3),
                "notes": notes,
            }
        )

    scores = pd.DataFrame(score_rows)

    # Bring in optional creator metadata when available
    if creators is not None and not creators.empty and "creator_handle" in creators.columns:
        scores = scores.merge(creators, on="creator_handle", how="left")

    scores = scores.sort_values("niche_fit_score", ascending=False)
    scores.to_csv(output_path, index=False)

    return scores