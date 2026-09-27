#!/usr/bin/env python3
"""
Tests for /source-provenance and /quality-of-information-check.

Offline. Standard library only. Run from anywhere:

  python3 tests/provenance/run_tests.py

Fixtures are synthetic HTML pages with invented content, mapped to URLs in
fixtures.json. No third-party article text is stored in this repository.
"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
RESOLVER = ROOT / "skills" / "source-provenance" / "scripts" / "resolve_provenance.py"
VALIDATOR = ROOT / "skills" / "quality-of-information-check" / "scripts" / "validate_evidence.py"
SOURCE_TYPES = ROOT / "skills" / "source-provenance" / "references" / "source-types.md"
EXPECTED = json.loads((HERE / "expected-chains.json").read_text())
TODAY = "2026-09-27"


def run(script, *args):
    proc = subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def resolve(*urls, extra=()):
    code, out, err = run(RESOLVER, "resolve", "--fixtures", str(HERE / "fixtures.json"),
                         "--no-cache", "--today", TODAY, *extra, *urls)
    return code, (json.loads(out) if out.strip() else None), err


class Chains(unittest.TestCase):
    """Each fixture URL resolves to the chain recorded in expected-chains.json."""

    def test_expected_chains(self):
        for case in EXPECTED:
            with self.subTest(case=case["name"]):
                code, data, _ = resolve(case["url"])
                result = data["results"][0]
                self.assertEqual(result["status"], case["status"])
                self.assertEqual(code, 0 if case["status"] == "resolved" else 2)
                self.assertEqual(result["provenance_basis"], "script-resolved")
                self.assertEqual([h["org"] for h in result["chain"]], case["chain"])
                primary = result["primary_source"] or {}
                for field, value in case.get("primary", {}).items():
                    self.assertEqual(primary.get(field), value, field)
                if "stated_confidence_contains" in case:
                    self.assertIn(case["stated_confidence_contains"], primary["stated_confidence"])
                if "reason_contains" in case:
                    reasons = " ".join(u["reason"] for u in result["unresolved"])
                    self.assertIn(case["reason_contains"], reasons)
                self.assertEqual([o["org"] for o in result["other_primaries"]],
                                 case.get("other_primaries", []))
                self.assertEqual([o["org"] for o in result["background_references"]],
                                 case.get("background_references", []))
                if "unattributed_sourcing" in case:
                    self.assertEqual(len(result["unattributed_sourcing"]),
                                     case["unattributed_sourcing"])

    def test_fidelity_is_never_judged_by_the_script(self):
        _, data, _ = resolve(*[c["url"] for c in EXPECTED])
        for result in data["results"]:
            for hop in result["chain"]:
                self.assertIn(hop["fidelity"], (None, "unresolved"))

    def test_boilerplate_links_are_ignored(self):
        _, data, _ = resolve(EXPECTED[0]["url"])
        result = data["results"][0]
        seen = json.dumps(result)
        for marker in ("nav-link-report", "sidebar-promo-report", "footer-link"):
            self.assertNotIn(marker, seen)

    def test_undetermined_fields_are_null_with_a_reason(self):
        _, data, _ = resolve("https://thehackernews.com/2026/09/gateway-zero-day-exploited.html")
        primary = data["results"][0]["primary_source"]
        self.assertIsNone(primary["title"])
        self.assertIsNone(primary["date_published"])
        self.assertTrue(primary["null_reasons"]["title"])
        self.assertNotIn("", [v for v in primary.values() if isinstance(v, str)])

    def test_access_comes_from_the_text_not_the_table(self):
        # The vendor fixture mentions a leak site three times and its own telemetry twice.
        _, data, _ = resolve(EXPECTED[0]["url"])
        primary = data["results"][0]["primary_source"]
        self.assertEqual(primary["access"], "telemetry")
        self.assertTrue(any(e["access"] == "actor_statement" for e in primary["access_evidence"]))

    def test_output_carries_anchors_not_full_text(self):
        _, data, _ = resolve(EXPECTED[0]["url"])
        self.assertNotIn("Network defenders can find indicators", json.dumps(data))


class Limits(unittest.TestCase):
    def test_more_than_fifty_urls_is_refused(self):
        urls = [f"https://thehackernews.com/2026/09/story-{n}.html" for n in range(51)]
        code, data, err = resolve(*urls)
        self.assertEqual(code, 3)
        self.assertIsNone(data)
        self.assertIn("Liberty91 API", err)

    def test_more_than_two_hops_is_refused(self):
        code, _, _ = resolve(EXPECTED[0]["url"], extra=("--max-hops", "3"))
        self.assertEqual(code, 3)

    def test_one_hop_limit_stops_at_the_article(self):
        code, data, _ = resolve("https://gbhackers.com/embers-backdoor-water-utilities/",
                                extra=("--max-hops", "1"))
        self.assertEqual(code, 2)
        self.assertIn("hop limit", json.dumps(data["results"][0]["unresolved"]))


class SourceTable(unittest.TestCase):
    def classify(self, url):
        code, out, _ = run(RESOLVER, "classify", url)
        self.assertEqual(code, 0)
        return json.loads(out)[0]

    def test_longest_prefix_wins(self):
        self.assertEqual(self.classify("https://www.sec.gov/Archives/edgar/data/1/a.htm")["type"], "victim")
        self.assertEqual(self.classify("https://www.sec.gov/news/press-release/x")["type"], "government")

    def test_documentation_is_not_a_primary(self):
        self.assertFalse(self.classify("https://learn.microsoft.com/en-us/defender/x")["is_primary_capable"])

    def test_onion_hosts_are_actor_statements(self):
        row = self.classify("http://exampleexampleexample.onion/post/1")
        self.assertEqual((row["type"], row["access_profile"]), ("actor", "actor_statement"))

    def test_unlisted_hosts_are_unknown(self):
        self.assertEqual(self.classify("https://blog.example.org/post")["type"], "unknown")

    def test_table_has_no_reliability_column_or_grades(self):
        text = SOURCE_TYPES.read_text()
        headers = [l for l in text.splitlines() if l.startswith("| domain |")]
        self.assertTrue(headers)
        for header in headers:
            self.assertEqual(header, "| domain | organisation | type | access_profile | interest | notes |")
        for line in text.splitlines():
            if line.startswith("|") and not line.startswith(("| domain", "|---", "| Column", "| `")):
                notes = line.strip().strip("|").split("|")[-1].lower()
                for word in ("reliable", "unreliable", "trustworthy", "reputable", "track record",
                             "accurate", "inaccurate", "credible"):
                    self.assertNotIn(word, notes, line)

    def test_no_duplicate_domains(self):
        domains = [l.split("|")[1].strip() for l in SOURCE_TYPES.read_text().splitlines()
                   if l.startswith("|") and l.count("|") == 7
                   and not l.startswith(("| domain", "|---"))]
        self.assertEqual(len(domains), len(set(domains)))


class Validator(unittest.TestCase):
    def validate(self, name, *args):
        code, out, _ = run(VALIDATOR, str(HERE / "qoi" / name), "--today", TODAY, *args)
        return code, json.loads(out)

    def test_valid_run_passes_with_anchors_checked(self):
        code, result = self.validate("valid-tier2.json",
                                     "--source-text", str(HERE / "qoi" / "primary.txt"),
                                     "--source-text", str(HERE / "qoi" / "article.txt"))
        self.assertEqual(result["violations"], [])
        self.assertEqual(code, 0)
        self.assertTrue(result["anchors_checked_against_source"])

    def test_each_violation_is_caught(self):
        cases = json.loads((HERE / "qoi" / "invalid-cases.json").read_text())
        base = json.loads((HERE / "qoi" / "valid-tier2.json").read_text())
        for case in cases:
            with self.subTest(case=case["name"]):
                doc = json.loads(json.dumps(base))
                item = next(i for i in doc["evidence_items"] if i["claim_id"] == case["claim_id"])
                for path, value in case["set"].items():
                    node = item
                    keys = path.split(".")
                    for key in keys[:-1]:
                        node = node[int(key)] if key.isdigit() else node[key]
                    node[keys[-1]] = value
                tmp = HERE / "qoi" / ".tmp-case.json"
                tmp.write_text(json.dumps(doc))
                try:
                    code, result = self.validate(tmp.name, "--source-text",
                                                 str(HERE / "qoi" / "primary.txt"),
                                                 "--source-text", str(HERE / "qoi" / "article.txt"))
                finally:
                    tmp.unlink()
                self.assertEqual(code, 1)
                rules = {v["rule"] for v in result["violations"] if v["claim_id"] == case["claim_id"]}
                self.assertIn(case["rule"], rules)

    def test_weakest_link_follows_the_footing_bands(self):
        # C04 is A3 (band 1, Low). C02 regraded D3 is band 0 (no confidence level): weaker.
        doc = json.loads((HERE / "qoi" / "valid-tier2.json").read_text())
        item = next(i for i in doc["evidence_items"] if i["claim_id"] == "C02")
        item["load_bearing"] = True
        item["primary_source"]["url"] = None
        item["grading"]["source_reliability"] = "D"
        item["grading"]["information_credibility"] = 3
        item["flags"] = ["single_source", "unresolved_provenance"]
        tmp = HERE / "qoi" / ".tmp-case.json"
        results = {}
        try:
            for link in ("C04", "C02"):
                doc["event_qoi_summary"]["weakest_link"] = link
                tmp.write_text(json.dumps(doc))
                results[link] = self.validate(tmp.name)
        finally:
            tmp.unlink()
        self.assertEqual(results["C04"][0], 1)
        self.assertTrue(any("weakest_link" in v["message"] for v in results["C04"][1]["violations"]))
        self.assertEqual(results["C02"][1]["violations"], [])

    def first_party_doc(self, **changes):
        doc = json.loads((HERE / "qoi" / "valid-tier2.json").read_text())
        item = {
            "claim_id": "C10", "load_bearing": True, "claim_type": "observation",
            "claim": "203.0.113.42 was contacted by two hosts in the user's environment on 2026-09-20.",
            "anchor": {"document_url": None, "location": "lookup-sentinel, DeviceNetworkEvents, P30D",
                       "sentence": "RemoteIP == 203.0.113.42: hits=14, devices=2, first=2026-09-20"},
            "primary_source": {"org": "user environment", "type": "first_party", "title": None,
                               "date_published": None, "url": None, "access": "telemetry",
                               "stated_confidence": "not stated", "interest": "independent"},
            "chain": [],
            "grading": {"source_reliability": "A", "information_credibility": 1,
                        "rationale": "First-party observation in the user's own telemetry. R12.",
                        "track_record_applied": "none"},
            "corroboration": {"independent_primaries": 1, "basis": "unchecked", "sources": [],
                              "alias_source": "none"},
            "recency": {"date_observed": "2026-09-20", "date_published": None, "age_days": 7,
                        "superseded_by": None},
            "flags": [], "provenance_basis": "first-party",
        }
        for path, value in changes.items():
            node, keys = item, path.split(".")
            for key in keys[:-1]:
                node = node[key]
            node[keys[-1]] = value
        doc["evidence_items"].append(item)
        doc["event_qoi_summary"]["claims_graded"] = 10
        return doc

    def run_doc(self, doc, *args):
        tmp = HERE / "qoi" / ".tmp-case.json"
        tmp.write_text(json.dumps(doc))
        try:
            return self.validate(tmp.name, *args)
        finally:
            tmp.unlink()

    def test_first_party_observation_is_a1_and_participates(self):
        # A1 without a second primary, load-bearing, anchors still checked for the rest.
        code, result = self.run_doc(self.first_party_doc(),
                                    "--source-text", str(HERE / "qoi" / "primary.txt"),
                                    "--source-text", str(HERE / "qoi" / "article.txt"))
        self.assertEqual(result["violations"], [])
        self.assertEqual(code, 0)

    def test_first_party_rules_are_enforced(self):
        for changes in ({"grading.source_reliability": "B"},
                        {"grading.information_credibility": 2},
                        {"claim_type": "assessment"},
                        {"primary_source.access": "osint"},
                        {"provenance_basis": "script-resolved"}):
            with self.subTest(changes=changes):
                code, result = self.run_doc(self.first_party_doc(**changes))
                self.assertEqual(code, 1)
                self.assertIn("R12", {v["rule"] for v in result["violations"]})

    def test_first_party_label_is_refused_on_reporting(self):
        doc = json.loads((HERE / "qoi" / "valid-tier2.json").read_text())
        doc["evidence_items"][1]["provenance_basis"] = "first-party"
        code, result = self.run_doc(doc)
        self.assertEqual(code, 1)
        self.assertIn("R12", {v["rule"] for v in result["violations"]})

    def test_missing_provenance_basis_is_rejected(self):
        doc = json.loads((HERE / "qoi" / "valid-tier2.json").read_text())
        del doc["provenance_basis"]
        tmp = HERE / "qoi" / ".tmp-case.json"
        tmp.write_text(json.dumps(doc))
        try:
            code, result = self.validate(tmp.name)
        finally:
            tmp.unlink()
        self.assertEqual(code, 1)
        self.assertTrue(any("provenance_basis" in v["message"] for v in result["violations"]))

    def test_claim_count_outside_range_is_rejected(self):
        doc = json.loads((HERE / "qoi" / "valid-tier2.json").read_text())
        doc["evidence_items"] = doc["evidence_items"][:3]
        tmp = HERE / "qoi" / ".tmp-case.json"
        tmp.write_text(json.dumps(doc))
        try:
            code, result = self.validate(tmp.name)
            allowed, _ = self.validate(tmp.name, "--allow-claim-count")
        finally:
            tmp.unlink()
        self.assertEqual(code, 1)
        self.assertTrue(any(v["rule"] == "claim_count" for v in result["violations"]))


if __name__ == "__main__":
    unittest.main(verbosity=1)
