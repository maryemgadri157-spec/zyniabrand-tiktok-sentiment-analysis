"""
Step 1: Combine the 3 raw TikTok scrapes into one deduplicated CSV.
Expects 3 CSVs from Apify TikTok Comments Scraper runs.
"""
import pandas as pd

files = ['zynia_1.csv', 'zynia_2.csv', 'zynia_3.csv']
dfs = [pd.read_csv(f) for f in files]

df = pd.concat(dfs, ignore_index=True)
print(f"Total rows before dedup: {len(df)}")

df = df.drop_duplicates(subset='commentId')
print(f"Total rows after dedup: {len(df)}")

df.to_csv('zynia_combined.csv', index=False, encoding='utf-8-sig')
print("Saved as zynia_combined.csv")