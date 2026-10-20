#!/usr/bin/env python3
"""Lab 3 beam tools as a command-line skill for Claude Code (.claude/skills/beam-tools/).

Three dumb tools, one job each, units in the names (Lecture 6, slide 22):
  candidates                       -> list the catalogue sections
  lookup   --section W12x26        -> {Ix_in4, Sx_in3, wt_plf}
  deflection --span-ft 20 --w-klf 0.5 --section W12x26 [--E-ksi 29000]
                                   -> {delta_in, limit_in, passes, inputs}
  check    --span-ft 20 --w-klf 0.5 --section W12x26
                                   -> deflection + bending stress verdict (the Checker)

Every result carries the inputs it came from (Lecture 6, decision table row 2).
Catalogue values: AISC Steel Construction Manual, 15th ed., Table 1-1 (illustrative subset).
"""
import argparse
import json
import sys

E_KSI_DEFAULT = 29000.0          # A992 steel
F_ALLOW_KSI = 33.0               # 0.66 Fy, A992 (demo check only)

CATALOGUE = {
    # name:    (Ix_in4, Sx_in3, wt_plf)  — identical to Lecture 6 lab3_demo/tools.py
    "W8x15":  (48.0, 11.8, 15),
    "W10x15": (68.9, 13.8, 15),
    "W10x22": (118.0, 23.2, 22),
    "W12x26": (204.0, 33.4, 26),
    "W16x26": (301.0, 38.4, 26),
    "W12x30": (238.0, 38.6, 30),
    "W14x30": (291.0, 42.0, 30),
    "W14x90": (999.0, 143.0, 90),
}


def candidates():
    return {"sections": sorted(CATALOGUE, key=lambda k: (CATALOGUE[k][2], CATALOGUE[k][0])), "source": "AISC 15th ed. Table 1-1 (subset)"}


def lookup(section: str):
    key = section.replace("×", "x").replace("X", "x").strip()
    if key not in CATALOGUE:
        # The first boundary: refuse names outside the catalogue (L6 slide 22).
        raise KeyError(f"{section!r} is not in the catalogue. Use `candidates`.")
    ix, sx, wt = CATALOGUE[key]
    return {"section": key, "Ix_in4": ix, "Sx_in3": sx, "wt_plf": wt,
            "source": "AISC 15th ed. Table 1-1"}


def deflection(span_ft: float, w_klf: float, section: str, e_ksi: float = E_KSI_DEFAULT):
    p = lookup(section)
    L = span_ft * 12.0            # in
    w = w_klf / 12.0              # k/in
    delta = 5 * w * L**4 / (384 * e_ksi * p["Ix_in4"])
    limit = L / 360.0
    return {"delta_in": round(delta, 3), "limit_in": round(limit, 3),
            "passes_deflection": delta <= limit,
            "inputs": {"span_ft": span_ft, "w_klf": w_klf, "section": p["section"],
                       "E_ksi": e_ksi, "Ix_in4": p["Ix_in4"]}}


def check(span_ft: float, w_klf: float, section: str, e_ksi: float = E_KSI_DEFAULT):
    """Deterministic Checker (Lecture 6, slide 33): no model anywhere in here."""
    d = deflection(span_ft, w_klf, section, e_ksi)
    p = lookup(section)
    M_kft = w_klf * span_ft**2 / 8.0
    stress = (M_kft * 12.0) / p["Sx_in3"]          # ksi
    ok = d["passes_deflection"] and stress <= F_ALLOW_KSI
    if ok:
        msg = "PASS"
    else:
        need_ix = p["Ix_in4"] * d["delta_in"] / d["limit_in"]
        msg = (f"delta = {d['delta_in']:.2f} in > {d['limit_in']:.2f} in; "
               f"need Ix >= {need_ix:.0f} in4")
    return {"passes": ok, "delta_in": d["delta_in"], "limit_in": d["limit_in"],
            "stress_ksi": round(stress, 1), "stress_limit_ksi": F_ALLOW_KSI,
            "message": msg, "inputs": d["inputs"]}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("candidates")
    s = sub.add_parser("lookup"); s.add_argument("--section", required=True)
    for name in ("deflection", "check"):
        s = sub.add_parser(name)
        s.add_argument("--span-ft", type=float, required=True)
        s.add_argument("--w-klf", type=float, required=True)
        s.add_argument("--section", required=True)
        s.add_argument("--E-ksi", dest="e_ksi", type=float, default=E_KSI_DEFAULT)
    a = ap.parse_args(argv)
    try:
        if a.cmd == "candidates":
            out = candidates()
        elif a.cmd == "lookup":
            out = lookup(a.section)
        elif a.cmd == "deflection":
            out = deflection(a.span_ft, a.w_klf, a.section, a.e_ksi)
        else:
            out = check(a.span_ft, a.w_klf, a.section, a.e_ksi)
    except KeyError as e:
        print(json.dumps({"error": str(e)}))
        return 2
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
