import pandas as pd
import json
import os

df = pd.read_csv("data/intermediate/with_predictions.csv")

report = {
    "n_entries": len(df),
    "antibody": int((df["Ab_or_Nano"] == "Antibody").sum()),
    "nanobody": int((df["Ab_or_Nano"] == "VHH").sum()),
    "affinity_available": int((df["Affinity_Kd"] != "NA").sum())
}

os.makedirs("data/final", exist_ok=True)

with open("data/final/validation_report.json", "w") as f:
    json.dump(report, f, indent=2)

print("[QC] Validation report written")
