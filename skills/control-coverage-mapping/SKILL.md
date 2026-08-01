---
name: control-coverage-mapping
description: Use when you need to answer "which attacker techniques do our controls actually stop, and how well?", "what controls should I have for this threat?", or "what telemetry should I collect to detect it?" — joining a customer's or your own security control baseline to ATT&CK techniques using a public, versioned evidence base of 9,545 control-to-technique mappings from six sources. Produces four ranked lists (addressed strongly, addressed weakly, real gaps, and techniques no control anywhere addresses). Use for control gap analysis, security programme prioritisation, board reporting on coverage, or the Resistance Strength side of a FAIR risk assessment. Invoke after /threat-actor-profiling or /lookup-liberty91 has produced a technique list.
user-invocable: true
metadata:
  version: 1.0.0
  tags: [analysis, controls, mitre-attack, gap-analysis, fair, risk]
---

# Control Coverage Mapping

Answers one question with evidence instead of opinion: **which attacker techniques does this control set actually address, and at what strength?**

The usual way to answer it is to put people in a room and negotiate a percentage. This skill replaces that with a join against a public, versioned table that both sides can read and challenge. Where the evidence rates a control's strength, that rating is carried through unchanged. Where it does not, the output says so rather than inventing a number.

## When to invoke

- The user asks what their controls cover, where the gaps are, or how to prioritise security spend
- The user asks **what controls they should have** for a given threat, campaign or sector, with no baseline in hand
- A threat profile has produced a technique list and the next question is "so are we covered?"
- A FAIR or risk-quantification workflow needs the **Resistance Strength** input
- Board or audit reporting needs a defensible coverage statement with citations
- A vendor claims a product "stops" a technique and you want the public evidence
- A detection team asks **what telemetry to collect** for a given threat (`--telemetry`)

**Do NOT invoke for:** deciding whether a control is correctly *configured* in a specific environment (that is a testing question, not a mapping question), or for producing a single vulnerability percentage (see Limits).

## Four modes

Be clear which question you are answering, because the inputs and the honest wording differ.

| Question | Mode | Needs a baseline? |
|---|---|---|
| "What does my **current** control set cover?" | `--controls baseline.csv` | yes |
| "What controls **should** I have for this threat?" | omit `--controls` | no |
| "What do I actually **implement**?" | `--mitigations` | no |
| "What do I **collect and correlate**?" | `--telemetry` | no |

```bash
# COVERAGE — gap assessment against what they actually run
python3 tools/clis/map_controls.py --controls baseline.csv --techniques techs.json

# RECOMMEND — no baseline needed
python3 tools/clis/map_controls.py --techniques T1566,T1190,T1078 --top 15

# ACTIONABLE — ATT&CK mitigations and telemetry, combinable
python3 tools/clis/map_controls.py --techniques techs.json --mitigations --telemetry
```

Stdlib only, no install, no API key. Bundled data lives in `data/attack-control-mapping/`.

### When "SI-04 System Monitoring" is not a useful answer

It usually is not, and this is a limit of the evidence base rather than of the question. **The NIST half of the workbook carries a control id and a control name and nothing else**: no control text, no enhancements, no protect/detect/respond split. `SI-04` maps to 52 techniques in a real run, so as advice it means "monitor things". There is no field to expand it from, and paraphrasing NIST from memory into a customer deliverable is not sourcing, it is bluffing.

Two modes exist to answer the question properly, both carrying **MITRE's own text unchanged**:

**`--mitigations`** returns ATT&CK M-codes ranked by coverage of the supplied techniques, each with its published definition. On a real 79-technique set: `M1047 Audit` (19 techniques), `M1026 Privileged Account Management` (17), `M1018 User Account Management` (21), `M1017 User Training` (13). Narrower than a NIST family and each one arrives with a definition the reader can act on.

**`--telemetry`** resolves "monitoring" into named log sources and concrete detection logic, ranked by how much of the supplied technique set each covers, down to channel level: `WinEventLog:Sysmon EventCode=1`, `auditd:SYSCALL execve`, `WinEventLog:Security 4688`. Per technique it returns MITRE's detection strategy, e.g. for `T1562 Impair Defenses`: "unusual service stop events, termination of AV/EDR processes, registry modifications disabling security tools ... correlate process creation with service stop requests and registry edits."

**Prefer these two whenever the output has to be acted on.** Keep the NIST list for customers who must report in that language, and say plainly that the family label is doing a lot of work.

Both read pre-extracted files in `data/attack-control-mapping/`, not the full ATT&CK bundle, because `mitre-attack/*.json` is gitignored and absent on a fresh clone. Regenerate after an ATT&CK refresh with `python3 data/attack-control-mapping/build_attack_extract.py`.

### Do not brief the basic hygiene: the distinctive/baseline split

An analyst does not put "user awareness training" in a threat briefing. It applies to everyone, everywhere, always, so it says nothing about the threat just analysed. But a naive ranking surfaces exactly those controls **every time**, because breadth is what it ranks on: `M1018 User Account Management` maps to 20% of every technique MITRE publishes, and `SI-04 System Monitoring` to most of the NIST-mapped universe. They top any list for any input.

The tool separates them by **lift**: the share of *your* techniques a control covers, divided by the share of *all* ATT&CK techniques it covers.

- **lift ≈ 1.0** — covers your set at the same rate it covers everything → **baseline hygiene**
- **lift ≥ 1.5** — over-represented in your set → **distinctive to this threat**

Both `--mitigations` and recommend mode return `*_distinctive`, `*_baseline` and `*_low_support`. On a real run against 79 techniques trending in US financial services:

| | Distinctive | Baseline |
|---|---|---|
| ATT&CK | `M1016` Vulnerability Scanning **5.2x**, `M1050` Exploit Protection 3.6x, `M1033` Limit Software Installation 2.6x, `M1013` Application Developer Guidance 2.6x | `M1026` PAM 1.3x, `M1038` Execution Prevention 1.0x |
| NIST | `SC-29` Heterogeneity 7.3x, `SC-30` Concealment and Misdirection 6.5x, `RA-10` Threat Hunting 4.2x | `SI-04` System Monitoring **1.3x**, `CM-06` Configuration Settings 1.2x |

That set was dominated by supply-chain compromise and public-facing exploitation, and the distinctive list names exactly that: application developer guidance, limit software installation, vulnerability scanning, exploit protection. Breadth ranking buried all four under "audit" and "user training".

**Three things to say when you present it.** Distinctive does **not** mean more important: baseline controls are usually the ones a customer must have first, they are simply not *news* and not evidence about this threat. Lift on a small denominator is noisy, which is why `--min-support` (default 3) holds thin controls back into `low_support` rather than letting a 1-of-2 control claim 20x. And a technique set of only a handful will put everything in `low_support`, which is correct rather than broken; the summary says so explicitly, and `--min-support 1` overrides it if you accept the noise.

Tune with `--lift-threshold` (default 1.5): 1.2 is permissive, 3.0 gives only the sharpest signals.

### Recommend mode returns two lists, and you must keep them apart

**Only the four CTID cloud stacks carry effectiveness scores.** Rank everything on strength and you get nothing but Microsoft, Google and AWS products, which is useless to a customer not on those stacks and reads as a product pitch. So the output splits:

- **`recommended_scored_capabilities`** — the four cloud stacks, ranked by how many of the supplied techniques each addresses at `significant` strength.
- **`recommended_control_classes`** — NIST 800-53 and ATT&CK mitigations, ranked by **breadth of relevance only**, because no source rates their strength.

**The second list is not "weaker controls". It is "controls nobody has scored."** Say that when presenting it. In practice it is the more useful list for most customers: a real run against 79 trending techniques put `SI-04 System Monitoring` at 52 techniques touched and `AC-06 Least Privilege` at 40, which is a far more actionable answer than a licence recommendation.

### The control baseline

A CSV. Three required columns:

| Column | Meaning |
|---|---|
| `control_ref` | your identifier, e.g. `IAM-05` |
| `framework` | must match the evidence base exactly: `NIST SP 800-53 rev5`, `Microsoft 365 security`, `Microsoft Azure security`, `AWS security services`, `Google Cloud security`, `ATT&CK Mitigations` |
| `mapping_key` | the control id in that framework, e.g. `AC-06`, `EID-MFA-E3` |

Optional: `control_name`, `implementation_status`, `owner`, `mapping_note`.
See `data/attack-control-mapping/example_control_baseline.csv` for a worked 45-control example.

**Leave `mapping_key` empty when a control genuinely does not map.** That is a finding to report, not a gap to paper over with the nearest-looking identifier. Forcing a match is the fastest way to make this analysis dishonest, and the output has a dedicated section for controls that do not map.

The two vocabularies the evidence base understands natively are **NIST SP 800-53 rev5** and **named cloud security capabilities**. Getting a customer to express their baseline in one of them is most of the work of this skill.

## The four output buckets

Three are the familiar coverage lists. The fourth is the one that gets misreported.

| Bucket | Meaning | Actionable |
|---|---|---|
| `significant` | at least one of their controls is scored `significant` against the technique | yes, this is strength |
| `weak` | reached only at `partial`, `minimal`, or coverage-only | yes, this is where to invest |
| `gap` | controls exist in the evidence base; **theirs reach none of them** | yes, this is the real gap list |
| `no_control_exists` | no source maps any control, **or** the only mapping is `M1056 Pre-compromise` | **no** |

**Never merge the fourth into the third.** It inflates the gap list with things no control programme could close, which overstates the finding and costs you credibility the moment a competent CISO reads it. `M1056 Pre-compromise` is ATT&CK's explicit marker for "cannot be mitigated before compromise"; reconnaissance and resource-development techniques behave this way by nature, because the adversary performs them on their own infrastructure.

## How to report the result

- **Cite the source and score on every mapped row.** The evidence base carries both; a coverage claim without them is an assertion.
- **Never present a vendor score as a control-class score.** A `significant` rating for an Azure capability describes *that product*, not "network security" generally. If you generalise, say that you did.
- **`coverage-only` is not partial protection.** It means a recognised body asserts the control is relevant and makes **no claim about strength**. Only the four CTID cloud stacks carry effectiveness scores at all; ATT&CK's own mitigations and the entire NIST 800-53 mapping are relevance assertions.
- **Absence of a mapping is absence of evidence**, not evidence of ineffectiveness.
- Apply `/apply-tlp` and `/confidence-language` before the output leaves the building.

## Known traps

These are empirical, found by running this against real data. Each one silently corrupts the output if unhandled.

- **Revoked ATT&CK IDs.** Some feeds still emit `T1081`, `T1192`, `T1188`, `T1488`, `T1022`. They join to nothing, so a stale identifier reads as a security gap, and they fragment counts. The CLI remaps them to MITRE's successors and reports what moved.
- **Whole 800-53 families are missing.** CTID's mapping has **no PL, AT or IR family**. Policy, awareness training and incident response controls therefore score zero here regardless of how good they are. Say so explicitly; do not let it read as a gap.
- **No EDR in the Microsoft 365 sheet.** It scores Defender for Office, Identity, Cloud Apps and Entra ID. Defender for Endpoint and ASR rules are absent, so a well-run EDR deployment cannot be credited from that source.
- **The two workbook sheets disagree.** `Master_Mapping` holds rows for 18 technique IDs absent from `Technique_Summary`, including the entire `T1562` Impair Defenses family. Build the technique universe from `Master_Mapping`; the CLI does. Using the summary sheet misclassifies `T1562` as unmapped when 40 mapped rows exist for it.
- **Parent vs sub-technique granularity.** Many threat feeds report `T1566 Phishing` rather than `T1566.001`. The join works at both levels, but coverage assessed at parent granularity is blunter than the data supports. State it. Do not roll sub-techniques up to force matches.

## Limits, state these in any output

1. **It cannot produce a vulnerability percentage.** It tells you which behaviour your controls address and how strongly the public evidence rates that. Converting to a probability needs calibration with the customer.
2. **Scores are point-in-time expert judgement**, not test results. Breach-and-attack-simulation or purple-team results for the specific environment supersede them.
3. **Version skew.** CTID pins to ATT&CK 16.1 while native mitigation data is v19.1, so techniques introduced after 16.1 appear only via native mitigations or not at all. This accounts for most of the 32-technique gap list.
4. **It says nothing about configuration.** A mapped, strongly-scored control that is deployed in audit mode protects nothing.
5. **No adversary adaptation.** A `significant` rating says nothing about an attacker pivoting to an unscored sibling sub-technique.

## Where this sits in FAIR

This supports **Resistance Strength**, one half of **Vulnerability**, under **Loss Event Frequency**.

```
Risk
├── Loss Event Frequency
│   ├── Threat Event Frequency        (not from this data)
│   └── Vulnerability
│       ├── Threat Capability          <- /lookup-liberty91, /threat-actor-profiling
│       └── Resistance Strength        <- THIS SKILL + the customer's baseline
└── Loss Magnitude                     (not from this data)
```

The pairing matters: a technique list without controls tells you what is coming, a control list without techniques tells you what you bought. Joined, they tell you what to do next.

## The evidence base

`data/attack-control-mapping/` — 9,545 normalized rows across 697 techniques, from six public, versioned sources: MITRE ATT&CK Enterprise v19.1 native mitigations, and CTID Mappings Explorer for NIST SP 800-53 rev5, AWS, Azure, GCP and Microsoft 365. Shipped as JSON so nothing needs Excel; the source workbook is included for provenance.

Verify it reproduces its own published figures before trusting it:

```bash
python3 -c "
import json, collections
rows   = json.load(open('data/attack-control-mapping/master_mapping.json'))
active = [t['technique_id'] for t in json.load(open('data/attack-control-mapping/active_techniques.json'))]
by = collections.defaultdict(list)
for r in rows: by[r['technique_id']].append(r)
f = collections.Counter()
for t in active:
    rs = by.get(t, [])
    if   not rs:                                                        f['none'] += 1
    elif any(x['effectiveness']=='significant' for x in rs):            f['significant'] += 1
    elif any(x['effectiveness'] in ('partial','minimal') for x in rs):  f['partial/minimal'] += 1
    else:                                                               f['coverage-only'] += 1
print(len(rows), 'rows |', dict(f))"
```

Expected: `9545 rows | {'significant': 220, 'partial/minimal': 283, 'coverage-only': 162, 'none': 32}`, matching `data/attack-control-mapping/METHODOLOGY.md` section 5. **No score is ever synthesized** — that rule must survive any refresh.

## Related skills

- `/lookup-liberty91` — supplies the technique list, with per-occurrence notes on how each was used
- `/threat-actor-profiling`, `/campaign-tracking` — technique sets for a named actor or campaign
- `/mitre-attack` — the local ATT&CK dataset, for resolving technique names and revocations
- `/threat-assessment`, `/writing-assessments` — turn coverage into a finished product
- `/detection-engineer`, `/sigma-writing`, `/kql-writing` — the natural follow-on: write detections for the gap list
- `/apply-tlp`, `/confidence-language` — rigor pipeline before dissemination
