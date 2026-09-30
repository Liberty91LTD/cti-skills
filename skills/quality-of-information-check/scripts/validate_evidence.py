#!/usr/bin/env python3
"""
validate_evidence.py — check a Quality of Information output against the evidence
item schema and the grading caps.

Deterministic. Standard library only. This is the enforcement point: /quality-control
runs it before any human-judgement review, and /ach and /threat-assessment treat
evidence that does not pass as ungraded.

Usage:
  validate_evidence.py <qoi.json> [--source-text FILE ...] [--claims-only]
                                  [--allow-claim-count] [--today YYYY-MM-DD]

  <qoi.json>           the JSON envelope emitted by /quality-of-information-check,
                       or the claim list emitted by /claim-extraction (--claims-only)
  --source-text FILE   text of a source document; repeatable. When given, every
                       anchor must appear verbatim in one of them (whitespace and
                       quote style are normalised before comparison)
  --claims-only        validate claim_id, claim, claim_type and anchor only
  --allow-claim-count  the user asked for a focus or an exhaustive extraction,
                       so the five-to-twelve range does not apply

Exit codes:
  0  valid (warnings may be present)
  1  violations found
  2  usage error or unreadable input

Output: JSON on stdout: {"valid": bool, "violations": [...], "warnings": [...]}

Schema: references/evidence-item-schema.md. Caps: references/grading-rubric.md.
"""

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

CLAIM_TYPES = {"observation", "attribution", "assessment", "actor_claim", "victim_disclosure"}
SOURCE_TYPES = {"vendor", "government", "victim", "actor", "researcher", "press",
                "first_party", "unknown"}
ACCESS = {"telemetry", "ir_engagement", "sample_analysis", "osint", "actor_statement",
          "victim_statement", "statement", "undisclosed"}
INTEREST = {"commercial", "governmental", "victim", "actor", "independent"}
FIDELITY = {"faithful", "embellished", "caveats_dropped", "not_carried", "unresolved"}
# The evidence grade has two written elements. It is not the Admiralty scale and uses
# none of its letters or numbers. Both lists run from strongest to weakest.
ACCESS_LEVEL = ["direct", "limited", "indirect", "untraced", "adversary"]
CLAIM_SUPPORT = ["established", "firm", "tentative", "disputed", "unverified"]
LOWERS_FOOTING = {"untraced", "adversary"}       # with flag source_record_disputed
TRACK_RECORD = {"none", "boundary_up", "boundary_down"}
CORROBORATION_BASIS = {"platform", "script", "lookups", "unchecked"}
ALIAS_SOURCE = {"user", "liberty91", "none"}
PROVENANCE_BASIS = ["first-party", "platform-resolved", "script-resolved", "model-judged"]  # best to worst
FLAGS = {"single_source", "unresolved_provenance", "commercial_interest", "actor_sourced",
         "caveats_dropped_in_chain", "press_originated", "retracted", "superseded", "stale",
         "deception_indicators_present", "disputed", "derived_from_confidence",
         "source_record_disputed"}

# Best access level each kind of access can support (grading rubric, access table).
ACCESS_CEILING = {"telemetry": "direct", "ir_engagement": "direct",
                  "victim_statement": "direct", "sample_analysis": "limited",
                  "statement": "limited", "osint": "indirect", "undisclosed": "indirect",
                  "actor_statement": "adversary"}

SCALE_WORDS = re.compile(
    r"\b\d[\d,.]*\s*(?:GB|TB|MB|PB|gigabytes?|terabytes?|records?|victims?|organi[sz]ations?|"
    r"customers?|users?|accounts?|files?|documents?|million|billion)\b", re.IGNORECASE)
# A second clause: a conjunction, then a new subject (up to four words), then a verb.
# "X and Y were unsuccessful" is one assertion about two objects and does not match,
# because nothing stands between the conjunction's noun phrase and the first verb
# except the shared subject. "X was deleted and the actor then stole Y" matches.
_VERB = (r"(?:was|were|is|are|has|have|had|did|used|deployed|stole|exfiltrated|exploited|"
         r"attributed|deleted|installed|targeted|compromised|collected|observed|attempted|"
         r"failed|blocked|sent|ran|executed|created|obtained|accessed|moved)")
COMPOUND = re.compile(
    r";\s"
    r"|\b" + _VERB + r"\b[^.;]{0,80}?,?\s\b(?:and|but|while|whereas|although)\b\s"
    r"(?:(?!\b(?:and|but|or)\b)[\w'/-]+\s){0,4}?\b" + _VERB + r"\b",
    re.IGNORECASE)
ISO_DATE = re.compile(r"^\d{4}-\d{2}(-\d{2})?$")


def normalise(text):
    text = (text.replace("“", '"').replace("”", '"')
                .replace("‘", "'").replace("’", "'")
                .replace("–", "-").replace("—", "-").replace(" ", " "))
    return " ".join(text.split()).lower()


def level_better(a, b):
    """True when access level a is stronger than b."""
    return ACCESS_LEVEL.index(a) < ACCESS_LEVEL.index(b)


def support_rank(value):
    """1 (established) to 5 (unverified). Lower is stronger."""
    return CLAIM_SUPPORT.index(value) + 1


class Checker:
    def __init__(self, sources, today):
        self.sources = [normalise(s) for s in sources]
        self.today = today
        self.violations = []
        self.warnings = []

    def fail(self, claim_id, rule, message):
        self.violations.append({"claim_id": claim_id, "rule": rule, "message": message})

    def warn(self, claim_id, rule, message):
        self.warnings.append({"claim_id": claim_id, "rule": rule, "message": message})

    def enum(self, cid, field, value, allowed, required=True):
        if value is None or value == "":
            if required:
                self.fail(cid, "schema", f"{field} is missing")
            return False
        if value not in allowed:
            self.fail(cid, "schema", f"{field} is '{value}'; must be one of {sorted(map(str, allowed))}")
            return False
        return True

    # --- claim + anchor ---------------------------------------------------------------
    def claim(self, item, index):
        cid = item.get("claim_id") or f"#{index + 1}"
        if not item.get("claim_id"):
            self.fail(cid, "schema", "claim_id is missing")
        claim = item.get("claim")
        if not claim or not str(claim).strip():
            self.fail(cid, "schema", "claim is missing")
        elif COMPOUND.search(claim):
            self.warn(cid, "atomicity", "claim may contain two assertions; check it is atomic")
        self.enum(cid, "claim_type", item.get("claim_type"), CLAIM_TYPES)
        anchor = item.get("anchor") or {}
        sentence = anchor.get("sentence")
        if not sentence or not str(sentence).strip():
            self.fail(cid, "anchor", "anchor.sentence is missing: every claim needs a verbatim anchor")
        elif self.sources and (item.get("primary_source") or {}).get("type") != "first_party":
            needle = normalise(sentence).strip('"')
            if not any(needle in s for s in self.sources):
                self.fail(cid, "anchor", "anchor.sentence does not appear verbatim in the source text")
        if not anchor.get("location"):
            self.warn(cid, "anchor", "anchor.location is missing")
        return cid

    # --- full evidence item -----------------------------------------------------------
    def item(self, item, index):
        cid = self.claim(item, index)
        ctype = item.get("claim_type")
        flags = item.get("flags")
        if not isinstance(flags, list):
            self.fail(cid, "schema", "flags must be a list")
            flags = []
        for f in flags:
            if f not in FLAGS:
                self.fail(cid, "schema", f"unknown flag '{f}'")
        flags = set(flags)

        basis = item.get("provenance_basis")
        self.enum(cid, "provenance_basis", basis, PROVENANCE_BASIS)

        primary = item.get("primary_source") or {}
        if not isinstance(item.get("primary_source"), dict):
            self.fail(cid, "schema", "primary_source is missing")
        self.enum(cid, "primary_source.type", primary.get("type"), SOURCE_TYPES)
        access_ok = self.enum(cid, "primary_source.access", primary.get("access"), ACCESS)
        self.enum(cid, "primary_source.interest", primary.get("interest"), INTEREST,
                  required=bool(primary.get("org")))
        if not primary.get("stated_confidence"):
            self.fail(cid, "schema", 'primary_source.stated_confidence is missing; use the verbatim '
                                     'language or "not stated"')
        # An attributed quote has no document to link: the named organisation is the primary.
        quoted = primary.get("access") == "statement" and bool(primary.get("org"))
        first_party = primary.get("type") == "first_party"
        unresolved = ((not primary.get("url") and not quoted and not first_party)
                      or "unresolved_provenance" in flags)
        press_originated = "press_originated" in flags

        chain = item.get("chain")
        if not isinstance(chain, list) or (not chain and not first_party):
            self.fail(cid, "schema", "chain is missing or empty")
        if not isinstance(chain, list):
            chain = []
        for n, hop in enumerate(chain):
            self.enum(cid, f"chain[{n}].fidelity", (hop or {}).get("fidelity"), FIDELITY)
        dropped = any((h or {}).get("fidelity") in ("caveats_dropped", "embellished") for h in chain)

        grading = item.get("grading") or {}
        for old in ("source_reliability", "information_credibility"):
            if old in grading:
                self.fail(cid, "schema", f"grading.{old} is not part of the evidence grade; use "
                                         "grading.access_level and grading.claim_support")
        rel, support = grading.get("access_level"), grading.get("claim_support")
        rel_ok = self.enum(cid, "grading.access_level", rel, set(ACCESS_LEVEL))
        cred_ok = self.enum(cid, "grading.claim_support", support, set(CLAIM_SUPPORT))
        cred = support_rank(support) if cred_ok else None
        if not (grading.get("rationale") or "").strip():
            self.fail(cid, "schema", "grading.rationale is missing")
        track = grading.get("track_record_applied")
        self.enum(cid, "grading.track_record_applied", track, TRACK_RECORD)

        corr = item.get("corroboration") or {}
        n_primaries = corr.get("independent_primaries")
        cbasis = corr.get("basis")
        self.enum(cid, "corroboration.basis", cbasis, CORROBORATION_BASIS)
        self.enum(cid, "corroboration.alias_source", corr.get("alias_source"), ALIAS_SOURCE,
                  required=False)
        if not isinstance(n_primaries, int) or isinstance(n_primaries, bool) or n_primaries < 1:
            self.fail(cid, "schema", "corroboration.independent_primaries must be an integer of 1 or more")
            n_primaries = 1
        corr_sources = corr.get("sources") or []

        recency = item.get("recency") or {}
        for field in ("date_published", "date_observed"):
            value = recency.get(field)
            if value not in (None, "unknown") and not ISO_DATE.match(str(value)):
                self.warn(cid, "schema", f"recency.{field} is '{value}'; expected an ISO date or \"unknown\"")

        # --- corroboration must rest on data ----------------------------------------
        if n_primaries >= 2:
            if cbasis == "unchecked":
                self.fail(cid, "corroboration", "independent_primaries is 2 or more but basis is "
                                                "'unchecked': corroboration asserted without basis")
            if len(corr_sources) < n_primaries:
                self.fail(cid, "corroboration", f"independent_primaries is {n_primaries} but only "
                                                f"{len(corr_sources)} sources are listed")
            if basis == "model-judged" and cbasis in ("platform", "script"):
                self.fail(cid, "corroboration", "provenance is model-judged, so corroboration cannot "
                                                f"have basis '{cbasis}'")
            if "single_source" in flags:
                self.fail(cid, "flags", "single_source is set but independent_primaries is 2 or more")
        elif "single_source" not in flags and not first_party:
            self.fail(cid, "flags", "independent_primaries is 1, so flag single_source must be set")
        if cbasis == "platform" and basis != "platform-resolved":
            self.fail(cid, "corroboration", "corroboration basis 'platform' requires "
                                            "provenance_basis 'platform-resolved'")

        # --- caps (grading-rubric.md, R1 to R13) ------------------------------------
        if rel_ok and cred_ok:
            if unresolved and not press_originated:
                if "unresolved_provenance" not in flags:
                    self.fail(cid, "R1", "primary_source.url is null, so flag unresolved_provenance must be set")
                if rel != "untraced" and ctype != "actor_claim":
                    self.fail(cid, "R1", f"provenance is unresolved: access level must be untraced, not {rel}")
                if cred < 3:
                    self.fail(cid, "R1", f"provenance is unresolved: claim support is tentative at best, not {support}")
            if ctype == "actor_claim":
                if rel != "adversary":
                    self.fail(cid, "R3", f"actor claims have access level adversary, not {rel}")
                if "actor_sourced" not in flags:
                    self.fail(cid, "R3", "actor claims must carry flag actor_sourced")
                if n_primaries < 2:
                    if SCALE_WORDS.search(item.get("claim") or "") and support != "unverified":
                        self.fail(cid, "R2", "uncorroborated actor claim about scale, victim count or "
                                             f"data volume: claim support must be unverified, not {support}")
                    elif cred < 3:
                        self.fail(cid, "R3", f"uncorroborated actor claim: claim support is tentative at best, not {support}")
            if ctype in ("attribution", "assessment") and n_primaries < 2 and not first_party:
                stated = str(primary.get("stated_confidence") or "").lower()
                level = next((l for l in ("low", "moderate", "medium", "high")
                              if re.search(r"\b" + l + r"\b[- ]confidence|\bconfidence\b[^.]{0,20}\b"
                                           + l + r"\b", stated)), None)
                floor = {"high": 2 if ctype == "attribution" else 3, "moderate": 3,
                         "medium": 3, "low": 4, None: 3}[level]
                if cred < floor:
                    said = f"states {level} confidence" if level else "states no confidence level"
                    self.fail(cid, "R13", f"{ctype} on one primary that {said}: claim support is "
                                          f"{CLAIM_SUPPORT[floor - 1]} at best, not {support}")
            if ctype == "attribution" and cred < 2 and n_primaries < 2:
                self.fail(cid, "R4", "attribution cannot be established unless two independent primaries agree")
            if cred == 1 and (n_primaries < 2 or cbasis == "unchecked") and not first_party:
                self.fail(cid, "R5", "claim support established requires two or more independent "
                                     "primaries with a corroboration basis other than 'unchecked'")
            if press_originated:
                if rel != "untraced":
                    self.fail(cid, "R6", f"press_originated claims have access level untraced, not {rel}")
                if cred < 3:
                    self.fail(cid, "R6", f"press_originated claims are tentative at best, not {support}")
                if item.get("load_bearing") and not item.get("promoted_by_user"):
                    self.fail(cid, "R6", "press_originated claims are not load-bearing unless the user "
                                         "promotes them (set promoted_by_user: true)")
            if dropped and "caveats_dropped_in_chain" not in flags:
                self.fail(cid, "R7", "a hop has fidelity caveats_dropped or embellished, so flag "
                                     "caveats_dropped_in_chain must be set")
            if access_ok and not unresolved and ctype != "actor_claim":
                ceiling = ACCESS_CEILING[primary["access"]]
                if level_better(rel, ceiling):
                    self.fail(cid, "R8", f"access '{primary['access']}' supports access level "
                                         f"{ceiling} at best, not {rel}")
            if "source_record_disputed" in flags and "http" not in (grading.get("rationale") or ""):
                self.warn(cid, "record", "source_record_disputed requires a citation for the documented "
                                         "history of inaccurate claims; none found in the rationale")
        # R12: first-party observation is the top of the scale, and only that.
        if first_party:
            if ctype != "observation":
                self.fail(cid, "R12", "a first-party item must be claim_type observation")
            if primary.get("access") != "telemetry":
                self.fail(cid, "R12", "a first-party item must have access telemetry")
            if basis != "first-party":
                self.fail(cid, "R12", "a first-party item must have provenance_basis first-party")
            if rel_ok and rel != "direct":
                self.fail(cid, "R12", f"a first-party observation has access level direct, not {rel}")
            if cred_ok and cred != 1 and not (cred == 2 and "deception_indicators_present" in flags):
                self.fail(cid, "R12", "a first-party observation is established, or firm with "
                                      "deception_indicators_present where log tampering is suspected")
        elif basis == "first-party":
            self.fail(cid, "R12", "provenance_basis first-party is for observations in the user's "
                                  "own telemetry (primary_source.type first_party)")
        age = recency.get("age_days")
        start = recency.get("date_observed")
        if start in (None, "unknown"):
            start = recency.get("date_published")
        if isinstance(age, int) and isinstance(start, str) and re.match(r"^\d{4}-\d{2}-\d{2}$", start):
            expected = (self.today - dt.date.fromisoformat(start)).days
            if abs(expected - age) > 1:
                self.warn(cid, "R9", f"age_days is {age} but {start} is {expected} days before the "
                                     "assessment date; age counts from date_observed, or from "
                                     "date_published when that is unknown")
        if isinstance(age, int) and age > 180 and "stale" not in flags:
            self.warn(cid, "R9", f"claim is {age} days old; set flag stale if the topic is fast-moving")
        if track in ("boundary_up", "boundary_down") and basis != "platform-resolved":
            self.fail(cid, "R10", "a track record modifier may only be applied when provenance is "
                                  "platform-resolved")
        if "superseded" in flags and not recency.get("superseded_by"):
            self.fail(cid, "flags", "superseded is set but recency.superseded_by is empty")
        return cid

    # --- aggregate ------------------------------------------------------------------
    def aggregate(self, doc, items):
        summary = doc.get("event_qoi_summary")
        if not isinstance(summary, dict):
            self.fail(None, "aggregate", "event_qoi_summary is missing")
            return
        if summary.get("claims_graded") != len(items):
            self.fail(None, "aggregate", f"claims_graded is {summary.get('claims_graded')} but "
                                         f"{len(items)} items are present")
        bases = [i.get("provenance_basis") for i in items if i.get("provenance_basis") in PROVENANCE_BASIS]
        if bases:
            worst = max(bases, key=PROVENANCE_BASIS.index)
            for where, value in (("event_qoi_summary", summary.get("provenance_basis")),
                                 ("envelope", doc.get("provenance_basis"))):
                if value != worst:
                    self.fail(None, "aggregate", f"{where} provenance_basis is '{value}'; the worst of "
                                                 f"the items is '{worst}'")
        weakest = summary.get("weakest_link")
        ids = {i.get("claim_id"): i for i in items}
        bearing = [i for i in items if i.get("load_bearing")]
        if bearing:
            if weakest not in ids:
                self.fail(None, "aggregate", f"weakest_link '{weakest}' is not a claim_id in this run")
            elif not ids[weakest].get("load_bearing"):
                self.fail(None, "aggregate", f"weakest_link '{weakest}' is not a load-bearing claim")
            else:
                def footing(i):
                    # Footing bands from evidence-item-schema.md; lower is weaker.
                    g = i.get("grading") or {}
                    rel, support = g.get("access_level"), g.get("claim_support")
                    cred = support_rank(support) if support in CLAIM_SUPPORT else 5
                    band = {1: 3, 2: 2, 3: 1}.get(cred, 0)
                    if cred == 1 and rel == "indirect":
                        band = 2
                    if rel in LOWERS_FOOTING or "source_record_disputed" in (i.get("flags") or []):
                        band = max(band - 1, 0)
                    track = g.get("track_record_applied")
                    if track == "boundary_down":
                        band = max(band - 1, 0)
                    elif track == "boundary_up":
                        band = min(band + 1, 3)
                    order = ACCESS_LEVEL.index(rel) if rel in ACCESS_LEVEL else len(ACCESS_LEVEL)
                    return (band, -cred, -order)
                lowest = min(map(footing, bearing))
                if footing(ids[weakest]) != lowest:
                    self.fail(None, "aggregate", f"weakest_link '{weakest}' is not the lowest-graded "
                                                 "load-bearing claim")
                else:
                    tied = sorted(str(i.get("claim_id")) for i in bearing if footing(i) == lowest)
                    if len(tied) > 1 and weakest != tied[0]:
                        self.warn(None, "aggregate", f"claims {', '.join(tied)} tie as the weakest "
                                                     f"link; name the lowest claim_id ({tied[0]}) "
                                                     "and list the others with it")
        else:
            self.warn(None, "aggregate", "no claim is marked load_bearing; the weakest link cannot be checked")
        for field in ("grade_range", "summary_line", "independent_primaries"):
            if summary.get(field) in (None, ""):
                self.fail(None, "aggregate", f"event_qoi_summary.{field} is missing")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate QoI evidence items.")
    parser.add_argument("path")
    parser.add_argument("--source-text", action="append", default=[])
    parser.add_argument("--claims-only", action="store_true")
    parser.add_argument("--allow-claim-count", action="store_true")
    parser.add_argument("--today")
    args = parser.parse_args(argv)

    try:
        doc = json.loads(Path(args.path).read_text(encoding="utf-8"))
        sources = [Path(p).read_text(encoding="utf-8", errors="replace") for p in args.source_text]
    except (OSError, ValueError) as e:
        print(json.dumps({"valid": False, "error": str(e)}, indent=2))
        return 2
    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    checker = Checker(sources, today)

    if isinstance(doc, list):
        doc = {"claims" if args.claims_only else "evidence_items": doc}
    items = doc.get("claims") if args.claims_only else doc.get("evidence_items")
    if not isinstance(items, list) or not items:
        key = "claims" if args.claims_only else "evidence_items"
        print(json.dumps({"valid": False, "error": f"no '{key}' list in input"}, indent=2))
        return 2

    seen = set()
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            checker.fail(f"#{index + 1}", "schema", "item is not an object")
            continue
        cid = checker.claim(item, index) if args.claims_only else checker.item(item, index)
        if cid in seen:
            checker.fail(cid, "schema", "duplicate claim_id")
        seen.add(cid)

    primary_claims = [i for i in items if isinstance(i, dict)
                      and "press_originated" not in (i.get("flags") or [])]
    if not args.allow_claim_count and not 5 <= len(primary_claims) <= 12:
        checker.fail(None, "claim_count", f"{len(primary_claims)} claims; the range is five to twelve "
                                          "per primary unless the user asked otherwise "
                                          "(--allow-claim-count)")
    if not args.claims_only:
        if doc.get("provenance_basis") not in PROVENANCE_BASIS:
            checker.fail(None, "schema", "envelope provenance_basis is absent or invalid")
        checker.aggregate(doc, [i for i in items if isinstance(i, dict)])

    result = {"valid": not checker.violations, "items_checked": len(items),
              "anchors_checked_against_source": bool(sources),
              "violations": checker.violations, "warnings": checker.warnings}
    print(json.dumps(result, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
