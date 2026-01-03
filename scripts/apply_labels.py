import json
import os
import subprocess
import sys
from pathlib import Path

def run(cmd: list[str]) -> None:
    # Print command for visibility
    print(">", " ".join(cmd))
    subprocess.run(cmd, check=True)

def main():
    # Allow passing custom path, default to .github/labels.json
    labels_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".github/labels.json")

    if not labels_path.exists():
        raise SystemExit(f"labels.json not found at: {labels_path}")

    # Basic check: gh installed
    try:
        subprocess.run(["gh", "--version"], check=True, stdout=subprocess.DEVNULL)
    except Exception:
        raise SystemExit("GitHub CLI (gh) not found. Install it and run: gh auth login")

    labels = json.loads(labels_path.read_text(encoding="utf-8"))

    if not isinstance(labels, list):
        raise SystemExit("labels.json must be a JSON array.")

    for item in labels:
        name = item["name"]
        color = item["color"].lstrip("#")
        desc = item.get("description", "")

        # --force updates existing labels if already present
        cmd = ["gh", "label", "create", name, "--color", color, "--force"]
        if desc:
            cmd += ["--description", desc]

        run(cmd)

    print("\n✅ Labels created/updated successfully.")

if __name__ == "__main__":
    main()
