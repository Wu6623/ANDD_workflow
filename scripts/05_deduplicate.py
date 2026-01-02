import pandas as pd

df = pd.read_csv("data/intermediate/harmonized.csv")
df = df.drop_duplicates(subset=["H_Chain_Seq"])

df.to_csv("data/intermediate/deduplicated.csv", index=False)
print("[Dedup] Completed")
