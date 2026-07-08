import os

from preprocess import (
    load_posts,
    load_creators,
    load_target_niche,
)
from cluster import embed_texts, cluster_posts
from label_topics import build_topics_json
from score_creators import score_creators

def main():
    os.makedirs("outputs", exist_ok=True)

    print("Loading data...")
    posts = load_posts("data/posts.csv")
    creators = load_creators("data/creators.csv")
    target_niche = load_target_niche("data/target_niche.json")

    print("Embedding posts...")
    embeddings, vectorizer = embed_texts(posts["clean_caption"].tolist())

    print("Clustering posts...")
    posts, cluster_model, num_topics = cluster_posts(posts, embeddings)

    print(f"Selected {num_topics} topics.")

    print("Saving labeled posts...")
    posts.to_csv("outputs/labeled_posts.csv", index=False)

    print("Building topics.json...")
    topics = build_topics_json(
        posts=posts,
        embeddings=embeddings,
        output_path="outputs/topics.json"
    )

    print("Scoring creators...")
    scores = score_creators(
        posts=posts,
        creators=creators,
        target_niche=target_niche,
        topics=topics,
        output_path="outputs/creator_niche_scores.csv"
    )

    print("Done.")
    print("Created:")
    print("- outputs/labeled_posts.csv")
    print("- outputs/topics.json")
    print("- outputs/creator_niche_scores.csv")
    print("Manual deliverable: outputs/report.md")


if __name__ == "__main__":
    main()