# Telegram setup for `telegram_monitor.py`

> Read [`opsec.md`](opsec.md) first. The setup steps below produce credentials that are equivalent to your Telegram identity. Treat them like passwords; better yet, like passwords for an alias you keep at arm's length from your real life.

This page walks you through everything you need before `scripts/telegram_monitor.py` will let you connect: a burner account, an `api_id` + `api_hash`, a session file, and the OPSEC posture the script will demand at runtime.

## Decision: are you going live, or just testing?

**Just testing the script logic?** You don't need any of this. Run:

```bash
python3 scripts/telegram_monitor.py --self-test
```

The self-test exercises the parser and matcher against a built-in synthetic fixture. No Telegram, no network, no credentials. PASS/FAIL output to stderr, JSONL hits to stdout. Use this in CI or as a sanity check after editing the script.

**Going live?** Continue reading.

## Step 0 — OPSEC posture (do this before Step 1)

You need three things in place before you create any account:

1. **A research-only host.** A second laptop is best; otherwise a hardened VM (Whonix workstation, encrypted-disk Ubuntu in VirtualBox/UTM, Tails persistent volume). Not your daily driver. Not the host that runs your real-name browser, your work email, or your password manager.
2. **A research-only network egress.** Either Tor (via Whonix gateway, Tails, or torsocks) or a paid no-logs VPN bought on a separate identity. Not your home or office IP.
3. **A burner phone number.** Telegram requires SMS verification on signup, and the number is permanently associated with the account.
   - **Cheapest reliable**: pre-paid SIM bought in cash at a corner shop in any country that does not require ID for prepaid (jurisdiction varies — check before you buy). Use it for SMS, then remove from the phone.
   - **Easiest for international researchers**: MySudo, JMP.chat, or a paid VOIP-with-SMS service. Both have ongoing fees but you can keep the number.
   - **Avoid**: free online "receive SMS" services. Their numbers are routinely re-issued and have already been used for thousands of accounts; many forums and Telegram itself flag them.

Do not skip this step. The number you register with is permanent and is visible to Telegram (and via metadata leaks to certain channel admins).

## Step 1 — Install Telegram on the burner host

Use the desktop client (`telegram-desktop` on Linux/macOS/Windows, or the official .deb/.rpm for Linux). Do **not** install on your phone alongside your personal Telegram — they will share state in subtle ways.

Sign in:
1. Launch Telegram Desktop.
2. Enter the burner phone number in E.164 format (e.g. `+447700900000`).
3. Wait for the SMS, enter the code.
4. (If 2FA is enabled on the account it will prompt for a password — you set that later, not now.)

You're now signed in. Don't set a profile photo or a display name; "Edit profile" → leave the first name as something inconspicuous (a common first name in the locale of the phone number works), no last name, no bio.

## Step 2 — Get an `api_id` and `api_hash`

1. Open https://my.telegram.org in a browser (the same burner host).
2. Sign in with the burner phone number. Telegram will send a confirmation code via the Telegram client (not SMS) — fetch it from the desktop app.
3. Click **API development tools** (https://my.telegram.org/auth?to=apps).
4. Fill in the form:
   - **App title**: any unremarkable string. `research-monitor`, `feed-reader`, `personal-rss`. Avoid anything that hints at CTI or "monitoring criminal X".
   - **Short name**: same energy. `rmon`, `feedrd`. 5-32 chars, alphanumeric only.
   - **URL**: leave blank.
   - **Platform**: pick **Desktop** (or **Other**, both fine).
   - **Description**: leave blank or write one neutral sentence.
5. Click **Create application**. The page will display:
   - **App api_id**: an integer, around 7 digits.
   - **App api_hash**: a 32-character hexadecimal string.
6. **Copy both immediately into your password manager / encrypted notes.** Re-displaying the `api_hash` later requires re-loading the page and is occasionally awkward. Treat them like a credential pair.

Important rules from Telegram's side:
- **One application per Telegram account.** You cannot delete or re-create. If you fat-finger the App title or the values displayed, you live with it (or burn the account and start over).
- **The `api_hash` must stay secret.** Anyone with both id and hash can build a client that authenticates as your account (subject to also having a valid session or being able to complete an SMS code).

## Step 3 — Set environment variables

Two ways: per-shell (transient) or via this pack's `.claude/settings.local.json` (gitignored, persistent across Claude Code sessions).

**Per-shell:**

```bash
export TELEGRAM_API_ID=1234567
export TELEGRAM_API_HASH=0123456789abcdef0123456789abcdef
export TELEGRAM_SESSION="$HOME/.cache/cti-skills/telegram.session"
export TELEGRAM_PHONE="+447700900000"   # only needed on first run
mkdir -p "$(dirname "$TELEGRAM_SESSION")" && chmod 700 "$(dirname "$TELEGRAM_SESSION")"
```

**Persistent in this repo (recommended):**

Run `/cti-setup`. It will prompt for the values and merge them into `.claude/settings.local.json` under the `env` block. That file is gitignored.

Alternatively, hand-edit `.claude/settings.local.json`:

```json
{
  "env": {
    "TELEGRAM_API_ID": "1234567",
    "TELEGRAM_API_HASH": "0123456789abcdef0123456789abcdef",
    "TELEGRAM_SESSION": "/Users/you/.cache/cti-skills/telegram.session",
    "TELEGRAM_PHONE": "+447700900000"
  }
}
```

Verify:

```bash
python3 scripts/telegram_monitor.py --dry-run \
  --channels @vxunderground \
  --selectors-file <(echo "literal:test")
```

The output's `env` block should show `<set>` for `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, `TELEGRAM_PHONE`, and the path for `TELEGRAM_SESSION`.

## Step 4 — Install Telethon (in a dedicated virtualenv)

**Use a dedicated venv.

```bash
# One-time setup. Lives outside the repo so it survives `git clean`.
mkdir -p ~/.cache/cti-skills && chmod 700 ~/.cache/cti-skills
python3 -m venv ~/.cache/cti-skills/venv
~/.cache/cti-skills/venv/bin/python3 -m pip install --upgrade pip
~/.cache/cti-skills/venv/bin/python3 -m pip install telethon
```

Verify:

```bash
~/.cache/cti-skills/venv/bin/python3 -c "import telethon; print('telethon', telethon.__version__)"
```

From this point onward, **always invoke the script via the venv's interpreter**:

```bash
~/.cache/cti-skills/venv/bin/python3 skills/darkweb-collection/scripts/telegram_monitor.py …
```

(Adding `~/.cache/cti-skills/venv/bin` to `PATH` is OK if the rest of your environment doesn't already have a conflicting `python3`. Activating the venv with `source ~/.cache/cti-skills/venv/bin/activate` is also fine, but is per-shell and easy to forget.)

Telethon is the canonical Python MTProto client; the script imports it lazily so `--dry-run` and `--self-test` work even with the system `python3` (no telethon required).

## Step 5 — First-time login (creates the session file)

The first time you run a live operation, Telethon will:
1. Read your `api_id` + `api_hash`.
2. Send a login code to your Telegram client (the desktop app you signed into in Step 1).
3. Prompt you for that code (interactively). If your account has 2FA enabled, prompt for the password too.
4. Write the session file to `$TELEGRAM_SESSION`.

After this, future runs are non-interactive — they read the session file and reconnect.

**Important**: do this first run while attended, on the burner host, and use a defender-safe channel like `@vxunderground` for the test. Example:

```bash
# In Telegram Desktop on the burner host: search "@vxunderground" → "Join Channel".
# Then:
python3 scripts/telegram_monitor.py \
  --i-understand-opsec --once --history 5 \
  --channels @vxunderground \
  --selectors-file <(echo "regex:.+")
```

The script will print a 5-second pre-connect banner (Ctrl+C aborts), prompt for the SMS code, write the session file, fetch the last 5 vx-underground messages, scan against the (catch-all) selector, and emit JSONL.

## Step 6 — Protect the session file

The session file is equivalent to your account credentials. With it, anyone can authenticate as your burner account from any machine.

- **Permissions**: `chmod 600 $TELEGRAM_SESSION`. Parent dir `chmod 700`.
- **Storage**: encrypted-at-rest disk only. macOS FileVault, Linux LUKS, Windows BitLocker, or a per-file gpg-encrypted wrapper.
- **Backups**: encrypt before backing up. Treat backups as an extra credential copy.
- **Never** check the session file into git. The repo `.gitignore` does not list it by name — keep it outside the repo entirely (the recommended path `~/.cache/cti-skills/telegram.session` is fine).
- **If lost / leaked**: revoke from inside Telegram (Settings → Devices → terminate session) and rotate. The api_id/api_hash itself does not need rotating unless you suspect those leaked too.

## Step 7 — Joining target channels (manually, in the desktop client)

The script never auto-joins. Joining is a deliberate, OPSEC-significant act:

1. Decide the channel from `references/telegram-channels.md`.
2. Reconfirm: is this a **defender-run safe** channel (§ 6) or a **criminal/affiliated** channel (§§ 1-5)?
   - Defender-run safe: low OPSEC penalty. Many CTI analysts publicly subscribe to vx-underground, FalconFeedsio, etc. Fine.
   - Criminal/affiliated: high OPSEC penalty. Channel admins can see your subscriber-list presence, can DM you, can flag your account. Only do this from a fully OPSEC'd burner that you accept may be burned.
3. In Telegram Desktop on the burner host, search the `@handle` and click **Join channel**.
4. Wait at least a few minutes before the script first reads from the channel (joining bursts that immediately produce automated reads are flagged as bot-like).

## Step 8 — Run live with the OPSEC acknowledgement

Live operations require `--i-understand-opsec`. Without it the script refuses and prints a checklist. Example invocation against safe channels:

```bash
python3 scripts/telegram_monitor.py \
  --i-understand-opsec --watch \
  --channels-file safe-channels.txt \
  --selectors-file selectors.txt \
  --out hits.jsonl
```

## Anti-checklist (don't do these)

- ❌ Reuse your personal Telegram account "just for the test."
- ❌ Use a free online "SMS receive" number.
- ❌ Run from your daily-driver host without VPN/Tor.
- ❌ Auto-join channels via API. The script won't do this for you; do not patch it to.
- ❌ Use the same burner account across multiple research personae. One account, one persona.
- ❌ Set a profile photo or distinctive display name on the burner.
- ❌ Run `--watch` on criminal channels from a host that isn't always-on Tor/VPN — IP rotations during reconnects are deanon vectors.
- ❌ Commit session files, env files with real api_hash, or `.cache` paths into git.
- ❌ Skip `--skip-pre-connect-banner` casually. It's intended only for unattended supervisord/systemd runs where you've already vetted the channel list.

## Using `telegram_monitor.py` from a Claude Code/Cursor etc session

Most of the workflow above is one-time setup you do yourself in a terminal. After that, day-to-day use can run inside a Claude Code session or any other tool you use for these skills — Claude executes the script via its Bash tool, reads the output, and helps you tune selectors. Here is what changes (and what doesn't) compared to a plain CLI.

### What Claude can do for you

- **Build the selectors file from a PIR.** Paste your intelligence requirement ("alert me on any mention of Acme or its subsidiaries, especially exec names or `@acme.com` emails, in ransomware-related contexts"). Ask Claude to write a `selectors.txt` file using the `literal:` / `regex:` / `domain:` / `email:` prefixes from `keyword_match.py`'s docstring.
- **Build the channels file.** Ask "give me a starter channels file with the safe defender-run channels from `references/telegram-channels.md` § 6" and Claude will produce a `channels.txt` you can review.
- **Run the offline self-test.** No credentials, no risk. Just say "run the telegram monitor self-test." Claude will execute `python3 scripts/telegram_monitor.py --self-test` and summarise the PASS/FAIL output.
- **Run a `--dry-run`.** Validates env vars are wired up, channels parse, selectors compile. Still no network. Say "dry-run the telegram monitor against my channels file."
- **Run a live `--once` against safe channels** — but only after you have completed the burner setup outside Claude (Steps 0-5 above). Claude can then invoke `python3 scripts/telegram_monitor.py --i-understand-opsec --once …` and pipe results into a triage queue or `keyword_match.py`. You will be prompted by Claude Code to approve the Bash invocation; that prompt is your last chance to abort.
- **Tune selectors based on hits.** Claude can read the JSONL output, identify false positives, propose tighter selectors, edit `selectors.txt`, and re-run. This is the loop where having Claude in the picture pays for itself.
- **Compose with other skills.** Pipe a hit through `/lookup-misp`, `/lookup-virustotal`, `/lookup-ransomwarelive`, `/score-source`, `/apply-tlp` to enrich and report.

### What Claude cannot do for you

- **The first-run interactive SMS login.** Telethon's first authentication on a fresh session file prompts for an SMS code on the terminal — Claude's Bash tool does not handle interactive prompts well. **Do the first `--once` run yourself in a terminal**, completing the SMS verification, so the session file is created. Subsequent runs (which read the session file) are non-interactive and Claude can run them.
- **Decide it is OK to monitor a high-risk channel.** The `--i-understand-opsec` flag is a per-invocation acknowledgement *from you*, not from Claude. If Claude proposes the flag, that is still a question for you — the Bash permission prompt is where you confirm. Don't bake `--i-understand-opsec` into a `.claude/settings.local.json` permission allowlist; let it surface every time.
- **Configure your burner phone, your Tor stack, or your research VM.** Those are physical/infrastructure choices outside the agent's reach.
- **Talk you out of a bad idea.** Claude will warn (the SKILL and this file are quite loud about it), but ultimately you press enter. Read the refusal banner each time.

### Setting env vars from a Claude session

Two convenient paths:

1. **`/cti-setup`.** Ask Claude to "run cti-setup so I can add my Telegram api_id and api_hash." It will walk you through the four variables (`TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, `TELEGRAM_SESSION`, `TELEGRAM_PHONE`) and merge them into `.claude/settings.local.json` (gitignored). After that, Claude inherits them whenever it spawns a subprocess.
2. **Hand-edit `.claude/settings.local.json`.** Open it in your IDE, add the four keys under the `env` block (see "Persistent in this repo" further up this page), save. Claude will pick them up on the next Bash invocation.

Verify Claude sees them:

> "Dry-run the telegram monitor with `--channels @vxunderground` and a one-line catch-all selector."

The `env` block in the dry-run output should show `<set>` for the three required vars.

### A worked example session

A realistic first session, in plain English you'd type to Claude:

1. "Build a `selectors.txt` for monitoring mentions of Acme Corp, including its `acme.com` and `acme-cloud.io` domains, executive surnames Smith and Jones, and any CVE from 2024-2026."
2. "Build a `channels.txt` with the three defender-run safe channels from § 6 of `references/telegram-channels.md`."
3. "Run the telegram monitor self-test."
4. "Dry-run the telegram monitor against `channels.txt` and `selectors.txt`."
5. (Now you go to a terminal yourself, run the live `--once` once to complete SMS auth, confirm the session file exists.)
6. Back in Claude: "Run the telegram monitor live, pulling the last 50 messages from each channel in `channels.txt`, matching against `selectors.txt`, and write hits to `hits.jsonl`."
7. "Read `hits.jsonl`, summarise the top three selectors by hit count, and propose any selectors that are too noisy."
8. (Iterate.)

If you want this running continuously, ask Claude to write you a launchd / systemd unit file with the right env vars, the `--watch` mode, `--i-understand-opsec`, and `--skip-pre-connect-banner` (only after you have vetted the channel list and accepted the OPSEC posture).

### Anti-pattern

> "Claude, monitor my org against ransomware channels and let me know if anything pops up."

This sounds like one sentence; it is actually six decisions with OPSEC consequences. Do not let the convenience of a chat interface paper over them. Walk through Steps 0-7 above first, decide which channels and which posture, and *then* delegate the operational running to Claude.

## Reference

- [`opsec.md`](opsec.md) — full OPSEC primer, including persona separation, mental health, and incident handling.
- [`access-methods.md`](access-methods.md) — vendor alternatives if all of the above feels (correctly) like a lot of work for one channel.
- [`telegram-channels.md`](telegram-channels.md) — the channel list, with safe defender-run channels in § 6.
- Telegram's official API docs: https://core.telegram.org/api
- Telethon docs: https://docs.telethon.dev/
