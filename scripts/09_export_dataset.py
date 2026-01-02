import pandas as pd
import os

df = pd.read_csv("data/intermediate/with_predictions.csv")

os.makedirs("data/final/All_structures", exist_ok=True)

df.to_csv("data/final/ANDD.csv", index=False)

print("[Export] ANDD.csv generated")
