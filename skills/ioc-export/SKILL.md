---
name: ioc-export
description: IOC export formats and procedures. CSV, STIX 2.1, OpenIOC, MISP. Handles format conversion and packaging, and carries per-claim Admiralty grades from /quality-of-information-check into each format (STIX confidence, MISP attribute tags).
user-invocable: false
metadata:
  version: 2.0.0
---

# IOC Export Guide

## Supported Export Formats

### CSV
Standard tabular format. Most broadly compatible.

```csv
indicator,type,first_seen,last_seen,confidence,source_reliability,information_credibility,tlp,source,source_url,context,mitre_attack,tags
203.0.113.42,ipv4-addr,2026-01-15,2026-03-20,70,A,2,GREEN,"Mandiant report MAL-2026-001",https://vendor.example.com/mal-2026-001,C2 server for SUNBURST variant,T1071.001,"apt29;sunburst"
evil.example.com,domain-name,2026-02-01,2026-03-20,50,B,3,GREEN,"Internal analysis",,"Phishing landing page",T1566.002,"phishing;apt29"
```

**Column definitions:**
| Column | Required | Description |
|--------|----------|-------------|
| indicator | Yes | The IOC value |
| type | Yes | STIX indicator type: ipv4-addr, ipv6-addr, domain-name, url, file:hashes.SHA-256, file:hashes.MD5, email-addr |
| first_seen | Yes | ISO date first observed |
| last_seen | No | ISO date last observed |
| confidence | Yes | 0-100. When the row comes from a graded claim, derived from information credibility (see Grades on export). Empty for credibility 6 |
| source_reliability | No | Admiralty A-F, graded on the primary source |
| information_credibility | No | Admiralty 1-6, graded on the claim |
| tlp | Yes | TLP marking |
| source | Yes | Source description. The primary source, not the outlet that relayed it |
| source_url | No | URL of the primary source |
| context | No | What the IOC represents (C2, phishing, etc.) |
| mitre_attack | No | ATT&CK technique IDs |
| tags | No | Semicolon-separated tags |

A row is one claim about one indicator. If two primaries make different assertions about the same value, that is two rows, each with its own grade.

### STIX 2.1 Bundle
See `stix-bundle` skill for full specification, including which object carries `confidence` (never the SCO), the `x_liberty91_source_reliability` property and a worked example.

### OpenIOC (XML)
Mandiant's legacy IOC format. Still used by some tools.

```xml
<?xml version="1.0" encoding="utf-8"?>
<ioc xmlns="http://schemas.mandiant.com/2010/ioc" id="[UUID]" last-modified="YYYY-MM-DDT00:00:00">
  <short_description>IOC Title</short_description>
  <description>Description</description>
  <authored_by>CTI Platform</authored_by>
  <authored_date>YYYY-MM-DDT00:00:00</authored_date>
  <definition>
    <Indicator operator="OR" id="[UUID]">
      <IndicatorItem id="[UUID]" condition="is">
        <Context document="Network" search="Network/DNS" type="mir"/>
        <Content type="string">evil.example.com</Content>
      </IndicatorItem>
      <IndicatorItem id="[UUID]" condition="is">
        <Context document="FileItem" search="FileItem/Md5sum" type="mir"/>
        <Content type="md5">abc123...</Content>
      </IndicatorItem>
    </Indicator>
  </definition>
</ioc>
```

### MISP Format (JSON)
For import into MISP instances.

```json
{
  "Event": {
    "info": "IOC collection: [context]",
    "threat_level_id": "2",
    "analysis": "2",
    "distribution": "1",
    "Tag": [
      {"name": "tlp:green"},
      {"name": "misp-galaxy:mitre-attack-pattern=\"Phishing - T1566\""}
    ],
    "Attribute": [
      {
        "type": "ip-dst",
        "category": "Network activity",
        "value": "203.0.113.42",
        "to_ids": true,
        "comment": "C2 server",
        "Tag": [
          {"name": "admiralty-scale:source-reliability=\"a\""},
          {"name": "admiralty-scale:information-credibility=\"2\""},
          {"name": "misp:confidence-level=\"usually-confident\""}
        ]
      },
      {
        "type": "domain",
        "category": "Network activity",
        "value": "evil.example.com",
        "to_ids": true,
        "comment": "Phishing landing page",
        "Tag": [
          {"name": "admiralty-scale:source-reliability=\"b\""},
          {"name": "admiralty-scale:information-credibility=\"3\""},
          {"name": "misp:confidence-level=\"fairly-confident\""}
        ]
      }
    ]
  }
}
```

## Grades on export

Applies when the IOCs come with evidence items from `/quality-of-information-check`. Grades are exported **per claim, never per event**: each indicator carries the grade of the claim it came from.

| Information credibility | STIX `confidence` | MISP confidence tag | `confidence` range read on import |
|---|---|---|---|
| 1 | 90 | `misp:confidence-level="completely-confident"` | 80 to 100 |
| 2 | 70 | `misp:confidence-level="usually-confident"` | 60 to 79 |
| 3 | 50 | `misp:confidence-level="fairly-confident"` | 40 to 59 |
| 4 | 30 | `misp:confidence-level="rarely-confident"` | 20 to 39 |
| 5 | 10 | `misp:confidence-level="unconfident"` | 0 to 19 |
| 6 | property omitted | `misp:confidence-level="confidence-cannot-be-evaluated"` | absent |

The STIX column is the Admiralty Credibility table in STIX 2.1 Appendix A, which the spec makes normative. The MISP confidence tag is derived from credibility. It is not a separate judgement.

**MISP tags, at attribute level.** Each attribute gets three tags:

- `admiralty-scale:source-reliability="a"` through `"f"` (lowercase letter)
- `admiralty-scale:information-credibility="1"` through `"6"`
- the `misp:confidence-level` tag from the table

Tag strings verified on 2026-09-27 against `admiralty-scale/machinetag.json` (version 5) and `misp/machinetag.json` (version 14) in github.com/MISP/misp-taxonomies. The taxonomy also defines `source-reliability="g"` (deliberately deceptive). The grading rubric stops at F, so this pack never writes `g`. On import treat `g` as `E` and set the `deception_indicators_present` flag.

**Event-level tags.** Optional. If set, they are the weakest link, the grade of the lowest-graded load-bearing claim, never an average. They are there for consumers that filter on event tags. The attribute tags are the record.

**Pushing to MISP.** The target instance needs the `admiralty-scale` and `misp` taxonomies enabled. `/lookup-misp` `add-attribute --tags` applies them per attribute. Quote the whole list for the shell, since the tag names contain double quotes and commas separate tags. Do not rely on `upload-stix` to turn STIX `confidence` into these tags. That conversion is not verified here, so tag the attributes explicitly.

**Import.** Reading graded data in, prefer the admiralty-scale tags when present. With only a STIX `confidence` or a `misp:confidence-level` tag, map back to credibility with the table, and set reliability to `F` when nothing states it. Either way the item is flagged `derived_from_confidence`, so `/quality-of-information-check` re-grades it when a primary is available.

**Ungraded IOCs.** Without evidence items, set `confidence` per the `confidence-levels` skill and leave the Admiralty fields and tags off. Do not invent a grade to fill the column.

## MISP Attribute Types

| IOC Type | MISP attribute type | Category |
|----------|-------------------|----------|
| IPv4 address | ip-dst / ip-src | Network activity |
| IPv6 address | ip-dst / ip-src | Network activity |
| Domain | domain | Network activity |
| URL | url | Network activity |
| Email address | email-src | Payload delivery |
| SHA-256 hash | sha256 | Payload delivery |
| MD5 hash | md5 | Payload delivery |
| SHA-1 hash | sha1 | Payload delivery |
| Filename | filename | Payload delivery |
| Registry key | regkey | Persistence mechanism |
| Mutex | mutex | Artifacts dropped |

## Export Workflow

1. Collect all IOCs from the investigation/analysis
2. Deduplicate (same indicator + same type = one entry)
3. Validate format (IP regex, hash length, URL format)
4. Apply TLP marking (inherit from source or set explicitly)
5. Set confidence: from the claim's grade when evidence items exist (see Grades on export), otherwise per the confidence-levels skill
6. Attach the primary source to each indicator (source, URL)
7. Generate export in requested format
8. Write to `data/exports/YYYY-MM-DD-<context>.<format>`

## Output Location

Write exports to: `data/exports/`
- CSV: `YYYY-MM-DD-<context>.csv`
- STIX: `data/stix-bundles/YYYY-MM-DD-<context>.json`
- OpenIOC: `YYYY-MM-DD-<context>.ioc`
- MISP: `YYYY-MM-DD-<context>.misp.json`
