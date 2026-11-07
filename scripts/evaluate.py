import argparse, json
from pathlib import Path
from app.services.matching import cosine

def top1_precision(records):
    if not records:
        return 0.0
    correct = sum(1 for r in records if r["predicted_image"] == r["expected_image"])
    return correct / len(records)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/eval/eval_results.json")
    args = parser.parse_args()
    path = Path(args.input)
    if not path.exists():
        raise SystemExit(f"Missing {path}. Run your evaluation and write the JSON results first.")
    records = json.loads(path.read_text())
    precision = top1_precision(records)
    print(f"Top-1 precision: {precision:.3f} ({precision*100:.1f}%)")
    return precision

if __name__ == "__main__":
    main()
