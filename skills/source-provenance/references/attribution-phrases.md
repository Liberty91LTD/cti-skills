# Attribution, confidence and access phrases

The pattern lists used by `scripts/resolve_provenance.py`. The patterns live in the script (`ATTRIBUTION_PATTERNS`, `CONFIDENCE_PATTERNS`, `HEDGE_PATTERNS`, `ACCESS_PATTERNS`); this file documents them, with examples and known false positives. If you change one, change both.

All matching is case-insensitive and works on sentences from the article body only. Navigation, footers, sidebars and related-article blocks are removed first. Table rows are kept, one line per row.

Attribution phrases are also matched in the primary. A primary that says "Researchers at X found" is relaying X for that statement; the script reports it as `primary_relays`.

## 1. Attribution phrases

These mark a sentence in which an outlet says where its information came from. The script records the sentence, any organisation from `source-types.md` named in it, and any link inside it. A link inside an attribution sentence outranks every other link in the article when the script picks the primary.

| Pattern | Example match |
|---|---|
| `according to` | "According to a report by Unit 42, the group..." |
| `researchers (at\|from\|with)` | "Researchers at ESET found..." |
| `in a (new )?(report\|blog post\|advisory\|analysis\|write-up\|technical write-up)` | "Sophos said in a report published Tuesday" |
| `(said\|wrote\|noted\|stated\|explained\|warned) in (a\|an\|its\|their)` | "Microsoft said in a blog post" |
| `published by` | "an analysis published by Volexity" |
| `(a\|an\|the) (joint )?advisory` | "the joint advisory from CISA and the FBI" |
| `disclosed` | "Mandiant disclosed that..." |
| `told <Outlet>` | "a spokesperson told BleepingComputer" |
| `(first )?(reported\|spotted\|discovered\|uncovered\|documented\|detailed) by` | "first documented by Kaspersky" |
| `findings from` / `data from` / `telemetry from` | "telemetry from Cloudflare shows" |
| `shared with` | "in a statement shared with The Record" |
| `(8-K\|SEC) filing` / `filed with` | "said in an 8-K filing" |
| `(data )?leak site` / `posted on (its\|their) .* (site\|blog\|channel)` | "listed the company on its leak site" |

### False positives to expect

- **"according to"** also introduces documentation and statistics ("according to the vendor's documentation"). The script does not treat the phrase as proof of a primary; it only raises the rank of a link or organisation in the same sentence.
- **"disclosed"** is used for vulnerabilities ("the flaw was disclosed in March") as often as for reports. Same handling.
- **"told"** marks a direct statement to the journalist. There is usually no document to link. These become claims of the quoted organisation with `access: statement`; see `/claim-extraction`.
- **"advisory"** can refer to a vendor's patch advisory for the vulnerable product, which is a primary for the vulnerability but not for the exploitation or attribution claims.

### Unattributed sourcing

These phrases are recorded as findings. They mark a claim the script cannot trace, and the script will not guess a primary for them.

| Pattern | Example |
|---|---|
| `researchers (say\|said\|have\|warn)` with no organisation in the sentence | "Researchers say the group has shifted tactics" |
| `security experts` / `experts (say\|warn)` | "Experts warn the campaign is ongoing" |
| `sources (say\|said\|familiar with)` | "sources familiar with the matter" |
| `reports (suggest\|indicate)` / `it is (believed\|reported)` | "It is believed the attackers..." |

## 2. Confidence language

Extracted from the primary only. `stated_confidence` is the verbatim sentence, or `"not stated"`.

| Pattern | Example |
|---|---|
| `(assess\|assesses\|assessed\|assessment) .{0,40}(with )?(low\|moderate\|medium\|high) confidence` | "We assess with moderate confidence that..." |
| `(low\|moderate\|medium\|high)[- ]confidence` | "a high-confidence attribution" |
| `with (low\|moderate\|medium\|high) confidence` | "attributes the activity with high confidence to" |
| `confidence (level\|is)` | "our confidence level in this attribution is low" |

## 3. Hedging language

Recorded separately from confidence language, as `hedges`. Used by `/quality-of-information-check` when judging whether an outlet dropped a caveat.

`likely`, `unlikely`, `suspected`, `possibly`, `potentially`, `probably`, `may have`, `might`, `appears to`, `we believe`, `believed to`, `consistent with`, `overlaps with`, `linked to`, `attributed`, `cannot confirm`, `could not confirm`, `unconfirmed`, `alleged`, `claims`, `claimed`.

### False positives to expect

- **"likely"** and **"may"** appear in mitigation advice ("organisations may wish to..."). The script keeps the whole sentence so a reader can tell.
- **"attributed"** covers both "we attribute this to" (the primary's own judgement) and "which has been attributed to" (a reference to someone else's judgement). The second is derivative inside the primary and should be traced separately.

## 4. Access phrases

Read from the primary's own text. Mapped to an access type. If nothing matches, access is `undisclosed`. Access is never inferred from who the organisation is.

| Access type | Patterns |
|---|---|
| `telemetry` | `our telemetry`, `(our\|its\|their) (own )?(sensors\|telemetry\|visibility\|customer base\|honeypots?)`, `we (have )?observed`, `we (have )?detected`, `(observed\|detected\|blocked) (by\|in) (our\|its)`, `(product\|endpoint\|network) telemetry` |
| `ir_engagement` | `incident response (engagement\|investigation\|case)s?`, `during (an\|a recent\|our\|the) (investigation\|engagement\|response)`, `(were\|was) engaged (by\|to)`, `responded to (an\|a\|the) (incident\|intrusion\|breach)`, `forensic (analysis\|investigation\|examination)` |
| `sample_analysis` | `sample(s)? (was\|were )?(submitted\|uploaded\|obtained\|shared)`, `uploaded to VirusTotal`, `we (analy[sz]ed\|reverse[- ]engineered)`, `(static\|dynamic) analysis`, `reverse engineering` |
| `osint` | `open[- ]source (reporting\|information\|intelligence\|research)`, `publicly (available\|reported)`, `public reporting`, `previously (reported\|documented) by` |
| `victim_statement` | `(8-K\|10-K\|SEC) filing`, `notification (letter\|to affected)`, `we (recently )?(discovered\|identified\|detected\|became aware of) (unauthorized\|unauthorised\|suspicious)`, `breach notification` |
| `actor_statement` | `leak site`, `ransom note`, `posted on (a\|an\|the) (forum\|Telegram)`, `claimed responsibility` |

A match that follows a negation in the same clause is ignored (`no`, `not`, `never`, `without`, `neither`, `nor`, `n't`). "We did not observe a ransom note" is a statement about what the vendor did not see, not evidence that it read an actor's statement.

When more than one type matches, the script reports every match in `access_evidence` and sets `access` to the type with the most matching sentences. Ties resolve in table order. The agent should read `access_evidence` and correct the value if the matches are about someone else's access ("CISA said it observed...", inside a vendor blog).

### False positives to expect

- **"we observed"** in a press article is the outlet quoting the vendor. The script only runs access extraction on the primary document, never on an intermediary.
- **"forensic analysis"** in a government advisory may describe a partner's work. Check the sentence.
- A primary that aggregates ("public reporting indicates...") alongside its own telemetry will match both `osint` and `telemetry`. That mix is itself relevant to the grade: see access level indirect in the grading rubric.

## 5. Dates

Publication date, in order of preference:

1. JSON-LD `datePublished`
2. `<meta property="article:published_time">`
3. `<meta name="date">`, `pubdate`, `publish-date`, `parsely-pub-date`, `DC.date.issued`, `dcterms.created`, `sailthru.date`
4. First `<time datetime="...">` in the article body

If none is present the date is `null` with reason `no publication date in page metadata`. The script does not read dates out of prose, and it never sets `date_observed`: when the activity happened is stated in the text, if at all, and is recorded by `/claim-extraction`.
