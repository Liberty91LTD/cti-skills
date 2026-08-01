# ATT&CK Technique-to-Control-Effectiveness Mapping: Methodology

Version 1.0, built 2026-07-30. Every step below is reproducible from the cited public sources. No proprietary data, no analyst judgment beyond the stated transformation rules.

## 1. What this is and is not

This dataset maps MITRE ATT&CK Enterprise techniques to security controls, with an effectiveness assessment **where a public source provides one**, and an explicit "coverage-only" label where it does not.

It is not a claim that any control stops any technique in a specific environment. It is the public evidence base from which a per-customer Resistance Strength assessment can be built and audited.

## 2. Sources, exact versions

| # | Source | Publisher | Version pin | What it contributes |
|---|--------|-----------|-------------|---------------------|
| 1 | ATT&CK Enterprise STIX 2.1 | MITRE | v19.1 | Native technique-to-mitigation links (M-codes), technique metadata, detection data components |
| 2 | Mappings Explorer: NIST SP 800-53 | MITRE Center for Threat-Informed Defense (CTID) | ATT&CK 16.1 / 800-53 rev5, last updated 2025-04-16 | Technique-to-800-53-control coverage |
| 3 | Mappings Explorer: AWS | MITRE CTID | ATT&CK 16.1 / AWS 2024-12-12 | Scored capability mappings |
| 4 | Mappings Explorer: Azure | MITRE CTID | ATT&CK 16.1 / Azure 2025-04-26 | Scored capability mappings |
| 5 | Mappings Explorer: GCP | MITRE CTID | ATT&CK 16.1 / GCP 2025-03-06 | Scored capability mappings |
| 6 | Mappings Explorer: M365 | MITRE CTID | ATT&CK 16.1 / M365 2025-07-18 | Scored capability mappings |

Retrieval: source 1 from `raw.githubusercontent.com/mitre-attack/attack-stix-data`, sources 2-6 from the `center-for-threat-informed-defense/mappings-explorer` GitHub repository (main branch, retrieved 2026-07-30). Anyone can re-download these files and diff against the Master_Mapping sheet.

## 3. Extraction rules

1. **Techniques.** All `attack-pattern` objects from ATT&CK v19.1 with `revoked = false` and `x_mitre_deprecated = false`. Result: 697 active techniques (parent and sub-technique).
2. **Native mitigations.** All `relationship` objects of type `mitigates` where the source is an active `course-of-action` with an M-prefixed ATT&CK ID and the target is an active technique. Result: 1,448 pairs across 44 mitigations.
3. **CTID mappings.** From each framework's ATT&CK-16.1 enterprise JSON, every `mapping_object` excluding rows with `status = non_mappable` or a null `capability_id`. Result: 5,314 NIST rows; 487 AWS; 972 Azure; 518 GCP; 806 M365.
4. **Detection signal.** Count of `detects` relationships (data components) per technique from ATT&CK v19.1, carried as context only, never converted into an effectiveness score.

Total: 9,545 normalized rows.

## 4. The effectiveness column: where scores come from

Only CTID's four security-stack mappings assign effectiveness. Their published methodology scores each vendor capability against each technique on two axes, and we carry both through **unmodified**:

- **function**: protect / detect / respond
- **effectiveness**: minimal / partial / significant

The native ATT&CK mitigations and the NIST 800-53 mapping are binary assertions of relevance. These rows carry `effectiveness = coverage-only`.

**Rule: no score is ever synthesized.** Where the evidence is coverage-only, the honest statement is "a recognised body asserts this control addresses this technique, with no strength claim." The Technique_Summary sheet instead computes a **corroboration count** (distinct sources mapping any control to the technique), which is a defensible quantity: it measures agreement between independent mapping efforts, not effectiveness.

## 5. Derived fields (Technique_Summary)

All computed by live spreadsheet formulas against Master_Mapping so an auditor can trace every number:

- Counts of native mitigations, NIST controls, and scored cloud rows per technique
- Counts of `significant` and `partial` scored rows
- Distinct-source corroboration count (1-6)
- A coverage flag: `scored: significant available` / `scored: partial-minimal only` / `coverage-only` / `NO MAPPED CONTROL`

Distribution across the 697 current techniques: 220 have at least one significant-scored control, 283 have scored controls at partial/minimal only, 162 are coverage-only, 32 have no mapped control in any source.

## 6. Known limitations, stated for audit

1. **Version skew.** CTID pins to ATT&CK 16.1; native data is 19.1. Techniques introduced after 16.1 can only appear via native mitigations or not at all. This accounts for most of the 32-technique gap list. Fix on CTID's next release; the Sources sheet records the pins so the skew is visible, not hidden.
2. **Scores are capability-specific.** CTID's `significant` for an Azure capability describes that product's coverage, not the generic control class. Treating it as a proxy for the class is an analytical choice the consumer makes, and should be disclosed when doing so.
3. **Asymmetric evidence.** Absence of a mapping is absence of evidence, not evidence of ineffectiveness. The 32 unmapped techniques include several where ATT&CK itself states the technique cannot be easily mitigated by preventive controls (e.g., several discovery techniques), which is information, not a data gap.
4. **Scores are point-in-time expert judgment.** CTID's scoring rubric is public but the assessments are analyst judgment, not empirical test results. For empirical grounding, pair with breach-and-attack-simulation or purple-team results per customer; that data supersedes this mapping wherever it exists.
5. **No efficacy under adversary adaptation.** A `significant` rating does not model an attacker who pivots to an unscored sibling sub-technique. Population-level capability data (which techniques actors actually chain) is the correction, and is outside the scope of public mappings.

## 7. Intended use in FAIR

This mapping supports the **Resistance Strength** side of the Vulnerability node. Given a customer's implemented control set (mapped to 800-53 families or specific cloud capabilities), filter Master_Mapping to their controls, join against the technique set of the relevant threat community, and the result is an auditable statement of which attacker techniques the customer's controls address, at what evidenced strength. Vulnerability estimation then becomes an argument about a table both sides can read, instead of a percentage produced in a workshop.

## 8. Extension roadmap (public sources not yet incorporated)

- **MITRE D3FEND**: defensive technique ontology with ATT&CK "counters" relationships; adds a second independent mapping voice.
- **CTID Attack Flow / Sensor Mappings**: sequences and telemetry-to-technique links.
- **CIS Controls v8 community mapping**: widely used by mid-market customers who don't speak 800-53.
- **CTID Summiting the Pyramid**: scores detection analytics by robustness to evasion, the detection-side analogue of this dataset.
