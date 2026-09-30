# Deception screen

Four checks from Heuer and Pherson's deception detection technique, with prompts written for CTI source material. The screen inside a Quality of Information Check is short: a few sentences per check. It raises flags. It does not settle whether deception occurred.

Run it in full when:

- any claim is an `actor_claim`;
- attribution rests on artefacts an adversary controls (language strings, compile times, tool choice, infrastructure reuse);
- a single source carries the bottom line;
- the information arrived at a moment that suits someone.

Answer from the documents and from resolved data. Where a prompt asks about history ("does this actor inflate its claims?"), use a knowledge cell or a lookup and cite it, or answer "not established".

## MOM: motive, opportunity, means

Could someone be deceiving us, and would they want to?

| Prompt | Notes |
|---|---|
| Who benefits if this claim is believed? | The actor (pressure on the victim, reputation among affiliates), the victim (minimising), the vendor (commercial interest), a state (deflection) |
| Does the actor gain from overstating scale? | Extortion leverage depends on the victim and the public believing the figure |
| Does the victim gain from understating? | Disclosure wording is drafted with legal and market exposure in mind |
| Does the primary have a commercial interest in this finding? | Read `primary_source.interest`. A vendor reporting on a threat its product addresses, or on a competitor's product, sets `commercial_interest` |
| Could the adversary have planted the artefacts the attribution rests on? | Language settings, code comments, reused tooling and working-hours patterns are all within the adversary's control |
| Did the source have the opportunity to know what it claims? | This is the access question again. An actor knows what it took. A vendor without an engagement at the victim does not |

## POP: past opposition practices

Has this adversary deceived before, and how?

| Prompt | Notes |
|---|---|
| Does this actor have a history of inflating victim counts or data volumes? | Check `/ransomware-ecosystem`, `/lookup-ransomwarelive` |
| Has this actor re-posted old or third-party data as a new breach? | A recurring pattern on leak sites and forums |
| Has this actor or its sponsor used false-flag techniques? | Check the relevant regional knowledge cell |
| Is this a persona with a record of claiming others' operations? | Common among hacktivist fronts. Check `/hacktivism` |
| Does the claim fit the pattern of the actor's earlier statements that later proved accurate or inaccurate? | If no record is available, say so |

## MOSES: manipulability of sources

How easily could the source have been fed this?

| Prompt | Notes |
|---|---|
| Does the claim rest on a single sample, a single upload, or a single forum post? | Anyone can upload a file to a public sandbox |
| Is the source relaying what it was told, without its own observation? | A journalist quoting the actor, a vendor quoting a leak site |
| Could the source be the target of the message? | Actors speak to journalists and researchers because they will repeat it |
| Does the chain pass through a platform where identity is unverified? | Social posts and Telegram channels. The account holder is the source, and the account may not be who it says |
| Is the indicator set something an adversary could seed? | Infrastructure that is abandoned, shared or deliberately exposed |

## EVE: evaluation of evidence

Does the evidence hold together?

| Prompt | Notes |
|---|---|
| Is the claim consistent with the other claims from the same primary? | Internal contradictions lower claim support to disputed |
| Is it consistent with other primaries? | A conflict between two credible primaries sets `disputed` |
| Do the dates work? | Activity dated after publication, a "new" sample with an old compile time and old submissions |
| Is anything conspicuously missing? | Attribution with no stated basis. A breach claim with no sample data. An exploitation claim with no indicators |
| Is the evidence too neat? | Every artefact pointing at one actor, with no noise, in a domain where artefacts are cheap to forge |
| Has any part been retracted, corrected or superseded? | Set `retracted` or `superseded` |

## Recording the result

In the human-readable output, four short paragraphs or a four-row table, then the flags raised.

In the JSON envelope:

```json
"deception_screen": {
  "mom": "The 400GB figure serves the actor's extortion leverage. The vendor has a commercial interest but reports no finding that depends on its own product.",
  "pop": "Not established. No record of this actor's earlier claims was available in this run.",
  "moses": "C07 rests on a single leak-site posting relayed by the press.",
  "eve": "Dates are consistent. The attribution states its basis. No sample data accompanies the volume claim.",
  "flags_raised": [
    {"claim_id": "C07", "flag": "deception_indicators_present", "reason": "Actor has motive to inflate; single unverified posting; no sample data."}
  ]
}
```

A raised flag does not change a grade by itself. It is recorded on the claim, shown to the reader, and carried into `/ach`, where a hypothesis that depends on a flagged claim is marked as doing so.

## What the screen is not

It is not the full deception detection technique, which is a separate structured exercise. And it is not a reason to discount everything an actor says. Actors' claims are often true. Their access level is adversary because the source has a motive to mislead and cannot be held to account, and their claim support rises when someone with separate access confirms them.
