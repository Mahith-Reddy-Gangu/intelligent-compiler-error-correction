import os
import json
import argparse
import random
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Tuple, Set

RNG_SEED = 2026

# -----------------------------------------
# Rich seed generator (FAST)
# Key fix: DO NOT enumerate the full cartesian product of options.
# Instead, sample candidate specs on-the-fly and greedily pick ones that
# improve coverage until we reach --target.
# -----------------------------------------

FUNC_NAMES = [
    "add", "sub", "mul", "divi", "modi",
    "inc", "dec", "clamp", "max2", "min2",
    "sum3", "mix", "pick", "choose", "blend",
    "foo", "bar", "baz", "qux",
    "calc", "step", "update", "accum",
    "rangeSum", "abs2", "guard", "test",
    "score", "emit", "merge", "fold",
]

@dataclass(frozen=True)
class SeedSpec:
    n_funcs: int
    call_style: str  # none|single|fanout|chain

    include_if_else: bool
    include_while: bool
    include_for: bool
    include_nested_loops: bool
    include_break: bool
    include_continue: bool

    for_init_mode: str  # decl|expr
    for_allow_empty_cond: bool
    for_allow_empty_update: bool

    include_logical: bool
    include_rel_eq: bool
    include_ternary: bool
    include_prefix_unary: bool
    include_postfix_unary: bool
    include_compound_assign: bool

    params_k: int
    args_k: int
    decl_list_k: int

    include_arrays_1d: bool
    include_arrays_2d: bool
    include_float: bool
    include_char: bool


def _safe_mkdir(p: str) -> None:
    os.makedirs(p, exist_ok=True)


def _hash_src(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def _pick_unique_names(n: int) -> List[str]:
    names = FUNC_NAMES[:]
    random.shuffle(names)
    out = []
    used = set()
    for nm in names:
        if nm not in used:
            out.append(nm)
            used.add(nm)
        if len(out) >= n:
            break
    while len(out) < n:
        out.append(f"f{len(out)}")
    return out


def _fmt_params(k: int) -> str:
    pool = [("int", "a"), ("int", "b"), ("float", "f"), ("char", "c")]
    out = []
    for i in range(k):
        t, base = pool[i % len(pool)]
        out.append(f"{t} {base}{i}")
    return ", ".join(out)


def _fmt_args(k: int) -> str:
    pool = ["x", "y", "z", "1", "2", "3", "4", "5"]
    out = []
    for i in range(k):
        out.append(pool[i % len(pool)])
    return ", ".join(out)


def _decl_list(k: int) -> str:
    parts = []
    for i in range(k):
        if i % 2 == 0:
            parts.append(f"p{i} = {i+1}")
        else:
            parts.append(f"p{i}")
    return "int " + ", ".join(parts) + ";"


def _expr_block(spec: SeedSpec) -> List[str]:
    lines: List[str] = []
    lines.append("  int x = 1;")
    lines.append("  int y = 2;")
    lines.append("  int z = 3;")
    lines.append(f"  {_decl_list(spec.decl_list_k)}")

    if spec.include_float:
        lines.append("  float fx = 1.25;")
        lines.append("  float fy = 2.50;")
        lines.append("  float fz = fx + fy;")

    if spec.include_char:
        lines.append("  char ch = 'a';")
        lines.append("  char nl = '\\n';")

    if spec.include_prefix_unary:
        lines.append("  x = !x;")
        lines.append("  x = +x;")
        lines.append("  x = -x;")
        lines.append("  ++x;")
        lines.append("  --y;")

    if spec.include_postfix_unary:
        lines.append("  x++;")
        lines.append("  y--;")

    if spec.include_rel_eq:
        lines.append("  if (x <= y) { z = z + 1; }")
        lines.append("  if (z != 0) { z = z - 1; }")
        lines.append("  if (x == 1) { z = z * 2; }")
        lines.append("  if (y >= 2) { z = z / 2; }")

    if spec.include_logical:
        lines.append("  if ((x < y) && (z > 0)) { z += 1; }")
        lines.append("  if ((x == 0) || (y == 2)) { z -= 1; }")

    if spec.include_ternary:
        lines.append("  int m = (x < y) ? x : y;")
        lines.append("  z = (m == 1) ? (z + 1) : (z + 2);")

    if spec.include_compound_assign:
        lines.append("  x += 1;")
        lines.append("  y -= 1;")
        lines.append("  z *= 2;")
        lines.append("  z /= 2;")
        lines.append("  z %= 3;")

    lines.append("  x = (x = x + 1, y = y + 2, z);")
    return lines


def _arrays_block(spec: SeedSpec) -> List[str]:
    lines: List[str] = []
    if spec.include_arrays_1d:
        lines.append("  int n = 5;")
        lines.append("  int a[10];")
        lines.append("  int b[n];")
        lines.append("  a[0] = 1;")
        lines.append("  b[1] = a[0] + 2;")
        lines.append("  int t = a[0] + b[1];")
    if spec.include_arrays_2d:
        lines.append("  int m2[3][4];")
        lines.append("  m2[1][2] = 7;")
        lines.append("  int u = m2[1][2];")
    return lines


def _if_else_block(spec: SeedSpec) -> List[str]:
    if not spec.include_if_else:
        return []
    return [
        "  if (x < y) {",
        "    z = z + 1;",
        "  } else {",
        "    z = z + 2;",
        "  }",
    ]


def _while_block(spec: SeedSpec) -> List[str]:
    if not spec.include_while:
        return []
    lines = [
        "  while (x < 3) {",
        "    x++;",
    ]
    if spec.include_continue:
        lines += [
            "    if (x == 2) {",
            "      continue;",
            "    }",
        ]
    if spec.include_break:
        lines += [
            "    if (x == 3) {",
            "      break;",
            "    }",
        ]
    lines.append("  }")
    return lines


def _for_block(spec: SeedSpec) -> List[str]:
    if not spec.include_for:
        return []

    lines: List[str] = []

    if spec.for_init_mode == "expr":
        lines.append("  int i = 0;")

    cond = "i < 3"
    upd = "i++"
    if spec.for_allow_empty_cond and random.random() < 0.35:
        cond = ""
    if spec.for_allow_empty_update and random.random() < 0.35:
        upd = ""

    init = "int i = 0" if spec.for_init_mode == "decl" else "i = 0"
    lines.append(f"  for ({init}; {cond}; {upd}) {{")
    lines += [
        "    if (i == 1) {",
        "      ;",
        "    }",
        "    z += i;",
    ]
    if spec.include_continue:
        lines += [
            "    if (i == 2) {",
            "      continue;",
            "    }",
        ]
    if spec.include_break:
        lines += [
            "    if (i == 3) {",
            "      break;",
            "    }",
        ]
    lines.append("  }")
    return lines


def _nested_loops_block(spec: SeedSpec) -> List[str]:
    if not spec.include_nested_loops:
        return []
    return [
        "  for (int i = 0; i < 2; i++) {",
        "    for (int j = 0; j < 3; j++) {",
        "      z += (i + j);",
        "      if ((i == 1) && (j == 2)) {",
        "        break;",
        "      }",
        "    }",
        "  }",
    ]


def _make_helper_func(name: str, spec: SeedSpec) -> str:
    params = _fmt_params(spec.params_k)
    body: List[str] = ["{"]

    body += _expr_block(spec)

    if spec.include_arrays_1d or spec.include_arrays_2d:
        body += _arrays_block(spec)

    body += _if_else_block(spec)
    body += _while_block(spec)
    body += _for_block(spec)
    body += _nested_loops_block(spec)

    body.append("  return 0;")
    body.append("}")
    return f"int {name}({params})\n" + "\n".join(body)


def _make_main(helper_names: List[str], spec: SeedSpec) -> str:
    lines: List[str] = []
    lines.append("int main()")
    lines.append("{")
    lines.append("  int x = 1;")
    lines.append("  int y = 2;")
    lines.append("  int z = 3;")
    lines.append("  ;")

    def call_one(fname: str) -> None:
        args = _fmt_args(spec.args_k)
        lines.append(f"  {fname}({args});")

    if spec.call_style == "none" or not helper_names:
        pass
    elif spec.call_style == "single":
        call_one(helper_names[0])
    elif spec.call_style == "fanout":
        for nm in helper_names[: min(3, len(helper_names))]:
            call_one(nm)
    else:  # chain
        for nm in helper_names[: min(4, len(helper_names))]:
            call_one(nm)

    lines.append("  return 0;")
    lines.append("}")
    return "\n".join(lines)


def _make_program(spec: SeedSpec) -> str:
    helper_count = max(0, spec.n_funcs - 1)
    helper_names = _pick_unique_names(helper_count)

    funcs: List[str] = []
    for i, nm in enumerate(helper_names):
        # per-function variation to reduce repetition
        flip = (i % 2 == 1)
        if not flip:
            local_spec = spec
        else:
            local_spec = SeedSpec(
                n_funcs=spec.n_funcs,
                call_style=spec.call_style,
                include_if_else=spec.include_if_else,
                include_while=spec.include_while,
                include_for=spec.include_for,
                include_nested_loops=spec.include_nested_loops and (random.random() < 0.6),
                include_break=spec.include_break,
                include_continue=spec.include_continue,
                for_init_mode=spec.for_init_mode,
                for_allow_empty_cond=spec.for_allow_empty_cond,
                for_allow_empty_update=spec.for_allow_empty_update,
                include_logical=spec.include_logical,
                include_rel_eq=spec.include_rel_eq,
                include_ternary=spec.include_ternary and (random.random() < 0.7),
                include_prefix_unary=spec.include_prefix_unary,
                include_postfix_unary=spec.include_postfix_unary,
                include_compound_assign=spec.include_compound_assign and (random.random() < 0.8),
                params_k=spec.params_k,
                args_k=spec.args_k,
                decl_list_k=spec.decl_list_k,
                include_arrays_1d=spec.include_arrays_1d and (random.random() < 0.7),
                include_arrays_2d=spec.include_arrays_2d and (random.random() < 0.5),
                include_float=spec.include_float and (random.random() < 0.7),
                include_char=spec.include_char and (random.random() < 0.7),
            )
        funcs.append(_make_helper_func(nm, local_spec))

    funcs.append(_make_main(helper_names, spec))
    return "\n\n".join(funcs) + "\n"


def _feature_vector(spec: SeedSpec) -> Dict[str, int]:
    # match what your audit cares about + the missing ones you mentioned
    return {
        "else_branch": int(spec.include_if_else),
        "continue_statement": int(spec.include_continue),
        "empty_statement": 1,
        "array_declaration": int(spec.include_arrays_1d or spec.include_arrays_2d),
        "array_indexing": int(spec.include_arrays_1d or spec.include_arrays_2d),
        "multi_dim_arrays": int(spec.include_arrays_2d),
        "float_literals": int(spec.include_float),
        "char_literals": int(spec.include_char),
        "ternary_operator": int(spec.include_ternary),
        "for_init_expression": int(spec.include_for and spec.for_init_mode == "expr"),
        "op_&&": int(spec.include_logical),
        "op_||": int(spec.include_logical),
        "op_--": int(spec.include_prefix_unary or spec.include_postfix_unary),
        "break_statement": int(spec.include_break),
        "op_*=": int(spec.include_compound_assign),
        "op_/=": int(spec.include_compound_assign),
        "op_%=": int(spec.include_compound_assign),
        "op_!": int(spec.include_prefix_unary),
    }


def _rand_bool(p_true: float) -> bool:
    return random.random() < p_true


def _random_spec() -> SeedSpec:
    # Biased sampling toward “rich” programs (more True than False)
    n_funcs = random.choice([2, 3, 4, 5, 6, 1])
    call_style = random.choice(["chain", "fanout", "single", "none"])
    if n_funcs == 1:
        call_style = "none"

    include_for = _rand_bool(0.75)
    include_while = _rand_bool(0.65)
    include_if_else = _rand_bool(0.75)

    include_break = _rand_bool(0.55)   # ensure we get lots of break
    include_continue = _rand_bool(0.55)

    include_nested_loops = _rand_bool(0.45)

    for_init_mode = random.choice(["decl", "expr"])
    for_allow_empty_cond = _rand_bool(0.35) if include_for else False
    for_allow_empty_update = _rand_bool(0.35) if include_for else False

    include_logical = _rand_bool(0.65)
    include_rel_eq = True
    include_ternary = _rand_bool(0.65)

    include_prefix_unary = _rand_bool(0.65)   # ensures unary ! appears
    include_postfix_unary = _rand_bool(0.65)

    include_compound_assign = _rand_bool(0.70)  # ensures *= /= %= appear

    params_k = random.choice([0, 1, 2, 3])
    args_k = random.choice([0, 1, 2, 3])
    decl_list_k = random.choice([1, 2, 3, 4])

    include_arrays_1d = _rand_bool(0.65)
    include_arrays_2d = _rand_bool(0.45)
    include_float = _rand_bool(0.55)
    include_char = _rand_bool(0.55)

    # If 2D arrays, allow 1D either way (both are fine)
    return SeedSpec(
        n_funcs=n_funcs,
        call_style=call_style,
        include_if_else=include_if_else,
        include_while=include_while,
        include_for=include_for,
        include_nested_loops=include_nested_loops,
        include_break=include_break,
        include_continue=include_continue,
        for_init_mode=for_init_mode,
        for_allow_empty_cond=for_allow_empty_cond,
        for_allow_empty_update=for_allow_empty_update,
        include_logical=include_logical,
        include_rel_eq=include_rel_eq,
        include_ternary=include_ternary,
        include_prefix_unary=include_prefix_unary,
        include_postfix_unary=include_postfix_unary,
        include_compound_assign=include_compound_assign,
        params_k=params_k,
        args_k=args_k,
        decl_list_k=decl_list_k,
        include_arrays_1d=include_arrays_1d,
        include_arrays_2d=include_arrays_2d,
        include_float=include_float,
        include_char=include_char,
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out_dir", default=os.path.join("data", "seed_programs_generated"))
    ap.add_argument("--target", type=int, default=300)
    ap.add_argument("--min_per_feature", type=int, default=30)
    ap.add_argument("--start_index", type=int, default=0)
    ap.add_argument("--batch", type=int, default=250, help="how many random candidate specs to score per seed")
    ap.add_argument("--max_attempts", type=int, default=200000)
    args = ap.parse_args()

    random.seed(RNG_SEED)
    _safe_mkdir(args.out_dir)

    # Coverage tracking
    # (Initialize keys from a sample)
    sample = _random_spec()
    coverage_keys = list(_feature_vector(sample).keys())
    coverage: Dict[str, int] = {k: 0 for k in coverage_keys}

    def score(spec: SeedSpec) -> int:
        vec = _feature_vector(spec)
        s = 0
        for k, v in vec.items():
            if v == 1 and coverage[k] < args.min_per_feature:
                s += (args.min_per_feature - coverage[k])
        # mild preference toward richer structure
        s += min(3, spec.n_funcs - 1)
        if spec.call_style in ("fanout", "chain"):
            s += 2
        if spec.include_nested_loops:
            s += 2
        if spec.include_compound_assign:
            s += 2
        if spec.include_break:
            s += 1
        if spec.include_continue:
            s += 1
        return s

    seen_hashes: Set[str] = set()
    programs: List[Tuple[str, SeedSpec]] = []
    attempts = 0

    while len(programs) < args.target and attempts < args.max_attempts:
        attempts += 1

        # pick best out of a batch of random specs
        best_spec = None
        best_score = -1
        for _ in range(args.batch):
            sp = _random_spec()
            sc = score(sp)
            if sc > best_score:
                best_score = sc
                best_spec = sp

        if best_spec is None:
            continue

        src = _make_program(best_spec)
        h = _hash_src(src)
        if h in seen_hashes:
            continue

        seen_hashes.add(h)
        programs.append((src, best_spec))

        vec = _feature_vector(best_spec)
        for k, v in vec.items():
            coverage[k] += v

        # small progress ping every 25 seeds so you know it's alive
        if len(programs) % 25 == 0:
            print(f"[progress] wrote {len(programs)}/{args.target} seeds...")

    # Write seeds
    for idx, (src, spec) in enumerate(programs, start=args.start_index):
        fn = f"seedg_{idx:03d}.c"
        path = os.path.join(args.out_dir, fn)
        with open(path, "w", encoding="utf-8") as f:
            f.write(src)

    report = {
        "generated": len(programs),
        "attempts": attempts,
        "min_per_feature_target": args.min_per_feature,
        "coverage": coverage,
    }
    with open(os.path.join(args.out_dir, "_coverage_report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"Wrote {len(programs)} generated seeds to {args.out_dir}")
    print("Coverage:", coverage)
    print(f"Report: {os.path.join(args.out_dir, '_coverage_report.json')}")

    if len(programs) < args.target:
        print("WARNING: could not reach target within max_attempts. Try lowering --min_per_feature or increasing --max_attempts/batch.")


if __name__ == "__main__":
    main()