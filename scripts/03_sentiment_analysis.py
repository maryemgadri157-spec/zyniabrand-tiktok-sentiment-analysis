"""
Step 3: Score sentiment on each comment.
- Uses nlptown/bert-base-multilingual-uncased-sentiment for fr/en/ar
- Uses a custom keyword dictionary for Tunisian Arabizi (BERT doesn't handle it well)
"""
import pandas as pd
from transformers import pipeline
import torch

df = pd.read_csv('zynia_clean.csv', encoding='utf-8-sig')
df = df[df['lang_bucket'] != 'other'].reset_index(drop=True)

print("Loading sentiment model (first run downloads ~700MB)...")
sentiment = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment",
    device=0 if torch.cuda.is_available() else -1
)
print("Model loaded.")

positive_arabizi = [
    'bnina', 'bnin', 'ma7leha', 'ma7la', 'mahleha', 'helou', 'helwa',
    'nhebb', 'nheb', 'yeser', 'barcha', 'tayara', 'nchri', 'nehebb',
    'ri7etha bnina', 'rihetha bnina', 'ma3jebni', 'behia', 'behyin',
    'mezyena', 'mezyan', 'top', 'parfait', 'yarabi', 'inshallah'
]
negative_arabizi = [
    '9echra', 'ma7abitech', 'ma7abitou', 'ma3jebnich', 'khayba',
    'khayeb', 'mech behia', 'mahouch behi', 'mahich behia', 'taya7',
    'mech bnina', '3andha mochkla', 'mafihech', 'mahouch', '😔', '🥲', '😭'
]
question_markers = ['?', 'kifech', 'kifeh', 'chno', 'chnoua', 'wa9t',
                    'mnin', 'prix', 'be gadech', 'bgadech', 'win', 'ki']

def arabizi_sentiment(text):
    t = str(text).lower()
    pos = sum(1 for w in positive_arabizi if w in t)
    neg = sum(1 for w in negative_arabizi if w in t)
    is_question = any(q in t for q in question_markers)
    if pos > neg:
        return 'positive'
    if neg > pos:
        return 'negative'
    if is_question:
        return 'question'
    return 'neutral'

def model_sentiment(text):
    try:
        t = str(text)[:500]
        result = sentiment(t)[0]
        stars = int(result['label'][0])
        if stars >= 4:
            return 'positive'
        if stars == 3:
            return 'neutral'
        return 'negative'
    except Exception:
        return 'unknown'

def classify(row):
    if row['lang_bucket'] == 'arabizi':
        return arabizi_sentiment(row['text_clean'])
    return model_sentiment(row['text_clean'])

print(f"Scoring sentiment on {len(df)} comments (takes 1-2 min)...")
df['sentiment'] = df.apply(classify, axis=1)
print("Done.")

print("\nOverall sentiment distribution:")
print(df['sentiment'].value_counts())
print("\nSentiment by language:")
print(pd.crosstab(df['lang_bucket'], df['sentiment']))

df.to_csv('zynia_scored.csv', index=False, encoding='utf-8-sig')
print(f"\nSaved as zynia_scored.csv ({len(df)} rows).")