#!/usr/bin/env python3
"""
check-versions.py — verify pack version is consistent across the three files
that drive plugin cache invalidation:

  - .claude-plugin/marketplace.json (metadata.version + plugins[0].version)
  - VERSIONS.md (the **cti-skills:** X.Y.Z pack-version line)

The marketplace loader keys on marketplace.json. If skill bodies are bumped
in source but the plugin version is not, the cached copy under
~/.claude/plugins/cache/cti-skills/cti-skills/<version>/ never rotates and
new skill content is invisible to running Claude Code sessions.

Exit codes:
  0  all versions match
  1  mismatch (or file unreadable)
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE = REPO_ROOT / ".claude-plugin" / "marketplace.json"
VERSIONS_MD = REPO_ROOT / "VERSIONS.md"

PACK_LINE = re.compile(r"^\*\*cti-skills:\*\*\s+([0-9]+\.[0-9]+\.[0-9]+)\b")


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)


def main() -> int:
    try:
        manifest = json.loads(MARKETPLACE.read_text())
    except (OSError, json.JSONDecodeError) as e:
        fail(f"could not read {MARKETPLACE.relative_to(REPO_ROOT)}: {e}")
        return 1

    market_meta = manifest.get("metadata", {}).get("version")
    plugins = manifest.get("plugins") or []
    market_plugin = plugins[0].get("version") if plugins else None

    pack_version = None
    try:
        for line in VERSIONS_MD.read_text().splitlines():
            m = PACK_LINE.match(line)
            if m:
                pack_version = m.group(1)
                break
    except OSError as e:
        fail(f"could not read {VERSIONS_MD.relative_to(REPO_ROOT)}: {e}")
        return 1

    seen = {
        "marketplace.json metadata.version": market_meta,
        "marketplace.json plugins[0].version": market_plugin,
        "VERSIONS.md pack version": pack_version,
    }
    missing = [k for k, v in seen.items() if not v]
    if missing:
        for k in missing:
            fail(f"{k} not found")
        return 1

    if len({*seen.values()}) == 1:
        print(f"OK: all pack versions agree on {pack_version}")
        return 0

    fail("pack version mismatch — plugin cache will not rotate until aligned:")
    for k, v in seen.items():
        print(f"  {v}  {k}", file=sys.stderr)
    print(
        "\nFix: bump all three to match, then `/plugin marketplace update cti-skills`.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
