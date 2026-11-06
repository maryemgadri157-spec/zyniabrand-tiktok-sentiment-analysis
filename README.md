# Zynia TikTok Sentiment Analysis

A multilingual sentiment and theme analysis of consumer feedback on Zynia, a Tunisian beauty and skincare brand. Built as an unsolicited analytical pitch, surfacing actionable commercial insights from 283 unstructured customer comments across four languages.

## Problem

Zynia Botanicals is a growing Tunisian beauty brand with an active TikTok presence but no structured customer feedback loop. Comments on their videos contained rich signals about product perception, pricing concerns, and distribution gaps, but nothing was being analyzed systematically.

The project: scrape, clean, and analyze the full comment history, then package the insights into a decision-ready report that a founder could act on without a data analyst in the room.

## Approach

End-to-end pipeline in Python, split into 4 reproducible scripts:

1. [scripts/01_combine_sources.py](scripts/01_combine_sources.py) — Merge 3 raw Apify scrapes and deduplicate on commentId
2. [scripts/02_clean_and_detect_language.py](scripts/02_clean_and_detect_language.py) — Clean text, strip mentions, bucket comments into fr / en / ar / arabizi / other via a Latin-script detector
3. [scripts/03_sentiment_analysis.py](scripts/03_sentiment_analysis.py) — Score sentiment using `nlptown/bert-base-multilingual-uncased-sentiment` for fr/en/ar, plus a custom Tunisian Arabizi keyword dictionary
4. [scripts/04_theme_extraction.py](scripts/04_theme_extraction.py) — Tag each comment with one or more of 10 commercial themes using multilingual keyword lists

## Key insights

Three headline findings, each tied to a commercial decision:

- Price and availability dominate the conversation (34% of all themed comments). Mnin nishrih? ("Where can I buy it?") is one of the most frequent questions. Distribution is the bottleneck, not demand.
- Scent (parfum) has the strongest negative polarity: 88.89% of scent-related comments are negative. The product reformulation signal is clear and isolated.
- Brand love is high but silent: 27 comments express explicit loyalty with no complaints. These customers are retention assets, not acquisition targets.

## Results

- 283 comments analyzed across 4 languages (124 FR, 73 Arabizi, 48 EN, 38 AR)
- Overall sentiment: 122 positive (43%), 72 neutral (25%), 63 negative (22%), 26 questions (9%)
- 10 commercial themes extracted and quantified
- 1 decision-ready report delivered as the pitch deliverable

## Stack

- Scraping: Apify (TikTok Comments Scraper actor)
- Data processing: Python, pandas
- Language detection: Custom Latin-script heuristic for Tunisian Arabizi
- Sentiment: HuggingFace Transformers, `nlptown/bert-base-multilingual-uncased-sentiment`
- Visualization: Microsoft Power BI, Canva

## Documentation

Full brand report (6 pages, French): [Rapport analytique TikTok ZYNIA.pdf](Rapport%20analytique%20TikTok%20ZYNIA.pdf)

### Dashboard screenshots

![Sentiment distribution](Screenshots/sentiment_distribution.png)
![Theme breakdown](Screenshots/themes_bar_chart.png)
![Sentiment by theme — the scent insight](Screenshots/sentiment_by_theme.png)

## What I owned

- End-to-end pipeline design (scraping to final report)
- Multilingual handling, including a custom Arabizi detection and sentiment layer
- Theme taxonomy design based on actual comment content, not pre-defined categories
- Translation of raw signals into commercial recommendations
- Visual report design in Canva, tailored for a founder reader (not a data analyst)

## Data note

Raw scraped comments are not included in this repository to protect TikTok users' privacy. Comments contain usernames and personal content that users did not consent to have redistributed. The analytical scripts, aggregated insights, and visualizations are shared; the dataset can be regenerated using the scraping script with an Apify account and Zynia's video URLs.

## Running it yourself

1. Install dependencies: `pip install -r scripts/requirements.txt`
2. Scrape comments from Zynia's TikTok videos using the Apify TikTok Comments Scraper, save as `zynia_1.csv`, `zynia_2.csv`, `zynia_3.csv`
3. Run the scripts in order: 01 → 02 → 03 → 04
4. First run of script 03 downloads the BERT model (~700MB)

---

**Project context:** Independent client pitch, 2026
**Target brand:** Zynia Botanicals (Tunisia)
**Author:** Mariem Gadri — [LinkedIn](https://linkedin.com/in/mariemgadri)
