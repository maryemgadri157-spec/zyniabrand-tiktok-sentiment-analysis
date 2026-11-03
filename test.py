import pandas as pd

# ---- Load the 3 CSVs ----
files = ['zynia_1.csv', 'zynia_2.csv', 'zynia_3.csv']
dfs = [pd.read_csv(f) for f in files]

# ---- Combine ----
df = pd.concat(dfs, ignore_index=True)
print(f"Total rows before dedup: {len(df)}")

# ---- Remove duplicate comments (same commentId appearing twice) ----
df = df.drop_duplicates(subset='commentId')
print(f"Total rows after dedup: {len(df)}")

# ---- Save as one combined file ----
df.to_csv('zynia_combined.csv', index=False, encoding='utf-8-sig')
print("Saved as zynia_combined.csv")