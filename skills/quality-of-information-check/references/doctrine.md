# Doctrine

Where each part of the method comes from. Use this when a reader asks "why this grade" or "whose method is this". Most of the design is assembled from established doctrine. Four parts are this pack's own and are marked as such.

## Established

### Admiralty system (what this pack's grade is not)

Source reliability A to F and information credibility 1 to 6, rated separately. Reliability is the source's track record.

*NATO, AJP-2.1 Allied Joint Doctrine for Intelligence Procedures. US Army, FM 2-22.3 Human Intelligence Collector Operations, Appendix B.*

The scale was designed for human sources: one handled individual with a history. It has no notion of derivative reporting and no dimension for access type, recency or commercial interest. Applied to a news outlet paraphrasing a vendor blog, it grades the wrong thing. Its first element also needs a history with the source that this pack does not have.

This pack takes two ideas from it: a source and a piece of information are rated separately, and corroboration by an independent source is what lifts a claim to the top. It does not use the scale. The evidence grade has its own two elements, access level and claim support, written in words, and is never shown or exported as an Admiralty rating. The rubric sets out the difference. `/source-assessment` is the pack's reference for the Admiralty scale itself.

### Quality of Information Check

A diagnostic technique that asks how confident we are in the sources, how current the information is, whether it is independently corroborated, what the chain from original observation to us is, where the gaps are, and whether deception is possible.

*CIA, A Tradecraft Primer: Structured Analytic Techniques for Improving Intelligence Analysis, 2009. Heuer and Pherson, Structured Analytic Techniques for Intelligence Analysis, 3rd ed., 2020.*

In doctrine, Admiralty grading is one tool used inside it. In this pack the evidence grade takes that place.

### Separating evidence from judgement, and confidence from likelihood

Analytic products must distinguish underlying intelligence from assumptions and judgements, and express confidence separately from likelihood.

*ODNI, Intelligence Community Directive 203: Analytic Standards, 2015.*

This is the doctrinal basis for typing claims as observation, attribution or assessment and grading them separately.

### Sourcing, derivative reporting, single-source flagging

Disseminated products must carry source descriptors, state the source's access, and make clear when reporting is derivative.

*ODNI, Intelligence Community Directive 206: Sourcing Requirements for Disseminated Analytic Products, 2015.*

The closest doctrinal ancestor of the provenance chain, and the basis for the sourcing paragraph in `/intelligence-writing`.

### Access: was the source in a position to know

How far a source can be relied on for a given matter depends on whether it was in a position to know. Standard in human source evaluation and explicit in ICD 206. In this pack: telemetry, incident response engagement, sample analysis, open source, statement.

### Primary and secondary sources, provenance, chain of custody

*UN OHCHR and UC Berkeley Human Rights Center, Berkeley Protocol on Digital Open Source Investigations, 2020.*

The protocol formalises, for online material, what historians and journalists have long practised: establish where an item originated and how it reached you before you rely on it.

### Deception detection

MOM (motive, opportunity, means), POP (past opposition practices), MOSES (manipulability of sources), EVE (evaluation of evidence).

*Heuer and Pherson, Structured Analytic Techniques for Intelligence Analysis. Heuer, Psychology of Intelligence Analysis, 1999.*

### Corroboration by originating source

Repetition is not confirmation. The Tradecraft Primer names the trap directly: many reports that trace to one origin are one report.

### Machine-readable provenance and confidence

*W3C, PROV-O: The PROV Ontology, 2013. OASIS, STIX Version 2.1: `confidence`, Sighting, Report, `external_references`. MISP taxonomies `admiralty-scale` and `estimative-language`.*

## This pack's contribution

As far as we know these are not codified elsewhere. They are offered as practice, not as doctrine.

### Transmission fidelity

A distinct assessment of each intermediary: faithful, caveats dropped, embellished, unresolved. Doctrine says to note that reporting is derivative. It does not grade how well the outlet transmitted the primary. CTI source material forces the question, because most of what an analyst reads is derivative and the commonest distortion is a hedge lost in transit.

### Vendor and press reporting as the source base

Government doctrine assumes government sources. This method applies the same discipline to commercial vendors and the press, with the primary's commercial interest as an explicit flag.

### The schema and the division of labour

The evidence item schema, claim-level grading, and the split between fields resolved by a pipeline or script and a rubric applied by a model. The split is the point: the parts of source evaluation that can be made deterministic are, and the parts that remain judgement are labelled.

### Computed track record

Doctrine assumes an analyst's memory of how a source has performed. On the Liberty91 platform this becomes a stored quantity per organisation and per claim type, built from later independent confirmations and contradictions, decaying over time, and traceable to the evidence that moved it. It is reported next to the grade, only in Tier 1. It never changes the access level, and it moves a claim's footing by one band at most. This pack does not store or ship opinions about how far named organisations can be trusted.

### The evidence grade

Two elements written in words. Access level records how the source knows the thing claimed, read from the document. Claim support records what stands behind the statement. It replaces a letter-and-number rating with terms that say what was checked, so a reader cannot mistake it for a judgement of the source's history.

## How to cite this in an output

When asked why a claim received its grade, give the rubric row and the cap that applied, then the doctrine behind it in one sentence. For example:

> C04 is direct, tentative. The attribution is the vendor's own analytical judgement, stated with moderate confidence, from a single primary. The rubric rules out established without a second independent primary (rule R4), and the vendor's own moderate confidence places it at tentative (rule R13). Grading judgements separately from observations follows ICD 203; counting corroboration by originating source follows the Tradecraft Primer.
