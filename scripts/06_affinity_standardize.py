import pandas as pd

df = pd.read_csv("data/intermediate/deduplicated.csv")

def standardize(x):
    try:
        return float(x)
    except:
        return "NA"

df["Affinity_Kd"] = df["Affinity_Kd"].apply(standardize)

df.to_csv("data/intermediate/affinity_std.csv", index=False)
print("[Affinity] Standardised")
