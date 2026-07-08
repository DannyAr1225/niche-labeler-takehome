import json
import re
from collections import Counter


STOPWORDS = {
    "the", "and", "for", "you", "your", "with", "this", "that", "are", "was",
    "but", "not", "have", "has", "had", "from", "they", "them", "our", "out",
    "get", "got", "can", "all", "just", "like", "about", "into", "what",
    "when", "how", "why", "who", "will", "would", "could", "should", "a",
    "an", "to", "of", "in", "on", "is", "it", "as", "at", "be", "by", "or",
    "if", "so", "we", "i", "me", "my", "he", "she", "her", "his", "their",
    "there", "here", "than", "then", "too", "very", "more", "most", "much",
    "been", "were", "am", "do", "does", "did", "done", "up", "down", "new",
}


def tokenize(text):
    """
    Split text into useful lowercase tokens for keyword extraction.
    """
    raw_words = re.findall(r"[a-z][a-z']+", str(text).lower())

    # Remove short words and common filler words.
    return [
        word
        for word in raw_words
        if len(word) > 2 and word not in STOPWORDS
    ]


def get_top_keywords(topic_posts, top_n=8):
    """
    Return the most frequent meaningful words in a topic cluster.
    """
    word_counts = Counter()

    for caption in topic_posts["clean_caption"]:
        word_counts.update(tokenize(caption))

    return [word for word, _ in word_counts.most_common(top_n)]


def infer_topic_name(keywords):
    """
    Create an initial readable topic name from cluster keywords.
    """
    keyword_text = " ".join(keywords)

    topic_rules = [
        (
            ["skin", "skincare", "spf", "cleanser", "serum", "moisturizer", "retinol", "acne"],
            "Skincare routines and education",
        ),
        (
            ["makeup", "foundation", "concealer", "blush", "mascara", "lip", "grwm"],
            "Makeup routines and product application",
        ),
        (
            ["hair", "shampoo", "conditioner", "curl", "scalp", "blowout"],
            "Haircare and styling",
        ),
        (
            ["workout", "fitness", "gym", "protein", "pilates", "wellness"],
            "Fitness and wellness lifestyle",
        ),
        (
            ["outfit", "style", "fashion", "dress", "wear", "closet"],
            "Fashion and outfit styling",
        ),
        (
            ["morning", "night", "routine", "daily", "day", "week"],
            "Daily routines and lifestyle",
        ),
        (
            ["product", "review", "favorite", "must", "try", "recommend"],
            "Product recommendations and reviews",
        ),
    ]

    for trigger_words, topic_name in topic_rules:
        if any(word in keyword_text for word in trigger_words):
            return topic_name

    if keywords:
        return f"Content about {', '.join(keywords[:3])}"

    return "General lifestyle content"


def infer_topic_description(name, keywords):
    """
    Write a short topic description using the top cluster keywords.
    """
    if not keywords:
        return f"Posts focused on {name.lower()}."

    keyword_summary = ", ".join(keywords[:5])
    return f"Posts focused on {name.lower()}, commonly mentioning {keyword_summary}."


def get_representative_posts(posts, embeddings, topic_id, n=3):
    """
    Select example posts that help explain a topic cluster.
    """
    topic_posts = posts.loc[posts["topic_id"] == topic_id].copy()

    if topic_posts.empty:
        return []

    # For this simple pipeline, high-engagement posts serve as readable examples.
    if "like_count" in topic_posts.columns:
        topic_posts["like_count"] = topic_posts["like_count"].fillna(0)
        topic_posts = topic_posts.sort_values("like_count", ascending=False)

    representative_posts = []
    keywords = get_top_keywords(topic_posts, top_n=5)

    for _, post in topic_posts.head(n).iterrows():
        caption = str(post["caption"])
        snippet = caption[:220] + "..." if len(caption) > 220 else caption

        representative_posts.append(
            {
                "post_id": post["post_id"],
                "caption_snippet": snippet,
                "why": (
                    "This post is representative because it uses key terms "
                    f"from the cluster such as {', '.join(keywords[:4])}."
                ),
            }
        )

    return representative_posts


def build_topics_json(posts, embeddings, output_path="outputs/topics.json"):
    """
    Build the topics.json deliverable.
    """
    topics = []

    for topic_id in sorted(posts["topic_id"].unique()):
        topic_posts = posts.loc[posts["topic_id"] == topic_id]

        top_keywords = get_top_keywords(topic_posts)
        topic_name = infer_topic_name(top_keywords)
        topic_description = infer_topic_description(topic_name, top_keywords)

        topics.append(
            {
                "topic_id": int(topic_id),
                "name": topic_name,
                "description": topic_description,
                "post_count": int(len(topic_posts)),
                "top_keywords": top_keywords,
                "representative_posts": get_representative_posts(
                    posts=posts,
                    embeddings=embeddings,
                    topic_id=topic_id,
                    n=3,
                ),
            }
        )

    with open(output_path, "w", encoding="utf-8") as output_file:
        json.dump(topics, output_file, indent=2, ensure_ascii=False)

    return topics