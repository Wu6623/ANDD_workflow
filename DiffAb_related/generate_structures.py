import subprocess
from pathlib import Path

def generate_structures(model_ckpt, input_jsonl, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "python", "generate.py",
        "--model", model_ckpt,
        "--input", input_jsonl,
        "--output", str(out_dir),
        "--num_samples", "1"
    ]

    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    generate_structures(
        "outputs/diffab_andd_finetuned/model.ckpt",
        "data/processed/andd_diffab_train.jsonl",
        "outputs/generated"
    )
