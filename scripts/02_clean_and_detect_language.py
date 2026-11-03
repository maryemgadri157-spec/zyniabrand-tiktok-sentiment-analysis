"""
Step 2: Clean the combined dataset and bucket each comment by language.
Detects Tunisian Arabizi (Latin-script Arabic dialect) via script-based heuristic.
"""
import pandas as pd

df = pd.read_csv('zynia_combined.csv', encoding='utf-8-sig')

df = df[['commentId', 'text', 'language', 'likes', 'replyCount',
         'type', 'videoUrl', 'createdAt', 'authorUsername']]

df['text'] = df['text'].astype(str).str.strip()
df = df[df['text'].str.len() > 2]
df = df[~df['text'].str.match(r'^[@\s\W]+$')]
df['text'] = df['text'].str.replace(r'\s+', ' ', regex=True)

df['text_clean'] = df['text'].str.replace(r'@\w+\s*', '', regex=True).str.strip()
df = df[df['text_clean'].str.len() > 1]

def is_latin_script(text):
    letters = [c for c in str(text) if c.isalpha()]
    if not letters:
        return False
    latin_count = sum(1 for c in letters if c.isascii())
    return latin_count / len(letters) > 0.7

df['is_latin'] = df['text_clean'].apply(is_latin_script)

def bucket_lang(row):
    if row['language'] == 'fr':
        return 'fr'
    if row['language'] == 'en':
        return 'en'
    if row['language'] == 'ar':
        return 'ar'
    if row['is_latin']:
        return 'arabizi'
    return 'other'

df['lang_bucket'] = df.apply(bucket_lang, axis=1)

print(f"Total rows: {len(df)}")
print(f"\nLanguage buckets:")
print(df['lang_bucket'].value_counts())

df.to_csv('zynia_clean.csv', index=False, encoding='utf-8-sig')
print(f"\nSaved as zynia_clean.csv")