---
name: ioc-export
description: IOC export formats and procedures. CSV, STIX 2.1, OpenIOC, MISP. Handles format conversion and packaging.
user-invocable: false
metadata:
  version: 1.0.0
---

# IOC Export Guide

## Supported Export Formats

### CSV
Standard tabular format. Most broadly compatible.

```csv
indicator,type,first_seen,last_seen,confidence,tlp,source,context,mitre_attack,tags
203.0.113.42,ipv4-addr,2026-01-15,2026-03-20,85,GREEN,"Mandiant report MAL-2026-001",C2 server for SUNBURST variant,T1071.001,"apt29;sunburst"
evil.example.com,domain-name,2026-02-01,2026-03-20,70,GREEN,"Internal analysis","Phishing landing page",T1566.002,"phishing;apt29"
```

**Column definitions:**
| Column | Required | Description |
|--------|----------|-------------|
| indicator | Yes | The IOC value |
| type | Yes | STIX indicator type: ipv4-addr, ipv6-addr, domain-name, url, file:hashes.SHA-256, file:hashes.MD5, email-addr |
| first_seen | Yes | ISO date first observed |
| last_seen | No | ISO date last observed |
| confidence | Yes | 0-100 MISP confidence score |
| tlp | Yes | TLP marking |
| source | Yes | Source description |
| context | No | What the IOC represents (C2, phishing, etc.) |
| mitre_attack | No | ATT&CK technique IDs |
| tags | No | Semicolon-separated tags |

### STIX 2.1 Bundle
See `stix-bundle` skill for full specification.

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
        "comment": "C2 server"
      },
      {
        "type": "domain",
        "category": "Network activity",
        "value": "evil.example.com",
        "to_ids": true,
        "comment": "Phishing landing page"
      }
    ]
  }
}
```

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
5. Set confidence scores (per confidence-levels skill)
6. Generate export in requested format
7. Write to `data/exports/YYYY-MM-DD-<context>.<format>`

## Output Location

Write exports to: `data/exports/`
- CSV: `YYYY-MM-DD-<context>.csv`
- STIX: `data/stix-bundles/YYYY-MM-DD-<context>.json`
- OpenIOC: `YYYY-MM-DD-<context>.ioc`
- MISP: `YYYY-MM-DD-<context>.misp.json`
