import yaml
import subprocess

def finetune_diffab(config_path):
    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    cmd = [
        "python", "train.py",
        "--data", cfg["data_path"],
        "--pretrained", cfg["pretrained_ckpt"],
        "--epochs", str(cfg["epochs"]),
        "--batch_size", str(cfg["batch_size"]),
        "--lr", str(cfg["learning_rate"]),
        "--output", cfg["output_dir"]
    ]

    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    finetune_diffab("configs/finetune.yaml")
