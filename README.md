# Niche Labeler Take-home

This project builds a simple topic and niche labeling pipeline for social media creator posts.

Given creator posts from `data/posts.csv`, creator metadata from `data/creators.csv`, and a target niche definition from `data/target_niche.json`, the pipeline:

1. Cleans and preprocesses post captions.
2. Converts cleaned captions into TF-IDF text vectors.
3. Clusters posts into 5–10 coherent topics using KMeans.
4. Labels each topic with a short name, description, top keywords, and representative posts.
5. Scores each creator based on how well their content fits the target niche.
6. Writes reproducible outputs to the `outputs/` folder.

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Pipeline

From the project root, run:

```bash
PYTHONPATH=src python src/main.py
```

This will generate or update the output files in the `outputs/` folder.

## Outputs

The pipeline creates:

- `outputs/topics.json`: topic names, descriptions, top keywords, post counts, and representative posts.
- `outputs/creator_niche_scores.csv`: creator-level niche fit scores and labels.
- `outputs/labeled_posts.csv`: original posts with assigned topic IDs.
- `outputs/report.md`: short explanation of the method, topic quality, scoring approach, limitations, and next steps.

## Method

The pipeline uses a lightweight and reproducible approach. Captions are cleaned by lowercasing text, removing URLs, removing mentions, normalizing hashtags, removing punctuation, and trimming extra whitespace.

Cleaned captions are then converted into TF-IDF vectors. KMeans clustering groups posts into topics, and silhouette score is used to choose a topic count between 5 and 10.

For creator scoring, the pipeline compares each creator’s captions against the target niche definition. It rewards matches with on-niche skincare education keywords and penalizes off-niche content such as unrelated lifestyle, fashion haul, crypto, or giveaway content.

## Manual Review

The pipeline generates initial topic labels automatically, but the final `outputs/topics.json` was manually reviewed to improve topic names, descriptions, and representative post explanations. This manual review helps make the final topics more interpretable for a marketing use case.

## Limitations

This project only uses caption text, so it may miss important visual details from images or videos. KMeans also assigns every post to one topic, even when a post could reasonably belong to multiple themes. With more time, I would add multi-label topic assignment, use creator bios more directly, and incorporate image or video understanding.