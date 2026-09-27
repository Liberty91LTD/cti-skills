# How evidence grading works, in plain English

This page explains what version 2.0 of the pack does and why it matters. It assumes no background in intelligence analysis.

## The short version

Before the AI is allowed to draw a conclusion, it has to show where each piece of information came from and how much weight that information can carry. The checking is done by ordinary software with fixed rules, not by the AI's own impression. The AI's conclusion can then be no more confident than its weakest piece of evidence allows.

## The problem this solves

### Most security news is a copy of a copy

When a security company discovers something, it publishes a report. A news site writes about the report. A second site rewrites the first site's article. By the end of the week there may be fifteen articles.

Those fifteen articles are one source. Only the security company saw anything. Everyone else is passing it along.

Two things go wrong when nobody keeps track of this:

- **One source looks like many.** "It's being reported everywhere" feels like confirmation. It is repetition.
- **Caution gets lost along the way.** The company wrote "this is possibly linked to group X". Two articles later it reads "group X did it". Nobody lied. Each rewrite was a little more certain than the last.

### An AI can sound careful without being careful

Analysts have structured methods for testing a conclusion: list every possible explanation, line up the evidence against each one, and see which explanations the evidence rules out.

Ask an AI to do this and it will produce something that looks exactly right. The table is there. The headings are there. But if the AI already had a favourite answer, and chose for itself which evidence to trust, the table is decoration. It gives a hunch the appearance of a method.

A pack user put the question to us directly: how do you stop the AI from doing the analysis by feel? Version 2.0 is the answer.

## What happens now, step by step

Say you hand the pack a news article and ask who was behind an attack.

### 1. Trace it back to whoever actually saw something

A small program follows the links in the article to find the original report. It is a plain script. It does not guess and it has no opinions.

If it finds the original, it records the chain: this article, which came from that report, published on this date. If it cannot find an original, it says so. "This article names no source and links none" is a useful answer, and the AI is not allowed to fill the gap from memory.

### 2. Split the report into separate claims

A single report usually mixes very different kinds of statement. Take this sentence:

> A criminal group broke into a hospital through a flaw in its network equipment and stole 400 gigabytes of data.

That is four claims:

| Claim | Who is really saying it | How solid it is |
|---|---|---|
| The hospital was broken into | The hospital, in its legal notice | Very solid |
| They got in through the network equipment | The investigators who examined it | Solid |
| This particular group did it | Someone's reasoned judgment | A judgment, not a fact |
| 400 gigabytes were taken | The criminals themselves | Unverified. They gain from exaggerating |

Give the whole sentence one score and you either trust the criminals too much or the hospital too little. So each claim is handled separately, and each is pinned to the exact sentence it came from so anyone can check it.

### 3. Grade each claim using fixed rules

Each claim gets two marks, using a scale that military and intelligence services have used for decades:

- **How well placed was the source to know?** Did they see it themselves, examine a sample, or read about it?
- **Has anyone else confirmed it independently?** That means someone with their own evidence, not someone repeating the first report.

The rules have hard limits the AI cannot argue its way past. For example:

- If the original source cannot be found, the claim's grade is capped.
- What criminals say about their own haul counts as unverified until someone else confirms it.
- "Who did it" can never get the top mark on one source's say-so.
- A famous name earns nothing by itself. A grade must rest on how the source knows, not on who the source is.

### 4. Check the work

A second program checks every grade against the rules. If a grade is higher than the rules allow, or a claim has no sentence behind it, the output is rejected.

### 5. Only then, reason

The analysis tools now refuse to start on evidence that has not been graded. When they do run, two rules apply:

- **Evidence that fits every explanation counts for nothing.** If a fact would be true whichever explanation is right, it cannot help you choose between them, however reliable it is.
- **Confidence is limited by the weakest link.** If the conclusion depends on a claim that only one source has made, the pack will not call that conclusion "high confidence". If the key claim cannot be verified at all, the pack gives no confidence level and tells you what is missing.

## What you see in your own network counts most

One kind of evidence sits at the top of the scale: what your own systems recorded. If a suspicious address shows up in your own logs, nobody needs to confirm it for you. You saw it.

The reverse is not true. Finding nothing in your logs does not prove nothing happened. The logs may not cover that part of the network, or may not go back far enough. The pack reports this as "not seen in the data we have" and never as "you are safe".

## What is checked by software and what is judged by the AI

| Done by fixed software | Judged by the AI, and labelled as such |
|---|---|
| Following links to the original report | Deciding what kind of claim each statement is |
| Recording who published what, and when | Judging whether an article changed the original's meaning |
| Classifying a website as a company, government, news outlet and so on | Writing the reason for each grade |
| Checking every grade against the limits | Asking whether someone had a motive to mislead |

Every result carries a label saying how the source was traced: by the platform, by the script, or reconstructed by the AI from pasted text. That label follows the evidence into anything built on it, so a reader can always see how firm the footing is.

## Why this is significant

- **You can check it.** Every claim points to a sentence. Every grade has a stated reason. Nothing rests on "the AI said so".
- **It is honest about what it does not know.** We ran the tracing program on 30 real articles. It found the original source for 15. The other 15 rested on social media posts, on statements with no document behind them, or on nothing at all. Those are reported as findings and graded accordingly.
- **It resists the most common mistake in the field**, which is treating loud as true.
- **It does not rate companies.** The pack keeps a list of what each organisation is and how it usually gets its information. It deliberately keeps no list of who to trust. Trust is worked out claim by claim, every time.
- **It rests on established practice.** The grading scale and the sourcing rules come from published intelligence standards. Our own additions are the step that measures how faithfully each article passed the original along, and the split between software-checked facts and AI judgment.

## What it cannot do

- It cannot tell you whether a claim is true. It tells you how well supported a claim is, which is a different and more useful question when you cannot know the truth.
- It cannot trace what is not linked. An article that cites nothing stays untraced.
- Finding an original report does not mean every line of the article came from it. The pack compares them claim by claim for that reason.
- Tracing across a whole news event at once, using the Liberty91 platform, is built into the pack and switches on when the platform begins supplying that data. Until then the pack traces the articles you give it.

## Where to go next

- To try it: give the pack an article link and ask "how reliable is this?"
- For the rules themselves: [`grading-rubric.md`](../skills/quality-of-information-check/references/grading-rubric.md)
- For where the method comes from: [`doctrine.md`](../skills/quality-of-information-check/references/doctrine.md)
- For the test results: [`tests/provenance/`](../tests/provenance/README.md)
