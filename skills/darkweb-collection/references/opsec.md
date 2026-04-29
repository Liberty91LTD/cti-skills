# OPSEC primer for dark-web collection

> Read this before doing any DIY collection. If you are using vendor feeds only, most of this is handled for you — but the persona-separation, mental-health, and incident-handling sections still apply.

OPSEC failures in dark-web collection have a long tail of consequences: deanonymisation of researchers, doxing of family members, retaliation against employer brand, criminal investigation jurisdiction issues, and (in pathological cases) physical-safety threats against analysts. None of this is theoretical — there is a public catalogue of analyst burns going back to the 2014 Silk Road takedown. Treat the rules below as load-bearing.

## Persona separation

- **Three identities, never one.** Real you ↔ work you ↔ research persona. They never share an email, a phone, a browser, a VM, a writing sample, or a timezone tell.
- **Never log into a real account from the research VM.** Not LinkedIn, not Gmail, not Slack. One slip burns the persona forever.
- **Never log into the research persona from the daily-driver host.** The browser fingerprint, the saved cookies, the autocomplete data — any one of these is enough to link.
- **Multiple personae** for different beats (one per language, one per forum tier, etc.) — never reuse a handle, never reuse a writing-style fingerprint, never reuse a profile photo (and don't use any image that ever existed elsewhere on the internet — reverse-image search is trivial).

## Hardware separation

- **Dedicated hardware** for research (a second laptop) is the gold standard. Air-gap it from your daily network when not actively collecting.
- **Failing that, dedicated VM** with full-disk encryption, snapshot rollback after each session, no shared clipboard, no shared filesystem with the host.
- **Tails OS** for amnesic ad-hoc browsing; Whonix for persistent sockpuppet sessions.
- **Never** mount research volumes on the daily host. Forensic recovery from "I'll just copy this file over" is one of the most common deanon vectors.

## Network

- **Always Tor or a research-only VPN, never your home/office IP.** Even for "just checking the leak site" — the moment you do it once unproxied, your IP is in the access logs forever.
- **Defence in depth: VPN → Tor.** Hides Tor entry from your ISP and (some) traffic-correlation attacks from passive observers. Choose a no-logs VPN paid in crypto on a separate identity if your threat model warrants.
- **Disable WebRTC** in any browser (Tor Browser does this by default). WebRTC leaks your real IP even through Tor.
- **No torrents, no streaming** from the research VM — many Tor exit nodes log abuse, and these protocols leak.

## Behavioural OPSEC

- **Timezone:** post / lurk on the *target's* operational hours, not yours. A "Russian-speaking" sockpuppet who is suspiciously active at US Eastern business hours is obviously a Western analyst.
- **Calendar:** Western public holidays (Thanksgiving, July 4th) cause inactivity in Western-run sockpuppets — schedule cover posts. Russian holidays (May 9, Jan 1-7) similarly affect Russian-speaking personae.
- **Cadence:** humans don't post in machine-regular intervals. Build natural breaks.
- **Sleep schedule:** a sockpuppet that "sleeps" 11pm–7am US Eastern leaks the analyst's geography. Either rotate handlers across timezones or don't post in real-time.

## Linguistic OPSEC

- **Machine-translation tells** are obvious to native speakers: stilted idioms, perfect grammar, overuse of a single dictionary synonym. Russian elite forums in particular have admins who flag suspected non-natives within hours.
- **Use a native-speaker collaborator** for anything beyond lurking in non-English forums. Better: hire a vetted CTI vendor who already has native-speaker analysts.
- **Slang and references:** persona-appropriate. A 19-year-old "scammer" persona doesn't drop 1990s movie quotes; a long-tenured "veteran" persona doesn't use 2024 Gen-Z slang.
- **Stylometry:** automated stylometry (writing-style fingerprinting) is a documented research field. Vary punctuation, spelling tics, sentence-length distribution, function-word frequency. The simplest defence: have your sockpuppet text edited by a different author than the analyst running it.

## Image and file OPSEC

- **Strip EXIF** from every screenshot or image before sharing. `exiftool -all= file.png` is the safe default.
- **Never post any image that exists elsewhere on the internet.** Reverse-image search (Google Lens, Yandex, TinEye) will surface the original within seconds, deanon the persona, and tell the forum admins exactly when the persona was created.
- **Profile photos:** generated faces (`thispersondoesnotexist.com`) used to be safe but are now detectable; better to use no profile photo, or a heavily edited generic icon.
- **Filenames** can leak (default Windows screenshot timestamps, default Apple "IMG_4521.HEIC", etc.). Rename before sharing.
- **PDF metadata** leaks author name + originating tool; "print to PDF" from a clean Tor Browser session is safer than uploading a Word-converted PDF.

## Counter-surveillance

- **Assume forum admins log everything.** Many forum admins are intelligence-services-adjacent; some are confirmed cooperators with state services after takedowns.
- **Assume Telegram channels can be compromised** by law enforcement or rival groups — operators have been doxed via channel ownership records leaked by ex-affiliates.
- **Assume vendors get popped.** Even commercial CTI vendors get breached or have insiders. Don't put your most sensitive selectors in vendor portals; keep them local.
- **Assume your ISP / employer / national authority logs** every site you touch. Tor + VPN are the answer; "I'll just look briefly without Tor" is not.

## Deconfliction

- **Notify your CISO + legal** before paying for invitations, interacting with sellers, attempting any active collection that could cross into "buying stolen data" or "interacting with criminals."
- **Notify the relevant national CERT / law enforcement liaison** if you find active intrusion data on your own org or a customer. Don't sit on it for a content scoop.
- **Coordinate with sector ISAC** if you find sector-wide impact (FS-ISAC, H-ISAC, etc.).
- **Never confront a threat actor directly** — even via a sockpuppet. It collapses the persona and risks retaliation.

## Persona burn handling

- **If a persona is flagged or burned** (admin call-out, sudden ban, leaked DM, suspected stylometric match): retire it. Do not try to "rehabilitate" by changing tactics. Wind down the persona's account, do not delete (deletion is itself a signal); let it go quiet.
- **Replace with a fresh persona** built from the ground up — new email, phone, browser profile, narrative, *no* overlap with the burned one.
- **Post-burn review:** what tipped them off? Stylometry? Timing? An image hit on reverse-image search? Document the lesson for the next persona.

## Mental health (load-bearing)

Sustained exposure to dark-web content — even purely cybercrime-focused, no CSAM — is documented to cause vicarious trauma in analysts. The job entails reading ransom-victim coercion, breach-victim PII, occasional accidental exposure to graphic content, and constant cynicism about the human condition.

- **Rotate analysts off dark-web duty** every 6-12 months. Long-term continuous exposure is the highest-risk pattern.
- **Provide clinical support** access. Several large CTI firms include EAP / wellness budget specifically for SOC + intel analysts.
- **Mandatory time off** after exposure to incidentally-encountered illegal-content material. Do not let a "just push through" culture take hold.
- **Buddy system:** debrief sessions weekly with a peer or supervisor. Catch creeping desensitisation early.
- **Resources:** Bellingcat have published OSINT analyst wellbeing guidance; Tech Coalition and Project VIC have CSAM-exposure-specific clinical resources for incident handlers (US-centric but applicable framework).

## Out of scope (refer elsewhere)

This skill, this OPSEC primer, and the bundled scripts do not cover:
- **CSAM (child sexual abuse material).** Discovery is mandatory-reportable in most jurisdictions. Stop reading, do not screenshot, log only the URL/identifier, and report to NCMEC (US), IWF (UK), Project Arachnid (Canada), or national equivalent. Do not investigate further; that work belongs to law enforcement and trained NGO units.
- **Active terrorism content / violent-extremist material.** Refer to national counter-terrorism units (NCTV, FBI JTTF, etc.) and to specialist platforms (GIFCT, Tech Against Terrorism).
- **Live-stream violent content.** Same as terrorism — refer to law enforcement immediately.
- **Personal-physical-safety threats** against named individuals. Refer to law enforcement and (if your org) physical security.

## A note on this skill's scripts

- `scripts/onion_search.py` queries clearnet indexers; running it from your normal IP exposes your *query string* to those indexers, which is itself a signal. Run via VPN/Tor for sensitive queries (target names, specific actor aliases).
- `scripts/telegram_monitor.py` uses your Telegram session — that account is identifiable to Telegram via the registered phone number. Treat it as a sockpuppet.
- `scripts/keyword_match.py` is local-only; no external network. Safe to run from any host.

## See also

- `access-methods.md` — vendor matrix and DIY playbook.
- `telegram-setup.md` — step-by-step setup for `telegram_monitor.py` (api_id, burner phone, session file, OPSEC ack flag).
- `passive-monitoring.md` — selector hygiene; bad selectors are an OPSEC risk too (broad selector → broad collection → broad exposure).
- `/score-source` — source rating; assume your collection sources may be compromised and rate accordingly.
- `/apply-tlp` — handle classification before sharing any collected material.
