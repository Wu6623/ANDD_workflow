import pandas as pd

df = pd.read_csv("data/intermediate/parsed.csv")

def classify(seq):
    if len(seq) < 150:
        return "VHH"
    return "Antibody"

df["Ab_or_Nano"] = df["Sequence"].apply(classify)

df.to_csv("data/intermediate/filtered.csv", index=False)
print("[Filter] Antibody/Nanobody classified")
