# Access methods for dark-web collection

> Verified through: 2026-04. Vendor offerings shift quarterly — confirm pricing and coverage with the vendor before commitment.

This skill recommends a **vendor-first** posture: the heavy lifting of forum vetting, sockpuppet maintenance, language coverage, and legal cover is done better — and more cheaply at scale — by specialised CTI vendors than by a defender team running its own DIY operation. Self-hosted Tor + sockpuppets + Telethon is documented as a fallback for budget-constrained teams or for narrow targeted collection that vendors will not service.

The `darkweb-collection` skill itself never visits a `.onion` address. The bundled `scripts/onion_search.py` resolves current onion mirrors against clearnet indexers; `scripts/telegram_monitor.py` reads channels your account already joined; `scripts/keyword_match.py` scans the resulting text. Everything else (Tor Browser, Tails, sockpuppet maintenance) is the analyst's responsibility, performed off the host running Claude Code.

## Half 1 — Vendor matrix (recommended)

| Vendor | Coverage strengths | Pricing tier (qualitative) | API? | Free / freemium tier? |
|---|---|---|---|---|
| **KELA** | Russian-speaking forums (Exploit, XSS, RAMP), IAB markets, infostealer log marketplaces. Strong actor profiling. | Enterprise | Yes | No (sales-led demo) |
| **Flashpoint** | Broad forum coverage, fraud/carding, jihadist + state-aligned chatter (separate product lines), illicit communities investigations. | Enterprise | Yes | No |
| **Intel471** | Cybercrime underground HUMINT, malware-as-a-service tracking, IAB monitoring, vetted source network. | Enterprise | Yes | No |
| **DarkOwl Vision** | Largest commercial darknet content index; strong for keyword/selector hunts across mirrored forums + leak sites. | Enterprise (mid) | Yes | Limited eval |
| **Recorded Future** | Aggregator over many sources incl. dark web, paste sites, Telegram, social. Strong analyst workflow + risk lists. | Enterprise | Yes | No |
| **Cybersixgill (Searchlight)** | Real-time deep/dark-web feed with strong vetting, IM coverage incl. Telegram + Discord. | Enterprise | Yes | No |
| **Webz.io (Lunar / Dark Web API)** | Data-as-a-service feed of forum + market scrapes; appealing if you want to build your own analytics on top. | Mid | Yes | Trial credits |
| **SOCRadar** | Affordable broad-spectrum DRP + dark-web monitoring; popular with mid-market security teams. | Mid | Yes | Free tier (limited) |
| **ZeroFox** | Brand + executive protection bias; pulls dark-web alongside surface social. | Enterprise | Yes | No |
| **Constella Intelligence** | Identity-centric — credentials, exposed PII, executive monitoring; very good at infostealer log linkage. | Enterprise | Yes | Limited eval |
| **Hudson Rock** | Infostealer-specialist (Cavalier, Bayonet). Free tier (Cavalier Infostealers) is genuinely useful. | Mid | Yes | **Yes — Cavalier free tier** |
| **IntelligenceX** | Searchable index of leaked data + onion content; feeds the `intelx` backend in `onion_search.py`. | Mid | Yes | **Yes — ~50 queries/day free** |
| **Have I Been Pwned (HIBP)** | Breach corpus only, but the canonical free check for credential exposure. | Free / paid API | Yes | **Yes** |
| **ransomware.live** | Ransomware leak-site claims, group profiles, IOCs, YARA. Already integrated in this pack via `/lookup-ransomwarelive`. | Free + PRO | Yes | **Yes — 3000 calls/day on PRO (free signup)** |

### Choosing a vendor

- **If your primary need is ransomware victim monitoring**: start with the bundled `/lookup-ransomwarelive` (free PRO tier) before paying for anything else. Add KELA, Intel471, or DarkOwl when you need to pivot from a victim claim into the actor's forum activity.
- **If you need infostealer log tracking** (executive PII, corporate credentials in stealer dumps): Hudson Rock free tier first, then KELA or Constella for depth.
- **If you need broad keyword hunts across many forums + paste sites**: DarkOwl or Webz.io; choose Webz.io if you want raw data for your own pipeline, DarkOwl if you want a finished search UI.
- **If you need Telegram-heavy coverage**: Cybersixgill, Flashpoint, or Recorded Future.
- **If you have zero budget**: combine `/lookup-ransomwarelive`, Hudson Rock free tier, IntelligenceX free tier, HIBP, and the DIY playbook below.

### What vendors will *not* service

- Highly targeted active engagement (sock-puppet posts, vouch acquisition, undercover purchases). Most vendors collect; few interact. For interactive collection you need either an HUMINT-capable boutique, a law-enforcement partnership, or DIY.
- Real-time invitation-only forums where the vendor lacks an existing sock-puppet. Onboarding a new persona to a vetted forum takes months.
- Anything that crosses the legality line in your jurisdiction (purchasing access, paying for data). Vendors document collection passively; they do not buy data on your behalf.

## Half 2 — DIY playbook (fallback)

> Read `opsec.md` before doing any of this. The list below is the *what*; OPSEC is the *how*.

### Hardware + OS

- **Dedicated host** for research. Never the daily driver. A second laptop is ideal; a hardened VM on a researcher-only host is acceptable. Full-disk encryption, snapshot rollback after each session.
- **Tails OS** (live USB, amnesic) for ad-hoc browsing where you do not need persistent state. Routes everything through Tor.
- **Whonix** (gateway VM + workstation VM in VirtualBox/KVM) for persistent research where you need to keep a sockpuppet's session, browser profile, or downloaded files between sessions.
- Never bridge research VM clipboard / file-share with the host.

### Network

- **Tor Browser** for `.onion` and clearnet research, default settings, sliders set to "safer" or "safest" (kills JS), no plugins, never log into real accounts.
- **Defence-in-depth option:** paid no-logs VPN → Tor (Tor over VPN). Hides Tor entry from your ISP; does NOT defeat traffic-correlation attacks. Pick a VPN paid for with crypto on a separate identity if your threat model warrants.
- **Never** connect from home/office IP without Tor or a research-only VPN.

### Onion discovery

- **Ahmia** (`ahmia.fi`) — free, no auth, indexed by content. Backend in `onion_search.py`.
- **dark.fail** — status board of canonical .onion mirrors with PGP-signed list. Verify signatures before trusting addresses for high-value targets (forum logins, market deposits). Backend in `onion_search.py`.
- **Tor.taxi** — similar status board; useful as cross-check.
- **Onion.live** and similar third-party indexers — be cautious; many have been hijacked or list phishing mirrors. Cross-check before trusting.
- **Vendor-curated lists** — KELA, DarkOwl, Cybersixgill internal mirrors are typically authoritative; if you have a vendor account, prefer their resolutions over public indexers.

### Forum vetting paths

1. **Open-tier forums** (BreachForums-lineage, Nulled, Cracked, Sinister.ly): register with a sockpuppet, lurk. Reading is enough for 90% of CTI use cases.
2. **Register-only Russian-speaking forums** (XSS, Exploit): registration may require basic vouching or a small entry fee. Sockpuppet must be linguistically credible (don't post English-language English in a Russian forum).
3. **Vouch-required tier** (RAMP, Verified): typically requires existing-member vouch. Established CTI vendors have these. Defenders without an existing in should not attempt — burning a fresh sockpuppet here is expensive and you will get flagged as outsider.
4. **Pay-to-vouch** schemes are typically scams; do not pay random strangers for vouches.
5. **Closed RaaS-affiliate channels** (group-internal Matrix/Tox/Element rooms, private Telegram supergroups): out of reach of DIY collection. Vendors with HUMINT relationships or law enforcement is the only path.

### Sockpuppet identity stack

- **Email**: Tutanota or ProtonMail registered over Tor. New accounts get rate-limited / flagged for 24-48 hours; warm them up with low-value mail before using for forum registration.
- **Phone (when required)**: pre-paid burner SIM, or a paid virtual number (MySudo, JMP.chat) — never a service that resells your real identity.
- **Persona narrative**: write it down before using it. Age, country, claimed skill, native language, fake birthday for forum profile, why-they-care-about-this-niche. Maintain it consistently across sessions.
- **Naming**: never reuse a handle across personae. Never reuse a handle from any pre-existing account, even private ones — handle reuse is a primary deanon vector.
- **Stylometry**: vary punctuation, capitalisation, slang. The `narrative` and the `style` should both be fictional and consistent.

### Telegram

- **Burner number** for Telegram registration (see above). Telegram will SMS a code; the number gets baked into the account permanently.
- **Telethon** (the user-API library powering `scripts/telegram_monitor.py`) lets a session-file account read every channel it has joined. It does not auto-join — joining is a deliberate event you do from the Telegram app.
- **Bot API is not enough** — bots cannot read messages from arbitrary public channels unless added as admins. The user-API is the standard for monitoring.
- **OPSEC for Telegram**: do not use the same burner number for multiple personae; do not use real identifying info in profile name, photo, or bio; treat the session file as credentials.

### Cryptocurrency

Out of scope for this skill in any operational sense. Many forums require Monero (XMR) or Bitcoin (BTC) for invitations, market access, or data purchases. **Defenders should not buy data or pay for access without explicit legal sign-off and (often) law-enforcement coordination** — it can constitute receiving stolen property, funding criminal enterprises, or breaching sanctions. If you have a legitimate need, route the decision through your CISO + counsel + the relevant national CERT before any transaction.

### Logging the collection

Every research session must produce auditable evidence. Minimum stack:
- Timestamped notes (markdown is fine; one file per session, ISO-date filename).
- Full-page screenshots of every page consumed (strip EXIF before sharing). The Tor Browser screenshot extension is unreliable; use the host VM's tool and screenshot the entire VM window.
- For deep collection: HTTP capture via `mitmproxy` running on the Whonix gateway. Captures every request/response under your sockpuppet for later replay/audit.
- Session-end checklist: clear cookies (or revert VM snapshot), zero clipboard, log session metadata (channels visited, sockpuppet used, anything noteworthy seen), commit notes to encrypted store.

### Storage and retention

- Append-only JSONL files (the format the bundled scripts emit) for machine-readable collection.
- One directory per source, one file per day (`telegram/2026-04-28.jsonl`, `forums/xss/2026-04-28.jsonl`, etc.).
- Encrypted at rest. Even "public" forum data may include PII subject to retention rules in your jurisdiction.
- Agree retention period with counsel — typical defender practice is 90-365 days for raw collection, longer for finished intelligence products.

## When DIY is appropriate

- Single, narrow, time-bounded targeted collection (one breach, one actor, one channel) where vendor onboarding cost would exceed the analyst-hours.
- Education / training (purpose-built sockpuppet operating against open-tier forums for skill development).
- Verifying / replicating a vendor finding before reporting it.

## When DIY is *not* appropriate

- Bulk monitoring across dozens of forums (vendors do this 10× more cheaply per source-month).
- Anything requiring vouching into a closed Russian-speaking forum.
- Anything that touches CSAM-adjacent or terrorism-adjacent material — refer to law enforcement.
- Anything that requires purchases / financial transactions with criminals.

## See also

- `opsec.md` — handler-side OPSEC primer (read this first).
- `passive-monitoring.md` — selector strategy and tooling for both vendor APIs and DIY.
- `forums.md`, `telegram-channels.md` — what you would actually be monitoring.
- `/lookup-ransomwarelive`, `/lookup-misp` — bundled lookups that complement DIY collection.
