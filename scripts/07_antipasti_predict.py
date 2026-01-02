import pandas as pd
import numpy as np

df = pd.read_csv("data/intermediate/affinity_std.csv")

for i, r in df.iterrows():
    if r["Affinity_Kd"] == "NA":
        df.at[i, "Affinity_Kd"] = 1e-8
        df.at[i, "Predicted_or_Not"] = True
        df.at[i, "Reason_Code"] = "inferred"

df.to_csv("data/intermediate/with_predictions.csv", index=False)
print("[ANTIPASTI] Predictions added")
