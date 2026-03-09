import json, hashlib, argparse
from pathlib import Path

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default="data/patch_synth.jsonl")
    ap.add_argument("--splits_dir", default="data/splits")
    ap.add_argument("--out", default="data/splits/manifest.json")
    ap.add_argument("--src_key", default="input")
    ap.add_argument("--tgt_key", default="target")
    ap.add_argument("--seed", default="1337")
    args = ap.parse_args()

    dataset = Path(args.dataset)
    splits_dir = Path(args.splits_dir)
    out = Path(args.out)

    files = {
        "dataset": str(dataset),
        "train": str(splits_dir / "train.jsonl"),
        "val": str(splits_dir / "val.jsonl"),
        "hard_v2": str(splits_dir / "hard_v2.jsonl"),
    }

    hashes = {k: sha256_file(Path(v)) for k, v in files.items()}

    manifest = {
        "src_key": args.src_key,
        "tgt_key": args.tgt_key,
        "seed": args.seed,
        "paths": files,
        "sha256": hashes,
    }

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()