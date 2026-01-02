import pandas as pd

rows = []

# Parse UniProt
df_uni = pd.read_csv("data/raw/uniprot.tsv", sep="\t")
for _, r in df_uni.iterrows():
    rows.append({
        "Source": "UniProt",
        "PDB_ID": "NA",
        "Sequence": r["Sequence"]
    })

pd.DataFrame(rows).to_csv(
    "data/intermediate/parsed.csv", index=False
)

print("[Parse] Completed")
