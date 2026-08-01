#!/usr/bin/env python3
"""
build_attack_extract.py — derive the two compact files map_controls.py ships with.

The full ATT&CK Enterprise bundle is ~45 MB and is gitignored (setup.sh downloads it),
so it cannot be relied on at runtime. This extracts only what the mitigation and
telemetry modes need, which is small enough to commit.

    python3 build_attack_extract.py [--attack path/to/enterprise-attack.json]

Writes, alongside itself:
    attack_mitigations.json   M-code -> name, MITRE description, techniques mitigated
    attack_telemetry.json     technique -> detection analytics + named log sources

Re-run after an ATT&CK refresh. Everything here is MITRE's own text, carried unchanged.
"""
import argparse, json, os, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ATTACK = os.path.join(HERE, "..", "..", "mitre-attack", "enterprise-attack.json")


def ext_id(o):
    return next((r["external_id"] for r in o.get("external_references", [])
                 if r.get("source_name") == "mitre-attack"), None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--attack", default=DEFAULT_ATTACK)
    a = ap.parse_args()
    if not os.path.isfile(a.attack):
        sys.exit(f"ATT&CK bundle not found at {a.attack}\n"
                 "Run ./scripts/setup.sh (it downloads it) or pass --attack.")

    with open(a.attack, encoding="utf-8") as f:
        bundle = json.load(f)
    objs = bundle["objects"]
    by = {o["id"]: o for o in objs}

    # ---- mitigations -------------------------------------------------------
    mit = {}
    for o in objs:
        if o.get("type") == "course-of-action" and not o.get("revoked") \
                and not o.get("x_mitre_deprecated"):
            code = ext_id(o)
            if code and code.startswith("M"):
                mit[o["id"]] = {"id": code, "name": o["name"],
                                "description": " ".join(str(o.get("description", "")).split()),
                                "techniques": []}
    for r in objs:
        if r.get("type") == "relationship" and r.get("relationship_type") == "mitigates":
            src, tgt = by.get(r["source_ref"]), by.get(r["target_ref"])
            if src and tgt and src["id"] in mit and tgt.get("type") == "attack-pattern":
                t = ext_id(tgt)
                if t and not tgt.get("revoked") and not tgt.get("x_mitre_deprecated"):
                    mit[src["id"]]["techniques"].append(t)
    mitigations = {m["id"]: {**m, "techniques": sorted(set(m["techniques"]))}
                   for m in mit.values() if m["techniques"]}

    # ---- telemetry ---------------------------------------------------------
    # detection-strategy --detects--> technique; strategy references analytics;
    # each analytic names its log sources and channels.
    strat_for = collections.defaultdict(list)
    for r in objs:
        if r.get("type") == "relationship" and r.get("relationship_type") == "detects":
            tgt = by.get(r["target_ref"])
            if tgt and tgt.get("type") == "attack-pattern":
                t = ext_id(tgt)
                if t:
                    strat_for[t].append(r["source_ref"])

    telemetry = {}
    for tech, sids in strat_for.items():
        seen, items = set(), []
        for sid in sids:
            s = by.get(sid) or {}
            for aid in s.get("x_mitre_analytic_refs", []):
                an = by.get(aid) or {}
                desc = " ".join(str(an.get("description", "")).split())
                if not desc or desc in seen:
                    continue
                seen.add(desc)
                srcs = []
                for ls in an.get("x_mitre_log_source_references", []):
                    nm, ch = ls.get("name"), ls.get("channel")
                    if nm:
                        srcs.append({"source": nm, "channel": ch} if ch else {"source": nm})
                items.append({"detection": desc, "log_sources": srcs})
        if items:
            telemetry[tech] = items

    meta = {"_meta": {
        "generated_from": os.path.basename(a.attack),
        "note": "MITRE ATT&CK text carried unchanged. Regenerate with "
                "data/attack-control-mapping/build_attack_extract.py after an ATT&CK refresh.",
        "mitigations": len(mitigations),
        "techniques_with_telemetry": len(telemetry),
    }}
    with open(os.path.join(HERE, "attack_mitigations.json"), "w", encoding="utf-8") as f:
        json.dump({**meta, "mitigations": mitigations}, f, indent=1)
    with open(os.path.join(HERE, "attack_telemetry.json"), "w", encoding="utf-8") as f:
        json.dump({**meta, "telemetry": telemetry}, f, indent=1)
    print(f"wrote attack_mitigations.json ({len(mitigations)} mitigations)")
    print(f"wrote attack_telemetry.json ({len(telemetry)} techniques)")


if __name__ == "__main__":
    main()
