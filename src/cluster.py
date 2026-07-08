from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score


RANDOM_STATE = 42


def embed_texts(captions):
    """
    Turn cleaned captions into TF-IDF feature vectors.
    """
    # Include single words and short phrases while keeping the feature space small
    tfidf = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=1000,
    )

    caption_vectors = tfidf.fit_transform(captions)
    return caption_vectors, tfidf


def choose_num_topics(vectors, min_topics=5, max_topics=10):
    """
    Pick the best KMeans topic count using silhouette score.
    """
    post_count = vectors.shape[0]

    # KMeans needs fewer clusters than data points
    if post_count <= min_topics:
        return max(2, post_count)

    best_topic_count = min_topics
    best_silhouette = -1
    largest_valid_k = min(max_topics, post_count - 1)

    for topic_count in range(min_topics, largest_valid_k + 1):
        try:
            candidate_model = KMeans(
                n_clusters=topic_count,
                random_state=RANDOM_STATE,
                n_init=10,
            )
            candidate_labels = candidate_model.fit_predict(vectors)
            candidate_score = silhouette_score(vectors, candidate_labels)

            if candidate_score > best_silhouette:
                best_silhouette = candidate_score
                best_topic_count = topic_count
        except Exception:
            # Skip invalid cluster counts or edge cases in silhouette scoring
            continue

    return best_topic_count


def cluster_posts(posts, vectors, num_topics=None):
    """
    Assign each post to a KMeans topic cluster.
    """
    selected_topics = num_topics or choose_num_topics(vectors)

    clusterer = KMeans(
        n_clusters=selected_topics,
        random_state=RANDOM_STATE,
        n_init=10,
    )

    posts = posts.copy()
    posts["topic_id"] = clusterer.fit_predict(vectors)

    return posts, clusterer, selected_topics
