import pandas as pd
from pathlib import Path

def prepare_andd_for_diffab(
    andd_csv,
    output_dir,
    max_samples=12617
):
    df = pd.read_csv(andd_csv)

    # Minimal required fields
    required_cols = [
        "Sequence",
        "Antigen_Sequence",
        "PDB_ID",
        "Chain_ID"
    ]
    df = df.dropna(subset=required_cols)

    df = df.sample(
        n=min(max_samples, len(df)),
        random_state=42
    )

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # DiffAb-style JSONL
    records = []
    for _, row in df.iterrows():
        records.append({
            "antibody_sequence": row["Sequence"],
            "antigen_sequence": row["Antigen_Sequence"],
            "pdb_id": row["PDB_ID"],
            "chain_id": row["Chain_ID"]
        })

    out_file = output_dir / "andd_diffab_train.jsonl"
    pd.DataFrame(records).to_json(
        out_file,
        orient="records",
        lines=True
    )

    print(f"Prepared {len(records)} entries for DiffAb fine-tuning.")

if __name__ == "__main__":
    prepare_andd_for_diffab(
        "data/andd_subset.csv",
        "data/processed"
    )
