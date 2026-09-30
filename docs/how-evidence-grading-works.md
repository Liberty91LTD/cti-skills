# How evidence grading works, in plain English

This page explains, step by step, what the pack does when you ask it how reliable a piece of security news is. It assumes no background in intelligence analysis.

The example used throughout is invented.

## What it does, in one paragraph

You give the pack an article. It finds out who originally reported the information, breaks the report into separate statements, and gives each statement a grade. The grade says how much weight that statement can carry. When the pack later draws a conclusion, the conclusion can be no more confident than the weakest statement it depends on.

## Three words used on this page

| Word | Meaning here |
|---|---|
| **Original source** | Whoever first reported the information: the security company that investigated, the government agency that issued a warning, the organisation that was attacked, or the attackers themselves. |
| **Claim** | One statement that says one thing. "The hospital was broken into" is a claim. |
| **Grade** | Two words, such as "direct, firm". The first word says how the source knows. The second says what backs the statement. |

## The example

You read this in a news article and want to know how far to trust it:

> A criminal group broke into a hospital through a flaw in its network equipment and stole 400 gigabytes of data.

You give the pack the link and ask, "How reliable is this?"

## Step 1. Find the original source

News sites mostly report what someone else found. A security company publishes a report, a news site writes about it, and other sites write about that article. Fifteen articles can all lead back to one report.

A small program follows the links in your article until it reaches the original report. It records each stop on the way:

> this article → an earlier article → the security company's report

This program is ordinary software. It follows fixed rules and gives the same answer every time.

If the article links to no original source, the program says so. The AI is not allowed to fill that gap from memory.

## Step 2. Break the report into claims

The sentence in the example contains four claims. Each comes from a different place.

| Claim | Who is saying it | What kind of claim it is |
|---|---|---|
| The hospital was broken into | The hospital, in its legal notice | A statement by the victim |
| The attackers got in through the network equipment | The investigators who examined the systems | Something that was observed |
| This particular group did it | The investigators | A judgement about who is responsible |
| 400 gigabytes were taken | The criminals | A statement by the attackers |

The pack copies the exact sentence each claim came from, word for word. You can open any claim and read the sentence behind it.

## Step 3. Check whether the wording changed along the way

The pack compares what the article says with what the original report says.

Suppose the report said the attack was "possibly linked to" the group, and the article says the group "was behind" it. The pack records that the caution was dropped, and it grades the claim on the original wording.

## Step 4. Count who else confirms it

A claim is confirmed when a second organisation reports the same thing from its own evidence.

These do not count as confirmation:

- Several articles about the same report.
- One company quoting another company.
- A government warning that repeats a company's report and adds nothing of its own.

Unless the pack finds a second organisation with its own evidence, it records the claim as resting on one source.

## Step 5. Grade each claim

Each claim gets two words.

**First word, the access level: how does the source know this?**

| Access level | Meaning |
|---|---|
| Direct | The source saw it: in its own systems, in its own investigation, or because it is the organisation that was attacked |
| Limited | The source examined a piece of evidence, such as a sample of the malicious software, but did not see the attack itself. Or a named person at the source said it to a journalist |
| Indirect | The source does not say how it knows, or is repeating what others have published |
| Untraced | No original source could be found |
| Adversary | The attackers said it themselves |

**Second word, the claim support: what backs this statement?**

| Claim support | Meaning |
|---|---|
| Established | A second organisation confirms it from its own evidence. Or you saw it in your own systems |
| Firm | One source, which saw it directly, and nothing contradicts it |
| Tentative | One source, and the statement is either second-hand or is a conclusion the source reached |
| Disputed | Something contradicts it, or the source itself says it has low confidence |
| Unverified | There is nothing to judge it by |

In the example, the four claims come out like this:

| Claim | Access level | Claim support | Reason |
|---|---|---|---|
| The hospital was broken into | Direct | Firm | The hospital reported it, and it is in a position to know. No second source yet. |
| The attackers got in through the network equipment | Direct | Firm | The investigators examined the systems themselves. No second source yet. |
| This particular group did it | Direct | Tentative | The investigators are well placed, but this is a conclusion they reached, and they stated moderate confidence. |
| 400 gigabytes were taken | Adversary | Unverified | Only the criminals say so, and they gain from exaggerating. |

### Why two claims from the same source get different grades

The second and third claims both come from the investigators, and both rest on that one source. They get the same access level and a different claim support. The reason is the difference between what a source saw and what a source concluded.

**What a source saw.** The investigators examined the hospital's network equipment and found how the attackers got in. This is an observation. If the investigators are honest and competent, it is true. One source that saw something directly is enough for "firm".

**What a source concluded.** The investigators then decided which group was responsible. Nobody saw the group. The investigators compared the tools and methods with what they know about that group and reached a conclusion. Another investigator with the same evidence could reach a different one. One source's conclusion is "tentative" at best.

The same applies to any statement about what the attackers wanted or what they will do next. These are conclusions too.

| Kind of statement | Example | Best claim support on one source |
|---|---|---|
| Something seen | "The attackers got in through the network equipment" | Firm |
| A conclusion about who did it | "This group did it" | Tentative. Firm only if the source states high confidence |
| A conclusion about intent or the future | "The group will target more hospitals" | Tentative |

To reach "established", any of these needs a second organisation that confirms it from its own evidence.

## Step 6. Apply the limits

Some grades are not allowed, whatever the AI thinks. The main limits:

- If no original source was found, the access level is "untraced" and the claim support is "tentative" at best.
- What attackers say about how much they stole is "unverified" until someone else confirms it.
- A statement about who was responsible cannot be "established" unless two organisations reached that conclusion separately.
- A source that does not say how it knows gets the access level "indirect" at best.
- A well-known name earns nothing by itself. The reason for a grade must be how the source knows, not who the source is.

A second program checks every grade against these limits. If a grade breaks one, or a claim has no sentence behind it, the result is rejected and has to be corrected.

## Step 7. Show the result

You get back:

- A short summary in plain language.
- A table of the claims with their grades and the reason for each.
- The chain from your article to the original source.
- A list of what the evidence cannot tell you.
- A note saying which parts were checked by software and which were judged by the AI.

## This is not the Admiralty scale

Analysts will know the Admiralty scale, which rates a source with a letter from A to F and a piece of information with a number from 1 to 6. A rating looks like "B2".

The pack's grade is a different thing. It is written in words so that the two cannot be confused.

| | Admiralty scale | The pack's grade |
|---|---|---|
| What the first part measures | **Track record.** How often this source has been right in the past | **Access level.** How the source knows this particular thing |
| Where that comes from | Experience with the source over time | What the report itself says about how the finding was made |
| What it belongs to | The source | The individual claim |
| Two claims from one source | Get the same rating | Can get different access levels |
| How it is written | A letter and a number | Two words |

**Track record** answers the question "has this source been right before?" To answer it you need a history of the source's past claims and how they turned out. The pack does not have that history. Without it, a rating such as "usually reliable" would be the AI's impression of a company's reputation.

**Access level** answers the question "was this source in a position to know this?" The answer is in the report. A report either says "we saw this in our own systems" or it does not. Two people reading the same report reach the same answer.

Access level also changes from claim to claim. One report can contain something the company saw itself, something it learned from a sample another company shared, and a summary of what the press has said. Those are three different access levels from one source.

Track record is still useful. When the Liberty91 platform can calculate it from data, it will be shown next to the grade as a separate item. It will not change the access level.

The pack still uses the Admiralty scale in one place: rating the results of lookups against outside databases. Those ratings are labelled as Admiralty. They are never mixed with the grades described here.

## What happens when the pack draws a conclusion

If you go on to ask the pack for an assessment, it uses the graded claims. Two rules apply.

### The weakest link sets the confidence

The pack finds the claims its conclusion depends on and takes the weakest among them.

| Weakest claim the conclusion depends on | Most confidence the conclusion can have |
|---|---|
| Established | High |
| Firm | Moderate |
| Tentative | Low |
| Disputed or unverified | None. The pack says what is missing |

An access level of "untraced" or "adversary" lowers the result by one step.

In the example, a conclusion that the hospital was attacked through its network equipment can have moderate confidence. A conclusion that names the group can have low confidence. A conclusion about how much was stolen gets no confidence level.

### A fact only counts if it helps choose between explanations

This rule applies when there is more than one possible explanation and the pack has to weigh them.

Say there are two explanations for the hospital attack:

- Explanation 1: group X did it.
- Explanation 2: group Y did it.

Now take three facts, all of them well supported.

| Fact | Fits group X? | Fits group Y? | Does it help choose? |
|---|---|---|---|
| The attackers got in through a flaw in the network equipment | Yes. Group X uses this flaw | Yes. Group Y uses it too | No |
| The attack happened at night | Yes | Yes | No |
| The malicious software contains code that has only ever been seen in group X's tools | Yes | No | Yes |

The first two facts are true whichever group did it. They tell you that an attack happened and how. They tell you nothing about who. Only the third fact separates the two explanations.

The pack puts the first two facts to one side when it weighs the explanations. It still lists them in the report, marked as not helping to choose.

This matters because of a common mistake. A long list of well-supported facts looks like strong evidence. If every fact on the list fits both explanations, the list supports neither one over the other. Counting those facts would make whichever explanation was written first look stronger than it is.

A fact that is put to one side is not being called false or weak. It may be the best-supported fact in the report. It is set aside only for the question of choosing between explanations.

## If you skip the grading

The pack grades the evidence first unless you tell it not to. You can tell it not to.

If you do, the pack still writes the assessment. It marks the result "Evidence basis: ungraded" and never gives it more than moderate confidence.

## What you see in your own systems

If a suspicious address shows up in your own logs, that is graded "direct, established", the top of the scale. You saw it yourself, so nobody else needs to confirm it.

Finding nothing in your logs is different. It is not proof that nothing happened. The logs may not cover that part of the network or may not go back far enough. The pack reports this as "not seen in the data we have".

## Who does what

| Done by fixed software | Judged by the AI, and labelled as such |
|---|---|
| Following links to the original report | Deciding what kind of claim each statement is |
| Recording who published what, and when | Judging whether an article changed the original wording |
| Classifying a website as a company, government, news outlet and so on | Writing the reason for each grade |
| Checking every grade against the limits | Asking whether someone had a motive to mislead |

Every result also says how the original source was found:

| Label | Meaning |
|---|---|
| `script-resolved` | The pack's program traced the article you gave it |
| `model-judged` | You pasted text with no link, so the AI worked out what it could. Treat as unverified |
| `platform-resolved` | The Liberty91 platform traced every article about the event. Not yet available |

## What it cannot do

- It cannot tell you whether a claim is true. It tells you how well supported the claim is.
- It cannot tell you how often a source has been right before. That is track record, and the pack does not measure it.
- It cannot trace an article that links to nothing.
- It reads text and tables. It does not read images, so indicators shown only in a screenshot are missed.
- It keeps no list of which companies to trust. It keeps a list of what each organisation is and how it usually gets its information, and works out the grade claim by claim.
- The AI's judgements can be wrong. They are labelled so you know which parts to read critically.

## How well it works so far

| Test | Result |
|---|---|
| Tracing 30 real articles | 15 were traced to an original source. The other 15 rested on social media posts, on statements with no document, or on nothing |
| Breaking five real company reports into claims | 60 claims. All 60 pointed to a sentence that was in the report word for word. A second AI reviewed them and passed 53 on every point |
| What the review found missing | Each report held more than twelve claims worth grading, and the pack stops at twelve. It tended to leave out statements about what was not found |

The reviewer in the second test was an AI, not a person. These tests were run before the grade was changed from a letter and a number to two words. The change affects how a grade is written, not how claims are found or traced.

## Where to go next

- To try it: give the pack an article link and ask "how reliable is this?"
- For the rules themselves: [`grading-rubric.md`](../skills/quality-of-information-check/references/grading-rubric.md)
- For where the method comes from: [`doctrine.md`](../skills/quality-of-information-check/references/doctrine.md)
- For the test results: [`tests/provenance/`](../tests/provenance/README.md)
