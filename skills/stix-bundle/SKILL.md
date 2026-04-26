---
name: stix-bundle
description: STIX 2.1 bundle creation reference. Object types, relationships, and JSON templates for structured threat intelligence sharing.
user-invocable: false
metadata:
  version: 1.0.0
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
  "confidence": 85,
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
  "confidence": 85
}
```

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

## Output Location

Write STIX bundles to: `data/stix-bundles/YYYY-MM-DD-<context>.json`
