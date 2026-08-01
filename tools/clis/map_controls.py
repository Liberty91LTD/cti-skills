#!/usr/bin/env python3
"""
map_controls.py — join a customer control baseline to an attacker technique set.

Standalone, stdlib only. Produces the four buckets a FAIR Resistance Strength
assessment needs, plus the diagnostics that stop the output being misleading.

FOUR MODES
    --controls baseline.csv     coverage: what does their CURRENT set cover
    (omit --controls)           recommend: which controls SHOULD address these
    --mitigations               ATT&CK M-codes with MITRE's own definitions
    --telemetry                 named log sources + MITRE detection logic

    python3 map_controls.py --controls baseline.csv --techniques techs.json
    python3 map_controls.py --techniques T1566,T1190,T1078
    python3 map_controls.py --techniques techs.json --mitigations --telemetry

WHY --mitigations AND --telemetry EXIST
    The NIST half of the evidence base carries a control id and a name and nothing
    else. "SI-04 System Monitoring" stands in for 52 distinct techniques and tells a
    reader nothing they can act on, and the workbook has no control text to expand it
    with. ATT&CK does: its mitigations ship MITRE's own definition, and its detection
    strategies resolve "monitoring" into named log sources and channels. Reach for
    these two modes whenever the answer has to be actionable rather than auditable.

INPUTS
  master_mapping.json   9,545 control-to-technique rows exported from
                        attack_control_effectiveness_mapping.xlsx (Master_Mapping sheet).
                        Ships alongside this script so no Excel dependency is needed.

  controls CSV          The customer's control set. Required columns:
                          control_ref     your identifier, e.g. IAM-05
                          control_name    human name
                          framework       must match master_mapping.control_framework exactly,
                                          e.g. "NIST SP 800-53 rev5", "Microsoft 365 security"
                          mapping_key     must match master_mapping.control_id exactly,
                                          e.g. "AC-06", "EID-MFA-E3". Leave EMPTY when the
                                          control genuinely does not map: that is a finding,
                                          not a gap to be filled with a guess.
                        Optional: implementation_status, owner, mapping_note.

  techniques            Either a JSON file (see --techniques-format) or a comma-separated
                        list of ATT&CK IDs. Counts are optional; they only affect ordering.

OUTPUT
  JSON on stdout with four buckets and a diagnostics block. See BUCKETS below.
"""
import argparse, csv, json, os, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- known corrections

# ATT&CK IDs MITRE has revoked. A feed still emitting these will join to nothing and
# the technique will land in "no matching control", i.e. a stale identifier reads as a
# security gap. Verified against ATT&CK Enterprise v19.1 revoked-by relationships.
REVOKED = {
    "T1081": "T1552.001",   # Credentials In Files
    "T1192": "T1566.002",   # Spearphishing Link
    "T1188": "T1090.003",   # Multi-hop Proxy
    "T1488": "T1561.001",   # Disk Content Wipe
    "T1022": "T1560",       # Archive Collected Data
}

# ATT&CK's placeholder mitigation meaning "cannot be mitigated before compromise".
# A technique whose ONLY mapping is this is not an actionable control gap: it is
# ATT&CK stating that no preventive control applies. Keep it out of the gap list.
PRE_COMPROMISE = "M1056"

EFF_ORDER = {"significant": 0, "partial": 1, "minimal": 2, "coverage-only": 3}

# ---------------------------------------------------------------- load


DATA_CANDIDATES = [
    os.path.join(HERE, "..", "..", "data", "attack-control-mapping"),  # repo layout
    os.path.join(HERE, "data", "attack-control-mapping"),
    os.path.join(HERE),                                                 # flat/portable copy
]


def data_file(name):
    for d in DATA_CANDIDATES:
        p = os.path.join(d, name)
        if os.path.isfile(p):
            return p
    sys.exit(f"could not locate {name}; looked in:\n  " +
             "\n  ".join(os.path.normpath(d) for d in DATA_CANDIDATES))


def load_mapping(path=None):
    with open(path or data_file("master_mapping.json"), encoding="utf-8") as f:
        return json.load(f)


def load_attack(kind):
    """kind: 'mitigations' or 'telemetry'. Shipped pre-extracted, because the full
    ATT&CK bundle is ~45 MB and gitignored, so it is absent on a fresh clone."""
    with open(data_file(f"attack_{kind}.json"), encoding="utf-8") as f:
        return json.load(f)


def load_controls(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    missing = {"control_ref", "framework", "mapping_key"} - set(rows[0] or {})
    if missing:
        sys.exit(f"controls CSV missing required column(s): {', '.join(sorted(missing))}")
    return rows


def load_techniques(spec, fmt):
    """Accepts a comma-separated ID list, or JSON in one of three shapes."""
    if not os.path.isfile(spec):
        return [{"id": t.strip(), "count": 1} for t in spec.split(",") if t.strip()]
    with open(spec, encoding="utf-8") as f:
        data = json.load(f)
    if fmt == "auto":
        if isinstance(data, dict) and "techniques" in data:
            data = data["techniques"]
        if isinstance(data, dict):                      # {"T1566": {...}} or {"T1566": 12}
            return [{"id": k, "count": (v.get("count", v.get("actor_count", 1))
                                        if isinstance(v, dict) else v)}
                    for k, v in data.items()]
        if isinstance(data, list):                      # [{"id":..,"count":..}] or ["T1566"]
            return [({"id": x, "count": 1} if isinstance(x, str)
                     else {"id": x.get("id") or x.get("technique_id"),
                           "count": x.get("count", 1)}) for x in data]
    sys.exit("could not parse techniques input; pass --techniques-format")


# ---------------------------------------------------------------- join


def normalise(techs):
    """Merge revoked IDs into their successors, reporting what moved."""
    merged, moves = collections.Counter(), collections.Counter()
    for t in techs:
        tid = t["id"]
        if tid in REVOKED:
            moves[f"{tid} -> {REVOKED[tid]}"] += t.get("count", 1)
            tid = REVOKED[tid]
        merged[tid] += t.get("count", 1)
    return merged, dict(moves)


def join(controls, techs, mapping):
    rows_by_control = collections.defaultdict(list)
    rows_by_tech = collections.defaultdict(list)
    for r in mapping:
        rows_by_control[(r["control_framework"], r["control_id"])].append(r)
        rows_by_tech[r["technique_id"]].append(r)

    reachable = collections.defaultdict(list)   # technique -> customer control rows
    control_status = []
    for c in controls:
        key = (c["framework"], c["mapping_key"]) if c.get("mapping_key") else None
        hits = rows_by_control.get(key, []) if key else []
        control_status.append({
            "control_ref": c["control_ref"],
            "control_name": c.get("control_name", ""),
            "framework": c.get("framework", ""),
            "mapping_key": c.get("mapping_key", ""),
            "implementation_status": c.get("implementation_status", ""),
            "workbook_rows": len(hits),
            "maps": bool(hits),
            "mapping_note": c.get("mapping_note", ""),
        })
        for h in hits:
            reachable[h["technique_id"]].append({
                "control_ref": c["control_ref"],
                "control_id": h["control_id"],
                "control_name": h["control_name"],
                "framework": h["control_framework"],
                "source": h["source"],
                "function": h["function"],
                "effectiveness": h["effectiveness"],
                "implementation_status": c.get("implementation_status", ""),
            })

    counts, moves = normalise(techs)
    known = set(rows_by_tech)

    buckets = {"significant": [], "weak": [], "gap": [], "no_control_exists": []}
    for tid, n in counts.most_common():
        hits = sorted(reachable.get(tid, []), key=lambda h: EFF_ORDER[h["effectiveness"]])
        all_rows = rows_by_tech.get(tid, [])
        only_pre = bool(all_rows) and {r["control_id"] for r in all_rows} == {PRE_COMPROMISE}
        entry = {"technique_id": tid, "count": n,
                 "workbook_rows": len(all_rows), "controls": hits,
                 "in_mapping": tid in known,
                 "pre_compromise_only": only_pre}
        if any(h["effectiveness"] == "significant" for h in hits):
            buckets["significant"].append(entry)
        elif hits:
            buckets["weak"].append(entry)
        elif tid not in known or only_pre:
            buckets["no_control_exists"].append(entry)
        else:
            buckets["gap"].append(entry)

    return buckets, control_status, moves


# ---------------------------------------------------------------- main

def recommend(techs, mapping, top=25, min_support=3, threshold=1.5):
    """No baseline: which controls does the evidence base say address these techniques?

    Answers "what should I have in place", as distinct from "what does my current set
    cover". Ranks by how many of the supplied techniques a control addresses at
    `significant` strength, then by total techniques touched, so the top of the list
    is the shortest route to covering the most of what is actually being seen.
    """
    rows_by_tech = collections.defaultdict(list)
    for r in mapping:
        rows_by_tech[r["technique_id"]].append(r)

    counts, moves = normalise(techs)
    weight = {}          # control -> {sig:set, any:set, meta}
    unaddressed = []
    for tid, n in counts.items():
        rs = rows_by_tech.get(tid, [])
        if not rs or {r["control_id"] for r in rs} == {PRE_COMPROMISE}:
            unaddressed.append({"technique_id": tid, "count": n,
                                "reason": "pre-compromise only" if rs else "no control mapped"})
            continue
        for r in rs:
            k = (r["control_framework"], r["control_id"])
            w = weight.setdefault(k, {"sig": set(), "any": set(),
                                      "name": r["control_name"], "source": r["source"]})
            w["any"].add(tid)
            if r["effectiveness"] == "significant":
                w["sig"].add(tid)

    # Only the four CTID cloud stacks carry effectiveness scores. Ranking everything
    # on `significant` therefore returns nothing but vendor products and can never
    # surface a control class, which is useless to anyone not on those stacks and
    # reads as a product pitch. Split by evidence type and rank each on its own terms.
    SCORED = {"Microsoft 365 security", "Microsoft Azure security",
              "AWS security services", "Google Cloud security"}

    def entry(fw, cid, w):
        return {"framework": fw, "control_id": cid, "control_name": w["name"],
                "source": w["source"],
                "techniques_addressed_significant": sorted(w["sig"]),
                "techniques_addressed_any": len(w["any"]),
                "observed_events_covered": sum(counts[t] for t in w["any"]),
                "observed_events_covered_significant": sum(counts[t] for t in w["sig"])}

    scored = sorted(((k, v) for k, v in weight.items() if k[0] in SCORED),
                    key=lambda kv: (-len(kv[1]["sig"]),
                                    -sum(counts[t] for t in kv[1]["sig"]),
                                    -len(kv[1]["any"])))
    classes = sorted(((k, v) for k, v in weight.items() if k[0] not in SCORED),
                     key=lambda kv: (-len(kv[1]["any"]),
                                     -sum(counts[t] for t in kv[1]["any"])))
    # Control classes suffer the hygiene bias badly: SI-04 covers most of any input
    # because it covers most of ATT&CK. Split them on lift so the distinctive ones
    # surface instead of the same handful of families every time.
    cls_universe = collections.defaultdict(set)
    for r in mapping:
        if r["control_framework"] not in SCORED:
            cls_universe[(r["control_framework"], r["control_id"])].add(r["technique_id"])
    universe_techs = set().union(*cls_universe.values()) if cls_universe else set()
    yours = set(counts) & universe_techs
    cls_items = [{**entry(fw, c, w), "hit_count": len(w["any"]),
                  "universe_count": len(cls_universe.get((fw, c), ()))}
                 for (fw, c), w in classes]
    dis, base, low = split_by_lift(cls_items, len(yours), len(universe_techs),
                                   min_support, threshold)
    return ({"scored_capabilities": [entry(fw, c, w) for (fw, c), w in scored[:top]],
             "control_classes_distinctive": dis[:top],
             "control_classes_baseline": base[:top],
             "control_classes_low_support": low[:top]},
            unaddressed, moves)


def lift_of(hit, yours, covers, universe):
    """How over-represented a control is in THIS threat set versus ATT&CK overall.

    An analyst does not brief basic hygiene. "User Account Management" maps to 20% of
    every technique MITRE publishes, so it lands at the top of any breadth ranking for
    any input, and says nothing about the threat just analysed. Lift divides the share
    of YOUR techniques a control covers by the share of ALL techniques it covers:

        ~1.0  covers your set at the same rate it covers everything  -> baseline
        >1.5  over-represented in your set                           -> distinctive

    Distinctive is not "more important". Baseline controls are usually the ones you
    must have; they are simply not NEWS, and they are not evidence about this threat.
    """
    if not yours or not covers or not universe:
        return None
    return (hit / yours) / (covers / universe)


def split_by_lift(items, yours, universe, min_support, threshold):
    """items: list of dicts carrying 'hit_count' and 'universe_count'. Returns
    (distinctive, baseline, unranked) with lift attached, best-first."""
    distinctive, baseline, unranked = [], [], []
    for it in items:
        l = lift_of(it["hit_count"], yours, it["universe_count"], universe)
        if l is None or it["hit_count"] < min_support:
            # Too few of the supplied techniques to rank honestly. A control matching
            # one technique can show enormous lift on a tiny denominator.
            unranked.append({**it, "lift": round(l, 2) if l else None,
                             "note": f"below min-support ({min_support}); lift not reliable"})
            continue
        rec = {**it, "lift": round(l, 2)}
        (distinctive if l >= threshold else baseline).append(rec)
    distinctive.sort(key=lambda x: -x["lift"])
    baseline.sort(key=lambda x: -x["hit_count"])
    unranked.sort(key=lambda x: -x["hit_count"])
    return distinctive, baseline, unranked


def mitigations_for(techs, top=15, min_support=3, threshold=1.5):
    """ATT&CK's own mitigations, ranked by coverage of the supplied techniques.

    Preferred over the NIST list when the question is "what should I implement".
    NIST rows in the workbook carry an id and a name and NOTHING else: no control
    text, no enhancements, no protect/detect/respond split. "SI-04 System Monitoring"
    is a family label standing in for dozens of distinct behaviours. ATT&CK
    mitigations are narrower and ship MITRE's own definition, so a reader can act on
    them without a second lookup.
    """
    data = load_attack("mitigations")["mitigations"]
    counts, moves = normalise(techs)
    universe = set()
    for m in data.values():
        universe |= set(m["techniques"])
    yours = set(counts) & universe

    out = []
    for code, m in data.items():
        cov = set(m["techniques"])
        hit = sorted(cov & yours)
        if hit:
            out.append({
                "mitigation_id": code, "name": m["name"],
                "description": m["description"],
                "techniques_covered": hit,
                "hit_count": len(hit),
                "universe_count": len(cov),
                "observed_events_covered": sum(counts[t] for t in hit),
            })
    dis, base, unranked = split_by_lift(out, len(yours), len(universe),
                                        min_support, threshold)
    uncovered = sorted(set(counts) - universe)
    return ({"distinctive": dis[:top], "baseline": base[:top], "low_support": unranked[:top]},
            uncovered, moves,
            {"your_techniques_mapped": len(yours), "attack_universe": len(universe),
             "min_support": min_support, "lift_threshold": threshold})


def telemetry_for(techs, top=20):
    """What to actually collect and correlate, from MITRE's detection strategies.

    This is the answer to "System Monitoring is too broad": it resolves a control
    family into named log sources and concrete detection logic per technique.
    """
    data = load_attack("telemetry")["telemetry"]
    counts, moves = normalise(techs)
    weight, chan = collections.Counter(), collections.Counter()
    per_tech, no_cover = {}, []
    for tid, n in counts.most_common():
        items = data.get(tid)
        if not items:
            no_cover.append(tid)
            continue
        per_tech[tid] = {"count": n, "detections": items[:3]}
        for it in items:
            for ls in it["log_sources"]:
                weight[ls["source"]] += n
                if ls.get("channel"):
                    chan[(ls["source"], ls["channel"])] += n
    return ({"log_sources_ranked": [{"source": s, "weight": w} for s, w in weight.most_common(top)],
             "channels_ranked": [{"source": s, "channel": c, "weight": w}
                                 for (s, c), w in chan.most_common(top)],
             "per_technique": per_tech,
             "techniques_without_published_detection": no_cover}, moves)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--controls", help="customer control baseline CSV. Omit to get "
                                       "recommendations instead of a coverage assessment")
    ap.add_argument("--top", type=int, default=25,
                    help="how many controls to recommend (default 25)")
    ap.add_argument("--mitigations", action="store_true",
                    help="recommend ATT&CK mitigations (M-codes) with MITRE's own text, "
                         "instead of NIST families which carry no description")
    ap.add_argument("--min-support", type=int, default=3,
                    help="a control must cover at least this many of the supplied "
                         "techniques before its lift is treated as reliable (default 3)")
    ap.add_argument("--lift-threshold", type=float, default=1.5,
                    help="lift at or above this is 'distinctive to this threat'; below "
                         "it is baseline hygiene that applies to everything (default 1.5)")
    ap.add_argument("--telemetry", action="store_true",
                    help="what to collect and correlate: named log sources and MITRE "
                         "detection logic per technique")
    ap.add_argument("--techniques", required=True,
                    help="JSON file of techniques, or a comma-separated ATT&CK ID list")
    ap.add_argument("--techniques-format", default="auto", choices=["auto"])
    ap.add_argument("--mapping", help="override path to master_mapping.json")
    ap.add_argument("--out", help="write JSON here instead of stdout")
    a = ap.parse_args()

    mapping = load_mapping(a.mapping)
    techs = load_techniques(a.techniques, a.techniques_format)

    if a.mitigations or a.telemetry:
        res = {"mode": [], "summary": {"techniques_supplied": len(techs)}}
        if a.mitigations:
            recs, uncovered, moves, stats = mitigations_for(
                techs, a.top, a.min_support, a.lift_threshold)
            res["mode"].append("mitigations")
            res["summary"]["distinctive_to_this_threat"] = len(recs["distinctive"])
            res["summary"]["baseline_hygiene"] = len(recs["baseline"])
            res["summary"]["techniques_no_mitigation"] = len(uncovered)
            res["summary"]["revoked_ids_remapped"] = moves
            res["summary"]["low_support"] = len(recs["low_support"])
            res["summary"]["lift_basis"] = stats
            if not recs["distinctive"] and not recs["baseline"] and recs["low_support"]:
                res["summary"]["note"] = (
                    f"No control covered at least {a.min_support} of the "
                    f"{len(techs)} supplied techniques, so nothing could be ranked by "
                    f"lift and everything is in mitigations_low_support. This is normal "
                    f"for a small technique set. Lower --min-support to rank anyway, "
                    f"accepting that lift on a tiny denominator is noisy.")
            res["mitigations_distinctive"] = recs["distinctive"]
            res["mitigations_baseline"] = recs["baseline"]
            res["mitigations_low_support"] = recs["low_support"]
            res["techniques_without_mitigation"] = uncovered
        if a.telemetry:
            tel, moves = telemetry_for(techs, a.top)
            res["mode"].append("telemetry")
            res["summary"]["log_sources_ranked"] = len(tel["log_sources_ranked"])
            res["summary"]["techniques_without_published_detection"] = \
                len(tel["techniques_without_published_detection"])
            res["summary"].setdefault("revoked_ids_remapped", moves)
            res["telemetry"] = tel
        res["caveats"] = [
            "MITRE ATT&CK text, carried unchanged. Prefer this over the NIST families: "
            "the workbook holds an id and a name for those and nothing else, so a NIST "
            "recommendation cannot tell a reader what to actually do.",
            "Log-source weights count how often a technique was observed in YOUR input, "
            "not how effective the telemetry is. A high weight means 'relevant to a lot "
            "of what you are seeing', not 'will catch it'.",
            "Detection logic is a starting point for a rule, not a rule. Tune to the "
            "estate before deploying, and expect false positives on the correlations.",
            "Absence of a published detection strategy is absence of MITRE guidance, "
            "not proof a technique is undetectable.",
            "'Distinctive' means over-represented in THIS threat set relative to ATT&CK "
            "overall. It does NOT mean more important. Baseline controls are usually the "
            "ones you must have first; they are simply not evidence about this threat, "
            "which is why an analyst brief leads with the distinctive list and assumes "
            "the baseline.",
        ]
        out = json.dumps(res, indent=1)
        if a.out:
            open(a.out, "w", encoding="utf-8").write(out)
            print(f"wrote {a.out}  [{'+'.join(res['mode'])}]")
        else:
            print(out)
        return

    if not a.controls:
        recs, unaddressed, moves = recommend(techs, mapping, a.top,
                                             a.min_support, a.lift_threshold)
        res = {
            "mode": "recommend",
            "question": "which controls does the public evidence base say address "
                        "these techniques",
            "summary": {
                "techniques_supplied": len(techs),
                "scored_capabilities_returned": len(recs["scored_capabilities"]),
                "control_classes_distinctive": len(recs["control_classes_distinctive"]),
                "control_classes_baseline": len(recs["control_classes_baseline"]),
                "techniques_no_control_addresses": len(unaddressed),
                "revoked_ids_remapped": moves,
            },
            "recommended_scored_capabilities": recs["scored_capabilities"],
            "recommended_control_classes_distinctive": recs["control_classes_distinctive"],
            "recommended_control_classes_baseline": recs["control_classes_baseline"],
            "recommended_control_classes_low_support": recs["control_classes_low_support"],
            "techniques_no_control_addresses": unaddressed,
            "caveats": [
                "This is what the evidence base says SHOULD address these techniques. It "
                "is not a statement about what you have, nor about whether yours are "
                "configured and enforced.",
                "A CTID 'significant' score describes ONE vendor capability, never the "
                "generic control class. Name the product when quoting it.",
                "Ranking counts techniques covered, not risk reduced. A control high on "
                "this list still needs your own judgement on cost and fit.",
                "Two lists, because the evidence differs in kind. 'Scored capabilities' "
                "are the four cloud stacks CTID rates for strength, so they are ranked by "
                "significant coverage. 'Control classes' are NIST 800-53 and ATT&CK "
                "mitigations, which assert relevance with NO strength claim, so they are "
                "ranked by breadth only. Do not read the second list as weaker controls: "
                "read it as controls nobody has scored.",
                "Supply --controls to turn this into a gap assessment against what you "
                "actually run.",
            ],
        }
        out = json.dumps(res, indent=1)
        if a.out:
            open(a.out, "w", encoding="utf-8").write(out)
            print(f"wrote {a.out}\n  {len(recs['scored_capabilities'])} scored "
                  f"capabilities + {len(recs['control_classes'])} control classes "
                  f"for {len(techs)} techniques")
        else:
            print(out)
        return

    controls = load_controls(a.controls)
    buckets, control_status, moves = join(controls, techs, mapping)

    unmapped = [c for c in control_status if not c["maps"]]
    result = {
        "summary": {
            "controls_supplied": len(control_status),
            "controls_joining_to_mapping": sum(1 for c in control_status if c["maps"]),
            "controls_not_mapping": len(unmapped),
            "techniques_assessed": sum(len(v) for v in buckets.values()),
            "addressed_significant": len(buckets["significant"]),
            "addressed_weakly": len(buckets["weak"]),
            "actionable_gaps": len(buckets["gap"]),
            "no_control_exists_anywhere": len(buckets["no_control_exists"]),
            "revoked_ids_remapped": moves,
        },
        "buckets": buckets,
        "controls_not_mapping": unmapped,
        "control_status": control_status,
        "caveats": [
            "A CTID 'significant' score describes ONE vendor capability, never the generic "
            "control class. Say which product when quoting it.",
            "'coverage-only' means a body asserts relevance with NO strength claim. It is not "
            "partial protection.",
            "Absence of a mapping is absence of evidence, not evidence of ineffectiveness.",
            "no_control_exists_anywhere is NOT a customer gap. Reporting it as one overstates "
            "the finding: no control programme could close it.",
            "Scores are point-in-time expert judgement. Purple-team or BAS results for the "
            "specific environment supersede them.",
        ],
    }
    out = json.dumps(result, indent=1)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(out)
        s = result["summary"]
        print(f"wrote {a.out}\n"
              f"  controls {s['controls_joining_to_mapping']}/{s['controls_supplied']} joined\n"
              f"  significant {s['addressed_significant']} | weak {s['addressed_weakly']} | "
              f"gaps {s['actionable_gaps']} | no-control-anywhere "
              f"{s['no_control_exists_anywhere']}")
    else:
        print(out)


if __name__ == "__main__":
    main()
