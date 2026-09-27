---
name: stix-bundle
description: STIX 2.1 bundle creation reference. Object types, relationships, and JSON templates for structured threat intelligence sharing. Includes the per-claim mapping of Admiralty grades from /quality-of-information-check to STIX confidence, and the reverse mapping on import.
user-invocable: false
metadata:
  version: 2.0.0
---

# STIX 2.1 Bundle Creation

STIX (Structured Threat Information Expression) 2.1 is the standard for representing and sharing cyber threat intelligence.

## Bundle Structure

```json
{
  "type": "bundle",
  "id": "bundle--<UUID>",
  "objects": [
    // Array of STIX Domain Objects (SDOs) and Relationship Objects (SROs)
  ]
}
```

## STIX Domain Objects (SDOs)

### Indicator
Represents a pattern that can be used to detect suspicious activity.

```json
{
  "type": "indicator",
  "spec_version": "2.1",
  "id": "indicator--<UUID>",
  "created": "2026-01-15T00:00:00.000Z",
  "modified": "2026-01-15T00:00:00.000Z",
  "name": "Malicious IP used by APT28",
  "description": "C2 server observed in campaign targeting European government entities",
  "pattern": "[ipv4-addr:value = '203.0.113.42']",
  "pattern_type": "stix",
  "valid_from": "2026-01-15T00:00:00.000Z",
  "valid_until": "2026-04-15T00:00:00.000Z",
  "kill_chain_phases": [
    {
      "kill_chain_name": "mitre-attack",
      "phase_name": "command-and-control"
    }
  ],
  "confidence": 70,
  "labels": ["malicious-activity"],
  "object_marking_refs": ["marking-definition--613f2e26-407d-48c7-9eca-b8e91df99dc9"]
}
```

### STIX Pattern Syntax

| IOC Type | STIX Pattern |
|----------|-------------|
| IPv4 | `[ipv4-addr:value = '1.2.3.4']` |
| IPv6 | `[ipv6-addr:value = '2001:db8::1']` |
| Domain | `[domain-name:value = 'evil.com']` |
| URL | `[url:value = 'https://evil.com/payload']` |
| SHA-256 | `[file:hashes.'SHA-256' = 'abc123...']` |
| MD5 | `[file:hashes.MD5 = 'abc123...']` |
| Email | `[email-addr:value = 'phish@evil.com']` |
| File name | `[file:name = 'malware.exe']` |
| Combined | `[file:hashes.'SHA-256' = 'abc...' AND file:name = 'payload.dll']` |

### Threat Actor

```json
{
  "type": "threat-actor",
  "spec_version": "2.1",
  "id": "threat-actor--<UUID>",
  "created": "2026-01-15T00:00:00.000Z",
  "modified": "2026-01-15T00:00:00.000Z",
  "name": "APT28",
  "description": "Russian state-sponsored threat actor also known as Fancy Bear, Sofacy",
  "aliases": ["Fancy Bear", "Sofacy", "Pawn Storm", "Forest Blizzard"],
  "threat_actor_types": ["nation-state"],
  "roles": ["agent"],
  "sophistication": "expert",
  "resource_level": "government",
  "primary_motivation": "political",
  "goals": ["espionage", "disruption"]
}
```

### Malware

```json
{
  "type": "malware",
  "spec_version": "2.1",
  "id": "malware--<UUID>",
  "created": "2026-01-15T00:00:00.000Z",
  "modified": "2026-01-15T00:00:00.000Z",
  "name": "SUNBURST",
  "description": "Backdoor trojanised into SolarWinds Orion software",
  "malware_types": ["backdoor", "trojan"],
  "is_family": true,
  "kill_chain_phases": [
    {"kill_chain_name": "mitre-attack", "phase_name": "initial-access"},
    {"kill_chain_name": "mitre-attack", "phase_name": "command-and-control"}
  ]
}
```

### Attack Pattern (MITRE ATT&CK Technique)

```json
{
  "type": "attack-pattern",
  "spec_version": "2.1",
  "id": "attack-pattern--<UUID>",
  "created": "2026-01-15T00:00:00.000Z",
  "modified": "2026-01-15T00:00:00.000Z",
  "name": "Phishing: Spearphishing Attachment",
  "description": "Adversaries send spearphishing emails with malicious attachments",
  "external_references": [
    {
      "source_name": "mitre-attack",
      "external_id": "T1566.001",
      "url": "https://attack.mitre.org/techniques/T1566/001"
    }
  ],
  "kill_chain_phases": [
    {"kill_chain_name": "mitre-attack", "phase_name": "initial-access"}
  ]
}
```

### Campaign

```json
{
  "type": "campaign",
  "spec_version": "2.1",
  "id": "campaign--<UUID>",
  "created": "2026-01-15T00:00:00.000Z",
  "modified": "2026-01-15T00:00:00.000Z",
  "name": "Operation Fancy Storm",
  "description": "Targeted espionage campaign against European government entities",
  "first_seen": "2025-11-01T00:00:00.000Z",
  "last_seen": "2026-01-15T00:00:00.000Z"
}
```

### Identity (Victim/Target)

```json
{
  "type": "identity",
  "spec_version": "2.1",
  "id": "identity--<UUID>",
  "created": "2026-01-15T00:00:00.000Z",
  "modified": "2026-01-15T00:00:00.000Z",
  "name": "European Government Sector",
  "identity_class": "class",
  "sectors": ["government-national"]
}
```

## Relationship Objects (SROs)

```json
{
  "type": "relationship",
  "spec_version": "2.1",
  "id": "relationship--<UUID>",
  "created": "2026-01-15T00:00:00.000Z",
  "modified": "2026-01-15T00:00:00.000Z",
  "relationship_type": "uses",
  "source_ref": "threat-actor--<UUID>",
  "target_ref": "malware--<UUID>",
  "confidence": 70
}
```

`confidence` on an SRO grades the relationship itself, the claim that the source uses, targets or is attributed to the target. See [Confidence and source grading](#confidence-and-source-grading) for how the value is derived.

### Common Relationship Types

| Source | Relationship | Target |
|--------|-------------|--------|
| threat-actor | uses | malware, attack-pattern, tool |
| threat-actor | targets | identity, vulnerability |
| threat-actor | attributed-to | identity (sponsoring nation) |
| campaign | uses | malware, attack-pattern, tool |
| campaign | targets | identity, vulnerability |
| campaign | attributed-to | threat-actor |
| indicator | indicates | malware, threat-actor, campaign |
| malware | targets | identity, vulnerability |
| malware | uses | attack-pattern |

## Confidence and source grading

Grades are exported **per claim, never per event**. Each evidence item from `/quality-of-information-check` (schema: `skills/quality-of-information-check/references/evidence-item-schema.md`) carries its own `source_reliability` and `information_credibility`, and each lands on the one STIX object that expresses that claim. Do not stamp one value across every object in a bundle, and do not put `confidence` on the bundle itself. A bundle is a container and has no such property.

### Information credibility to `confidence`

STIX 2.1 Appendix A (Confidence Scales), Admiralty Credibility table. Section 3.2 of the spec makes the Appendix A mappings normative, so use these values and no others.

| Information credibility | `confidence` on export | Range read on import |
|---|---|---|
| 1 Confirmed by other sources | 90 | 80 to 100 |
| 2 Probably true | 70 | 60 to 79 |
| 3 Possibly true | 50 | 40 to 59 |
| 4 Doubtful | 30 | 20 to 39 |
| 5 Improbable | 10 | 0 to 19 |
| 6 Truth cannot be judged | omit the property | property absent |

Credibility 6 means the property is left out. It is never written as 0, which would read as credibility 5.

### Which object carries it

| Claim | Object that carries `confidence` |
|---|---|
| Any observable on its own (`domain-name`, `ipv4-addr`, `file`, `url`, `email-addr`) | None. SCOs never carry `confidence`. An observable is a fact about the world, not a claim. |
| "This observable is malicious" or "this pattern detects X" | The Indicator. One Indicator per distinct assertion, so the same IP asserted as C2 by one primary and as a scanner by another is two Indicators with separate grades. |
| Relational claims: `indicates`, `based-on`, `uses`, `attributed-to`, `targets`, `exploits` | The Relationship. For "X was seen at Y", the Sighting. |
| Other SDOs (`threat-actor`, `intrusion-set`, `malware`, `campaign`) | Only when the claim is the entity's own existence as a distinct thing, for example a vendor asserting a new cluster. Otherwise leave it off and grade the relationships. |

An attribution is a Relationship (`attributed-to`), so its grade goes there and not on the Threat Actor. A well-known actor object with `confidence: 50` wrongly says the actor's existence is in doubt.

### Source reliability and the primary source

STIX has no reliability property. On the same object that carries `confidence`:

- `x_liberty91_source_reliability`: the letter `A` to `F`, graded on the primary source.
- An `external_references` entry for the primary source (`source_name`, `url`, and `description` with the report title and date). Cite the primary, not the outlet that relayed it.
- When the grade was read from a confidence value rather than assessed, `x_liberty91_derived_from_confidence: true`.

Reliability is still written when credibility is 6 and `confidence` is omitted, for example `F` on an uncorroborated actor claim.

**OpenCTI.** Reliability belongs to the source, so set it on the primary source's Organization entity, which has a native A to F reliability field, and link the object to that Organization as its author (`created_by_ref`). The custom property still travels in the bundle for other consumers.

### Worked example

Two claims from one vendor report: an observation graded A2 and an attribution graded B3.

```json
[
  {
    "type": "indicator",
    "spec_version": "2.1",
    "id": "indicator--<UUID>",
    "created": "2026-09-27T00:00:00.000Z",
    "modified": "2026-09-27T00:00:00.000Z",
    "name": "C2 domain observed in incident response",
    "pattern": "[domain-name:value = 'update-check.example.net']",
    "pattern_type": "stix",
    "valid_from": "2026-09-20T00:00:00.000Z",
    "confidence": 70,
    "x_liberty91_source_reliability": "A",
    "external_references": [
      {
        "source_name": "Example Vendor",
        "description": "Primary source. Intrusion report, 2026-09-22",
        "url": "https://vendor.example.com/blog/intrusion-report"
      }
    ]
  },
  {
    "type": "relationship",
    "spec_version": "2.1",
    "id": "relationship--<UUID>",
    "created": "2026-09-27T00:00:00.000Z",
    "modified": "2026-09-27T00:00:00.000Z",
    "relationship_type": "attributed-to",
    "source_ref": "campaign--<UUID>",
    "target_ref": "threat-actor--<UUID>",
    "confidence": 50,
    "x_liberty91_source_reliability": "B",
    "external_references": [
      {
        "source_name": "Example Vendor",
        "description": "Primary source. Intrusion report, 2026-09-22",
        "url": "https://vendor.example.com/blog/intrusion-report"
      }
    ]
  }
]
```

The `domain-name` SCO and the `threat-actor` SDO, if included, carry neither `confidence` nor the reliability property.

### Report objects

A Report groups many claims, so it has no grade of its own. Where a consumer needs a value, write the **weakest link**: the `confidence` of the lowest-graded load-bearing claim (`event_qoi_summary.weakest_link`), with `x_liberty91_confidence_basis: "weakest_link"`. Never an average. If the weakest link is credibility 6, omit `confidence` and keep the basis property. This value exists for interoperability only. Analysis consumes the per-claim grades.

### Import direction

Reading a bundle from elsewhere, map `confidence` back with the ranges in the table above, absent property = 6. Set the `derived_from_confidence` flag on every imported item. The number tells you what the producer thought, not how they knew, so `/quality-of-information-check` re-grades the item when a primary is available (rubric rule R11). Read reliability from `x_liberty91_source_reliability` when present. Otherwise it is `F`, cannot be judged. Do not infer it from the producer's name.

MISP tagging for the same grades is in `/ioc-export`.

## TLP Marking Definitions (Standard UUIDs)

These are the canonical marking-definition object IDs. Reference them from `object_marking_refs`; **do not include the marking-definition object itself in the bundle** (see below).

```json
"marking-definition--613f2e26-407d-48c7-9eca-b8e91df99dc9"  // TLP:CLEAR
"marking-definition--34098fce-860f-48ae-8e50-ebd3cc5e41da"  // TLP:GREEN
"marking-definition--f88d31f6-486f-44da-b317-01333bde0b82"  // TLP:AMBER
"marking-definition--826578e1-40a3-4b46-a8d7-b76e4fd71d29"  // TLP:AMBER+STRICT
"marking-definition--e828b379-4e03-4974-9ac4-e53a884c97c1"  // TLP:RED
```

### MISP-compatible bundles — reference TLPs, don't inline them

For bundles that will be imported into MISP via `/lookup-misp` `upload-stix`, **only reference TLP marking-definition UUIDs** in `object_marking_refs`. Don't include a `{"type": "marking-definition", ...}` object in the bundle's `objects` array.

The inline shape that older STIX 2.0 examples show — `definition_type: "tlp"` with `definition: {"tlp": "clear"}` — fails MISP's STIX 2 importer with `"Does not match any TLP Marking definition!"`. MISP resolves the canonical UUIDs from its own catalog; supplying an inline copy triggers the spec-conformance check and the whole bundle is rejected.

✅ **Correct (MISP-compatible)** — reference only, marking resolved by consumer:
```json
{
  "type": "bundle",
  "id": "bundle--...",
  "objects": [
    {
      "type": "indicator",
      "id": "indicator--...",
      "object_marking_refs": ["marking-definition--613f2e26-407d-48c7-9eca-b8e91df99dc9"],
      "pattern": "[ipv4-addr:value = '203.0.113.42']",
      "pattern_type": "stix",
      "valid_from": "2026-04-26T00:00:00.000Z"
    }
  ]
}
```

❌ **Don't do this** for MISP-bound bundles — inlined TLP definition trips the importer:
```json
{
  "type": "marking-definition",
  "id": "marking-definition--613f2e26-407d-48c7-9eca-b8e91df99dc9",
  "definition_type": "tlp",
  "definition": {"tlp": "clear"}
}
```

If you need a self-contained bundle for non-MISP consumers (offline ingest, archives, partners without a TLP catalog), the inline form is valid STIX 2.1 — keep a separate non-MISP variant rather than tweaking the MISP one.

If you need TLP applied inside MISP after import, do it via a `tag-event` call rather than a STIX marking — see `tools/integrations/misp.md`.

**OpenCTI is not affected** — it is STIX 2.1-native and imports bundles as-is via `/lookup-opencti` `upload-stix`, inline TLP marking-definitions included. Only MISP-bound bundles need the reference-only treatment above.

## Output Location

Write STIX bundles to: `data/stix-bundles/YYYY-MM-DD-<context>.json`
