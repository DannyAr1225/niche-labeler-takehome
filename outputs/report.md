# Topic and Niche Labeling Report

## Method

I built a lightweight topic labeling pipeline for the provided creator post dataset. First, I cleaned each caption by lowercasing text, removing URLs, removing mentions, normalizing hashtags, removing punctuation, and removing extra whitespace. I then converted each cleaned caption into TF-IDF text vectors. These vectors were clustered with KMeans.

I selected the number of topics automatically within the requested 5–10 topic range using silhouette score, which resulted in 10 topics. The goal was not perfect clustering, but a readable and reproducible set of themes that could explain what creators commonly post about.

After generating the initial clusters, I manually reviewed `topics.json` and renamed the topics to make them more specific and business-relevant. I also rewrote the representative post explanations so they describe why each example fits the topic rather than only repeating the cluster keywords.

## Topic Quality

The strongest target-aligned topics were:

- **SPF and melasma-focused morning routines**: Posts about sunscreen, melasma-prone skin, and morning routines where SPF is treated as the most important daily skincare step.
- **Double cleansing and sunscreen removal**: Posts demonstrating oil cleansers, gentle gel cleansers, and sunscreen removal routines.
- **Ingredient education: ceramides and niacinamide**: Posts explaining skincare ingredients and how they support barrier repair and product decision-making.
- **Moisturizer and skin barrier basics**: Posts explaining moisturizer, serum layering, and skin barrier fundamentals in beginner-friendly language.

The clearest off-niche topics were:

- **Beauty hauls and product unboxings**: Sephora hauls, product launches, PR packages, and beauty shopping content.
- **Fitness, marathon, and crypto-adjacent lifestyle**: Running vlogs, marathon training, and some crypto-related lifestyle language.
- **Home reset and everyday lifestyle content**: Cleaning, groceries, laundry, weekly planning, and apartment reset posts.

A strong cluster example is **SPF and melasma-focused morning routines**, where representative posts repeatedly describe SPF as “step zero” for melasma-prone skin. This theme is highly aligned with the target niche because sunscreen education is one of the target brand’s core interests.

One weaker cluster is **Beauty and lifestyle crossover content**. It contains posts that use skincare or beauty hashtags, but the actual content is often broader lifestyle or makeup styling. I treated this as a lower-confidence cluster because hashtags alone do not always indicate strong niche alignment.

## Niche Scoring

For niche fit, I used the target niche JSON directly. I treated `core_keywords` or `on_niche_keywords` as positive niche signals and `off_niche_keywords` as negative niche signals. The score is my own documented definition of creator fit, as required by the deliverable instructions.

For each creator, I combined all of their cleaned captions into one text block and counted how many on-niche and off-niche keywords appeared in that text. I also checked each individual post to calculate two ratios:

- `aligned_post_ratio`: the share of the creator’s posts that contained at least one on-niche keyword.
- `off_niche_post_ratio`: the share of the creator’s posts that contained at least one off-niche keyword.

I then calculated a keyword score:

```bash
keyword_score = min(1.0, on_niche_keyword_matches / 8)
```

This rewards creators for matching more target skincare keywords, while capping the keyword score at 1.0 after 8 matches.

I calculated an off-niche penalty:

```bash
penalty = min(0.40, off_niche_keyword_matches * 0.05 + off_niche_post_ratio * 0.20)
```

This lowers the score for creators who repeatedly mention off-niche content such as giveaways, crypto, fashion hauls, or unrelated lifestyle content. The penalty is capped at 0.40 so that off-niche content matters without completely dominating the score.

The final niche fit score is:

```bash
niche_fit_score = 0.55 * keyword_score + 0.45 * aligned_post_ratio - penalty
```

I then clipped the result to stay between 0 and 1. This means the final score combines three signals: how many target niche keywords the creator matches, what share of their posts directly align with the niche, and how much off-niche content appears in their captions.

Fit labels are assigned using these thresholds:

```bash
high fit:   niche_fit_score >= 0.60
medium fit: niche_fit_score >= 0.30 and < 0.60
low fit:    niche_fit_score < 0.30
```

The strongest creators are listed at the top of `creator_niche_scores.csv`, along with their niche fit score, fit label, primary topic, post count, keyword match counts, post ratios, and explanation notes.

## Limitations

This approach is limited by the small dataset size and by the fact that captions alone do not fully describe visual social media content. Many social posts rely on images or videos, so some content themes may be missed when only caption text is available.

KMeans also forces every post into exactly one cluster, even if a post could belong to multiple themes. For example, a post about a morning skincare routine could also mention SPF, moisturizer, and product recommendations. A multi-label approach would better capture that overlap.

Some captions are repeated across different creators or posts, so a few representative examples are textually similar even when they have different post IDs. This makes the clustering look repetitive in places, but it also reflects the structure of the provided dataset.

At 10x or 100x scale, the current approach would start to feel limited because the pipeline recomputes vectors and clusters in a simple local workflow. Larger datasets would need more efficient storage for text vectors, better evaluation of topic quality, and stronger monitoring for repeated or low-quality captions.

## Next Steps

- Manually review and refine topic names after inspecting representative posts.
- Add multi-label topic assignment so posts can belong to more than one theme.
- Use creator bios and follower counts more directly in niche scoring.
- Add image/video understanding if visual content becomes available.
- Add stronger evaluation for topic quality, such as cluster coherence or human review scores.
- At 10x or 100x scale, store TF-IDF vectors, embeddings, and cluster results in a more efficient database or vector index.