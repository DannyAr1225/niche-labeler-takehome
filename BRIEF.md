# Chimeboard Take-home project: Topic & niche labeler
 
**Time expectation:** 6–10 hours (designed to fit within one calendar week alongside other commitments)  
**Submission:** GitHub repository (public or private link shared with us) + short demo video or live walkthrough (optional but appreciated)

---

## Context

Chimeboard helps brands find and evaluate social media creators for marketing campaigns. A core part of that workflow is understanding what creators actually talk about — not just who they are, but whether their content clusters into themes that match a brand’s niche (e.g. “clinical skincare education” vs. “GRWM makeup” vs. “fitness lifestyle”).

Your task is to build a topic and niche labeling pipeline on a provided dataset of creator posts. You will group posts into themes, name those themes, and assess how well each creator fits a target niche.

This project is standalone, so you won't need access to Chimeboard code, accounts, or infrastructure.

---

## Objective

Given a CSV of social posts from beauty and lifestyle creators:

1. **Discover topics** — cluster or otherwise group posts into a small set of coherent themes (target: 5–10 topics).
2. **Label topics** — assign each theme a short human-readable name and one-sentence description.
3. **Show evidence** — for each topic, surface 3 representative posts that best exemplify the theme.
4. **Niche fit** — score each creator on how well they fit a provided target niche (see `data/target_niche.json`).
5. **Document your approach** — explain choices, limitations, and what you would improve with more time.

We care more about clear thinking, reproducible code, and honest evaluation than about squeezing out the last point of clustering accuracy.

---

## Provided materials

| File | Description |
|------|-------------|
| `data/posts.csv` | ~200 posts with `post_id`, `creator_handle`, `platform`, `caption`, `like_count`, `posted_at` |
| `data/target_niche.json` | Brand niche definition used for creator-level fit scoring |
| `data/creators.csv` | Creator metadata (handle, follower_count, bio) — optional context |

You may use only this data (no live scraping required). You may augment with standard open-source libraries and public embedding models.

---

## Deliverables

### 1. Code repository

Include at minimum:

- README.md with setup instructions (Python version, `pip install` or `uv` / `poetry` commands).
- A runnable entrypoint (e.g. `python -m src.run` or `jupyter notebook`) that produces outputs from `data/posts.csv`.
- Reproducibility: fixed random seed where applicable; pin key dependency versions in `requirements.txt` or `pyproject.toml`.

Suggested structure (you may adapt):

```
topic-labeler/
├── README.md
├── requirements.txt
├── data/              # copy or symlink provided files
├── src/
│   ├── preprocess.py
│   ├── cluster.py
│   ├── label_topics.py
│   └── score_creators.py
├── outputs/
│   ├── topics.json
│   ├── creator_niche_scores.csv
│   └── report.md
└── notebooks/         # optional
```

### 2. `outputs/topics.json`

JSON array of topics. Example shape:

```json
[
  {
    "topic_id": 0,
    "name": "Routine-focused skincare",
    "description": "Posts about AM/PM routines, product layering, and gentle actives.",
    "post_count": 42,
    "representative_posts": [
      { "post_id": "p_001", "caption_snippet": "...", "why": "Mentions double cleanse and SPF daily" }
    ]
  }
]
```

### 3. `outputs/creator_niche_scores.csv`

One row per creator. Columns at minimum:

| Column | Description |
|--------|-------------|
| `creator_handle` | Creator identifier |
| `niche_fit_score` | Float 0–1 (your definition; document it) |
| `primary_topic` | Dominant topic for this creator |
| `notes` | Brief human-readable justification (1–2 sentences) |

### 4. `outputs/report.md` (1–2 pages)

Answer:

- **Method:** preprocessing, embedding/clustering approach, number of topics chosen and why.
- **Topic quality:** do the themes make sense? Show 1–2 examples of good clusters and 1 failure mode.
- **Niche scoring:** how you mapped topics/posts to the target niche in `target_niche.json`.
- **Limitations:** what would break at 10× or 100× scale?
- **Next steps:** what you would do with one more week (bullet list).

### Out of scope (please do not spend time on)

- Live Instagram / TikTok scraping.
- Training large language models from scratch.
- Production deployment, auth, or databases.


We do not expect perfection. We want to see how you reason about messy text data. Please feel free to ask any follow up questions; the spec is intentionally somewhat ambiguous.

---

## Submission instructions

1. Push code to GitHub (or GitLab). If private, grant access to: *adaeze@chimeboard.com*.
2. Email us:
   - Repository link
   - Walkthough or written description of choices / tradeoffs (fine as a markdown link in the repository)
