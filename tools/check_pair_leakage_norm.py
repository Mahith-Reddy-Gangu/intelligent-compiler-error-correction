import json
import re
import hashlib
from pathlib import Path

TRAIN = Path("data/splits/train.jsonl")
VAL   = Path("data/splits/val.jsonl")
HARD  = Path("data/splits/hard_v2.jsonl")

SRC_KEY = "input"
TGT_KEY = "target"

_ws = re.compile(r"\s+")

def norm(s: str) -> str:
    # aggressive but safe: collapse all whitespace
    return _ws.sub(" ", s.strip())

def h(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()

def read_pairs(path: Path):
    pairs = set()
    n = 0
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            src = norm(r.get(SRC_KEY, ""))
            tgt = r.get(TGT_KEY, "")
            pairs.add(h(src + "\n<<<SEP>>>\n" + tgt))
            n += 1
    return pairs, n

def main():
    tr, ntr = read_pairs(TRAIN)
    va, nva = read_pairs(VAL)
    ha, nha = read_pairs(HARD)

    print("=== NORMALIZED (src,tgt) OVERLAP CHECK ===")
    print("train rows:", ntr, "unique pairs:", len(tr))
    print("val rows:  ", nva, "unique pairs:", len(va))
    print("hard rows: ", nha, "unique pairs:", len(ha))

    ov_tr_va = tr & va
    ov_tr_ha = tr & ha
    ov_va_ha = va & ha

    print("\nOverlaps:")
    print("train ∩ val :", len(ov_tr_va))
    print("train ∩ hard:", len(ov_tr_ha))
    print("val   ∩ hard:", len(ov_va_ha))

    if len(ov_tr_va) == 0 and len(ov_tr_ha) == 0 and len(ov_va_ha) == 0:
        print("\n✅ No normalized pair leakage detected.")
    else:
        print("\n❌ Pair leakage detected. Investigate generator/split.")

if __name__ == "__main__":
    main()