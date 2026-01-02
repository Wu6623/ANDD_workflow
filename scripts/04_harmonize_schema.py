import pandas as pd

df = pd.read_csv("data/intermediate/filtered.csv")

df["H_Chain_Seq"] = df["Sequence"]
df["L_Chain_Seq"] = "NA"
df["Ag_Seq"] = "NA"
df["Affinity_Kd"] = "NA"
df["Affinity_Method"] = "NA"
df["Reason_Code"] = "not_reported"
df["Predicted_or_Not"] = False

df.to_csv("data/intermediate/harmonized.csv", index=False)
print("[Schema] Harmonised")
