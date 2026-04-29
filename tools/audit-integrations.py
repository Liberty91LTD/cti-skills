#!/usr/bin/env python3
"""
audit-integrations.py — verify the integration set is internally consistent.

Source of truth: the catalog table at the top of `tools/REGISTRY.md`. Every
external integration in the pack is listed there with its skill name,
indicator types, and required environment variables. This auditor parses
that table and runs eight checks across the rest of the codebase to
surface drift introduced when integrations are added, renamed, removed,
or have their env vars changed.

Run:
  python3 tools/audit-integrations.py
  python3 tools/audit-integrations.py --strict      # treat WARNs as errors
  python3 tools/audit-integrations.py --json        # machine-readable
  python3 tools/audit-integrations.py --check       # exit non-zero on any FAIL

Exit codes:
  0  no FAILs (and no WARNs in --strict mode)
  1  one or more FAILs (or WARNs in --strict mode)
  2  could not parse REGISTRY.md
  3  bad arguments

The auditor never modifies files. It is read-only and safe to run from a
pre-commit hook, validate-skills.sh, or CI.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_MD = REPO_ROOT / "tools" / "REGISTRY.md"

# Composite skills that should reference lookups for the indicator types they cover.
# Mapping: composite skill -> set of indicator categories it handles.
COMPOSITE_COVERAGE = {
    "ip-investigation": {"ip"},
    "domain-investigation": {"domain"},
    "hash-investigation": {"hash"},
    "url-investigation": {"url"},
    "indicator-pivoting": {"ip", "domain", "hash", "url", "cert", "actor"},
}

# Cross-cutting lookups that should be referenced from a composite even though
# their REGISTRY indicator types don't map to ip/domain/hash/url directly. Hand
# maintained — re-evaluate when adding a new lookup of the same shape.
EXTRA_COVERAGE = {
    "ip-investigation": {"lookup-misp"},
    "domain-investigation": {"lookup-misp", "lookup-ransomwarelive"},
    "hash-investigation": {"lookup-misp"},
    "url-investigation": {"lookup-misp"},
    "indicator-pivoting": {"lookup-misp", "lookup-ransomwarelive"},
}

# Env vars documented in REGISTRY.md only as legacy/fallback. Skip them when
# checking cti-setup and scripts/setup.sh coverage — the canonical-supported
# auth path is sufficient.
LEGACY_ENVS = {
    "CENSYS_API_ID",
    "CENSYS_API_SECRET",
}

# Indicator labels in REGISTRY.md catalog rows -> normalised category.
INDICATOR_NORMALISE = {
    "ip": "ip", "ips": "ip",
    "domain": "domain", "domains": "domain", "hostname": "domain",
    "hash": "hash", "hashes": "hash", "file": "hash",
    "url": "url", "urls": "url",
    "cert": "cert", "certs": "cert", "certificate": "cert",
    "search query": None,
    "events": None, "attributes": None, "objects": None, "stix 2 bundles": None,
    "victim": None, "group": None, "sector": None, "country": None,
    "iocs": None, "yara": None,
}

# Where the canonical "tell the user about every integration" tables live.
VERSIONS_MD = REPO_ROOT / "VERSIONS.md"
CTI_SETUP_MD = REPO_ROOT / "skills" / "cti-setup" / "SKILL.md"
SETUP_SH = REPO_ROOT / "scripts" / "setup.sh"

CARDINALITY_NUMS = {
    "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
    "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "thirteen": 13, "fourteen": 14, "fifteen": 15,
}
CARDINALITY_RE = re.compile(
    r"\bthe\s+(" + "|".join(CARDINALITY_NUMS) + r")\s+(integrations|services|lookups|external\s+threat[- ]intel(ligence)?\s+integrations|external\s+(api|apis))\b",
    re.IGNORECASE,
)

LOOKUP_DIR_RE = re.compile(r"^lookup-([a-z0-9-]+)$")
LOOKUP_REF_RE = re.compile(r"/lookup-([a-z0-9-]+)\b")
AGENT_REF_RE = re.compile(r"\b([a-z0-9-]+)-agent\b")


# ---------- registry parsing ----------

def parse_registry():
    """Return list of dicts: {api, skill, env_vars: [...], indicators: [...]}.
    Parses the first markdown table whose header has Skill | Env variable(s) | Indicators."""
    if not REGISTRY_MD.exists():
        return None
    text = REGISTRY_MD.read_text(encoding="utf-8")
    lines = text.splitlines()
    rows = []
    in_table = False
    header_idx = None
    for i, ln in enumerate(lines):
        if "|" in ln and re.search(r"\bSkill\b.*\bEnv variable", ln, re.IGNORECASE):
            in_table = True
            header_idx = i
            continue
        if in_table:
            if not ln.strip().startswith("|"):
                in_table = False
                continue
            if re.match(r"^\|[\s\-:|]+\|$", ln.strip()):
                continue  # separator row
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) < 6:
                continue
            api_cell, skill_cell, env_cell, indicator_cell = cells[0], cells[1], cells[2], cells[3]
            api = re.sub(r"\[([^\]]+)\].*", r"\1", api_cell).strip()
            skill_match = re.search(r"`/lookup-([a-z0-9-]+)`", skill_cell)
            if not skill_match:
                continue
            skill = "lookup-" + skill_match.group(1)
            env_vars = re.findall(r"`([A-Z][A-Z0-9_]+)`", env_cell)
            indicator_tokens = []
            for token in re.split(r"[,/]", indicator_cell):
                token = token.strip().lower()
                if token in INDICATOR_NORMALISE:
                    norm = INDICATOR_NORMALISE[token]
                    if norm:
                        indicator_tokens.append(norm)
            rows.append({
                "api": api,
                "skill": skill,
                "env_vars": env_vars,
                "indicators": sorted(set(indicator_tokens)),
            })
    return rows


# ---------- finding helpers ----------

def all_skill_md():
    return sorted((REPO_ROOT / "skills").rglob("SKILL.md"))

def grep_files(pattern, files, ignore_case=False):
    """Yield (path, lineno, line) tuples."""
    flags = re.IGNORECASE if ignore_case else 0
    rx = re.compile(pattern, flags) if isinstance(pattern, str) else pattern
    for fp in files:
        try:
            for n, line in enumerate(fp.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                if rx.search(line):
                    yield fp, n, line.rstrip()
        except OSError:
            continue


# ---------- checks ----------

class Finding:
    __slots__ = ("level", "check", "message", "where")
    def __init__(self, level, check, message, where=""):
        self.level = level   # FAIL | WARN | INFO
        self.check = check
        self.message = message
        self.where = where
    def to_dict(self):
        return {"level": self.level, "check": self.check, "message": self.message, "where": self.where}


def check_registry_disk_match(catalog, findings):
    """Every skills/lookup-* dir must be in the catalog, and vice versa."""
    on_disk = set()
    for d in (REPO_ROOT / "skills").iterdir():
        if d.is_dir():
            m = LOOKUP_DIR_RE.match(d.name)
            if m:
                on_disk.add(d.name)
    in_catalog = {row["skill"] for row in catalog}

    for missing in sorted(in_catalog - on_disk):
        findings.append(Finding("FAIL", "registry-disk-match",
            f"REGISTRY.md lists `{missing}` but `skills/{missing}/` does not exist"))
    for orphan in sorted(on_disk - in_catalog):
        findings.append(Finding("FAIL", "registry-disk-match",
            f"`skills/{orphan}/` exists but is not listed in REGISTRY.md catalog table"))


def check_integration_guides(catalog, findings):
    """Every catalog row must have a tools/integrations/<api>.md file."""
    integrations_dir = REPO_ROOT / "tools" / "integrations"
    for row in catalog:
        slug = row["skill"][len("lookup-"):]
        if not (integrations_dir / f"{slug}.md").exists():
            findings.append(Finding("FAIL", "integration-guide-exists",
                f"`tools/integrations/{slug}.md` missing for `{row['skill']}`"))


def check_clis_exist(catalog, findings):
    """Every catalog row must have at least one CLI under tools/clis/<api>.{py,js}."""
    clis_dir = REPO_ROOT / "tools" / "clis"
    for row in catalog:
        slug = row["skill"][len("lookup-"):]
        candidates = [clis_dir / f"{slug}.py", clis_dir / f"{slug}.js"]
        if not any(c.exists() for c in candidates):
            findings.append(Finding("FAIL", "cli-exists",
                f"no CLI for `{row['skill']}` (expected `tools/clis/{slug}.py` or `.js`)"))


def check_versions_md(catalog, findings):
    """Every catalog skill must appear in VERSIONS.md skills tables."""
    if not VERSIONS_MD.exists():
        findings.append(Finding("FAIL", "versions-md", "VERSIONS.md missing"))
        return
    text = VERSIONS_MD.read_text(encoding="utf-8")
    for row in catalog:
        if f"`{row['skill']}`" not in text:
            findings.append(Finding("FAIL", "versions-md",
                f"`{row['skill']}` missing from VERSIONS.md"))


def check_cti_setup_envvars(catalog, findings):
    """Every non-legacy env var in the catalog must appear in skills/cti-setup/SKILL.md."""
    if not CTI_SETUP_MD.exists():
        findings.append(Finding("FAIL", "cti-setup", "skills/cti-setup/SKILL.md missing"))
        return
    text = CTI_SETUP_MD.read_text(encoding="utf-8")
    for row in catalog:
        for env in row["env_vars"]:
            if env in LEGACY_ENVS:
                continue
            if env not in text:
                findings.append(Finding("WARN", "cti-setup",
                    f"`{env}` (for `{row['skill']}`) not mentioned in `skills/cti-setup/SKILL.md`"))


def check_setup_sh_envvars(catalog, findings):
    """Every non-legacy env var should also be wired into scripts/setup.sh."""
    if not SETUP_SH.exists():
        findings.append(Finding("WARN", "setup-sh", "scripts/setup.sh missing"))
        return
    text = SETUP_SH.read_text(encoding="utf-8")
    for row in catalog:
        for env in row["env_vars"]:
            if env in LEGACY_ENVS:
                continue
            if env not in text:
                findings.append(Finding("WARN", "setup-sh",
                    f"`{env}` (for `{row['skill']}`) not handled by `scripts/setup.sh`"))


def check_dead_agent_refs(catalog, findings):
    """Every `<x>-agent` token in skills/ must NOT collide with a current lookup name.
    Catches stale references to retired *-agent agents."""
    current_apis = {row["skill"][len("lookup-"):] for row in catalog}
    for fp, n, line in grep_files(AGENT_REF_RE, all_skill_md()):
        for m in AGENT_REF_RE.finditer(line):
            api = m.group(1)
            if api in current_apis:
                findings.append(Finding("FAIL", "dead-agent-refs",
                    f"`{api}-agent` is a retired name; use `/lookup-{api}` instead",
                    where=f"{fp.relative_to(REPO_ROOT)}:{n}"))


def check_unknown_lookup_refs(catalog, findings):
    """Every `/lookup-X` reference across the whole repo must point to a current skill
    or be in an explicit retired-list comment."""
    current = {row["skill"] for row in catalog}
    targets = sorted(REPO_ROOT.rglob("*.md")) + sorted(REPO_ROOT.rglob("*.py")) + sorted(REPO_ROOT.rglob("*.js")) + sorted(REPO_ROOT.rglob("*.sh"))
    targets = [t for t in targets if "/.git/" not in str(t) and "/archive/" not in str(t)]
    for fp in targets:
        try:
            text = fp.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for n, line in enumerate(text.splitlines(), 1):
            for m in LOOKUP_REF_RE.finditer(line):
                ref = "lookup-" + m.group(1)
                if ref not in current:
                    findings.append(Finding("FAIL", "unknown-lookup-ref",
                        f"reference to `/{ref}` but no such skill exists",
                        where=f"{fp.relative_to(REPO_ROOT)}:{n}"))


def check_composite_coverage(catalog, findings):
    """Each composite skill should reference every catalog lookup whose indicator
    type the composite covers."""
    by_indicator = {}
    for row in catalog:
        for ind in row["indicators"]:
            by_indicator.setdefault(ind, []).append(row["skill"])

    for composite, indicators in COMPOSITE_COVERAGE.items():
        composite_path = REPO_ROOT / "skills" / composite / "SKILL.md"
        if not composite_path.exists():
            findings.append(Finding("WARN", "composite-coverage",
                f"composite skill `{composite}` listed but not on disk"))
            continue
        text = composite_path.read_text(encoding="utf-8")
        expected = set()
        for ind in indicators:
            for skill in by_indicator.get(ind, []):
                expected.add(skill)
        expected |= EXTRA_COVERAGE.get(composite, set())
        for skill in sorted(expected):
            if f"/{skill}" not in text:
                findings.append(Finding("WARN", "composite-coverage",
                    f"`{composite}` does not reference `/{skill}` (expected by indicator-type or EXTRA_COVERAGE rule)"))


def check_cardinality(catalog, findings):
    """Flag hardcoded 'the seven services' / 'the nine integrations' phrases.

    Skips occurrences inside `backticks` (illustrative examples) and inside
    fenced code blocks (which are also illustrative)."""
    current_count = len(catalog)
    targets = list(REPO_ROOT.rglob("*.md"))
    targets = [t for t in targets if "/.git/" not in str(t) and "/archive/" not in str(t) and "/data/" not in str(t)]
    for fp in targets:
        try:
            text = fp.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        in_fence = False
        for n, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for m in CARDINALITY_RE.finditer(line):
                # Skip if the match is inside a backtick span on this line
                start, end = m.span()
                ticks_before = line[:start].count("`")
                ticks_inside = line[start:end].count("`")
                if (ticks_before % 2) == 1 and ticks_inside == 0:
                    continue
                num_word = m.group(1).lower()
                stated = CARDINALITY_NUMS[num_word]
                if stated != current_count:
                    findings.append(Finding("WARN", "cardinality",
                        f"hardcoded `the {num_word}` (= {stated}) but catalog has {current_count}",
                        where=f"{fp.relative_to(REPO_ROOT)}:{n}"))


# ---------- driver ----------

def emit_text(findings):
    by_level = {"FAIL": [], "WARN": [], "INFO": []}
    for f in findings:
        by_level[f.level].append(f)
    for level in ("FAIL", "WARN", "INFO"):
        for f in by_level[level]:
            loc = f"  {f.where}" if f.where else ""
            print(f"{level:4}  [{f.check}] {f.message}{loc}")
    print(f"\nsummary: {len(by_level['FAIL'])} FAIL, {len(by_level['WARN'])} WARN, {len(by_level['INFO'])} INFO")


def emit_json(findings, catalog_count):
    print(json.dumps({
        "catalog_count": catalog_count,
        "findings": [f.to_dict() for f in findings],
        "summary": {
            "fail": sum(1 for f in findings if f.level == "FAIL"),
            "warn": sum(1 for f in findings if f.level == "WARN"),
            "info": sum(1 for f in findings if f.level == "INFO"),
        }
    }, indent=2))


def main():
    ap = argparse.ArgumentParser(prog="audit-integrations.py", description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--strict", action="store_true", help="treat WARN as failure")
    ap.add_argument("--json", dest="as_json", action="store_true", help="emit JSON instead of text")
    ap.add_argument("--check", action="store_true",
                    help="exit non-zero on any FAIL (default behaviour even without --check)")
    args = ap.parse_args()

    catalog = parse_registry()
    if catalog is None:
        print(f"error: could not parse {REGISTRY_MD}", file=sys.stderr)
        sys.exit(2)
    if not catalog:
        print(f"error: no rows parsed from {REGISTRY_MD} catalog table", file=sys.stderr)
        sys.exit(2)

    findings = []
    check_registry_disk_match(catalog, findings)
    check_integration_guides(catalog, findings)
    check_clis_exist(catalog, findings)
    check_versions_md(catalog, findings)
    check_cti_setup_envvars(catalog, findings)
    check_setup_sh_envvars(catalog, findings)
    check_dead_agent_refs(catalog, findings)
    check_unknown_lookup_refs(catalog, findings)
    check_composite_coverage(catalog, findings)
    check_cardinality(catalog, findings)

    if args.as_json:
        emit_json(findings, len(catalog))
    else:
        emit_text(findings)

    fails = sum(1 for f in findings if f.level == "FAIL")
    warns = sum(1 for f in findings if f.level == "WARN")
    if fails or (args.strict and warns):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
