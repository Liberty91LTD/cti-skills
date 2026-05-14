#!/usr/bin/env python3
"""
PostToolUse hook for cti-skills.

Fires when Write/Edit/MultiEdit touches `skills/lookup-*/SKILL.md`.
Injects a system reminder listing the sibling skills + orchestrator catalog
that should be updated in the same change set, so a new lookup never ships
without being wired into the investigation skills and orchestrator.

Backed by feedback memory: feedback_lookup_skill_propagation.md
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
LOOKUP_PATTERN = re.compile(r"/skills/(lookup-[A-Za-z0-9_-]+)/SKILL\.md$")

PROPAGATION_TARGETS = [
    ("skills/cti-orchestrator/SKILL.md",       "Lookup catalog table (always)"),
    ("skills/ip-investigation/SKILL.md",       "if it supports IPs"),
    ("skills/domain-investigation/SKILL.md",   "if it supports domains"),
    ("skills/url-investigation/SKILL.md",      "if it supports URLs"),
    ("skills/hash-investigation/SKILL.md",     "if it supports hashes"),
    ("skills/ioc-enrichment-workflow/SKILL.md","routing tables for any covered indicator type"),
    ("skills/malware-analysis/SKILL.md",       "if it provides sample/sandbox/MITRE data"),
]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    if payload.get("tool_name") not in {"Write", "Edit", "MultiEdit"}:
        return 0

    file_path = (payload.get("tool_input") or {}).get("file_path", "")
    match = LOOKUP_PATTERN.search(file_path)
    if not match:
        return 0

    lookup_name = match.group(1)

    missing = []
    try:
        for rel_path, _ in PROPAGATION_TARGETS:
            target = REPO_ROOT / rel_path
            if not target.exists():
                continue
            text = target.read_text(encoding="utf-8", errors="ignore")
            if f"/{lookup_name}" not in text:
                missing.append(rel_path)
    except Exception:
        missing = [rel for rel, _ in PROPAGATION_TARGETS]

    bullet_lines = "\n".join(
        f"  - {rel} ({why})" for rel, why in PROPAGATION_TARGETS
    )

    if missing:
        missing_lines = "\n".join(f"  - {m}" for m in missing)
        body = (
            f"You just modified `{lookup_name}/SKILL.md`. The user requires that every "
            f"new or updated lookup-* skill is propagated into the orchestrator catalog "
            f"and the relevant investigation skills in the same change set "
            f"(see feedback_lookup_skill_propagation memory).\n\n"
            f"`/{lookup_name}` is NOT yet referenced in:\n{missing_lines}\n\n"
            f"Update each that applies before considering this change complete. "
            f"Full propagation target list:\n{bullet_lines}\n\n"
            f"After committing, remind the user to refresh the installed plugin cache "
            f"(`/plugin update cti-skills` or equivalent) — slash-command invocations "
            f"load from `~/.claude/plugins/cache/...`, not the local repo."
        )
    else:
        body = (
            f"You just modified `{lookup_name}/SKILL.md`. `/{lookup_name}` is already "
            f"referenced in every propagation target — good. If this change altered the "
            f"lookup's capabilities (new indicator type, new subcommand), re-check the "
            f"siblings anyway:\n{bullet_lines}"
        )

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": body,
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
