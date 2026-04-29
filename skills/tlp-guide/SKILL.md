---
name: tlp-guide
description: Use when the user asks "what TLP should this be?", applying TLP markings to a finished product, or the tradecraft pipeline calls for TLP determination before sharing. Covers TLP v2.0 (CLEAR / GREEN / AMBER / AMBER+STRICT / RED).
user-invocable: true
metadata:
  version: 1.0.0
---

# Traffic Light Protocol (TLP) v2.0

Every intelligence output from this platform MUST have a TLP designation. This is enforced by platform rules and validated by hooks.

## TLP Definitions

### TLP:RED — Named Recipients Only
**When to use**: Information that would cause significant harm if shared beyond the named recipients. Sources may face risk.

- Share with: Only the named recipients, in person or via secure channels
- Do NOT share with: Anyone not explicitly named, even within the same organisation
- Examples: Active zero-day exploitation details shared to a specific CISO; source-identifying intelligence; ongoing law enforcement operation details

### TLP:AMBER+STRICT — Organisation Only
**When to use**: Information that requires support to be effectively acted upon, limited to the recipient's organisation only.

- Share with: Members of the recipient's own organisation on a need-to-know basis
- Do NOT share with: External parties, clients, partners, or affiliated organisations
- Examples: Targeted threat intelligence specific to one organisation's infrastructure; internal investigation findings

### TLP:AMBER — Organisation + Need-to-Know
**When to use**: Information that requires support to be effectively acted upon, and may be shared with clients/partners on a need-to-know basis.

- Share with: Members of the recipient's organisation AND their clients/partners who need the information to protect themselves
- Do NOT share with: The general public, social media, or parties without a clear need-to-know
- Examples: Sector-specific threat briefings shared with ISAC members; IOCs for active campaigns affecting a supply chain

### TLP:GREEN — Community
**When to use**: Information useful for awareness within a broader community but not for public disclosure.

- Share with: The wider community (sector peers, security community) but not via publicly accessible channels
- Do NOT share with: The general public, social media, public blogs, or news outlets
- Examples: General threat landscape updates shared at closed conferences; new TTP descriptions shared within an ISAC

### TLP:CLEAR — Unrestricted
**When to use**: Information that carries minimal or no foreseeable risk of misuse. Public sharing is acceptable.

- Share with: Anyone, through any channel
- Examples: Published CVE details, public vendor advisories, general best practices, published threat reports

## Decision Tree

```
Is this information source-identifying or would sharing risk the source?
  → YES → TLP:RED

Would sharing beyond the recipient's org cause harm?
  → YES → Does it need to stay within a single org?
    → YES → TLP:AMBER+STRICT
    → NO (partners/clients may need it) → TLP:AMBER

Is this useful for community awareness but not public?
  → YES → TLP:GREEN

Is this safe for public consumption?
  → YES → TLP:CLEAR
```

## Default TLP by Product Type

| Product Type | Default TLP | Rationale |
|-------------|-------------|-----------|
| Flash report (active incident) | AMBER | Often contains org-specific context |
| Threat actor profile | GREEN | General awareness value |
| Campaign report | AMBER | May contain victim-identifying information |
| IOC list (enriched) | GREEN | Broadly useful for detection |
| Threat assessment | AMBER | Often tailored to specific stakeholder |
| Detection rules (SIGMA/YARA/KQL) | GREEN | Broadly useful for defence |
| STIX bundle | GREEN | Designed for automated sharing |
| Strategic landscape report | GREEN | General awareness |

These are defaults — always evaluate the specific content and adjust.

## Implementation

In file frontmatter:
```yaml
tlp: GREEN
```

In report headers:
```
TLP:GREEN — This information may be shared within the security community
but should not be published on publicly accessible channels.
```

## Common Mistakes

- Over-classifying (TLP:RED for everything) — reduces trust and sharing
- Under-classifying (TLP:CLEAR for IOCs with victim context) — risks harm
- Not including TLP at all — violates platform rules
- Forgetting to downgrade TLP when information becomes public
- Sharing TLP:AMBER information on public Slack channels or social media
