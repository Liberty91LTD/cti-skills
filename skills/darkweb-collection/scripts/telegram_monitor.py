#!/usr/bin/env python3
"""
telegram_monitor.py — read-only Telegram channel monitor (Telethon).

================================================================================
READ THIS BEFORE FIRST USE.
================================================================================
This script connects to Telegram with your USER credentials. The Telegram
account you authenticate is identifiable to Telegram (registered phone) and
to every channel admin who looks at the subscriber list. It is NOT anonymous.

Running this against criminal channels (RaaS comms, IAB storefronts,
infostealer log shops, hacktivist ops) from your personal account or daily
host will burn the persona before it ever existed and may attract attention
from channel operators. See `references/opsec.md` for the full primer.

For first-time setup (getting an api_id/api_hash, picking a burner number,
isolating the session file), follow `references/telegram-setup.md` step by
step. Do NOT skip the burner-number step.

Live operations require the explicit `--i-understand-opsec` flag. Without
it, only `--dry-run`, `--self-test`, and `--help` work. Treat the flag like
a seatbelt: clicking it is acknowledgement, not protection.
================================================================================

Pulls historical messages or watches new ones across a list of channels
your Telegram account is *already a member of*. Matches each message
against a selector list and emits one JSONL record per hit.

Strictly read-only:
  - never sends messages
  - never auto-joins channels
  - never replies, reacts, or forwards
You must have manually joined every target channel from your Telegram
client first. The script will skip (and warn on) any handle the session
is not a member of.

Dependency: telethon (`pip install telethon`). Stdlib alone cannot speak
the MTProto protocol. Telethon is the most-vetted Python option.

Auth: this is a USER-API client, not a Bot API client. Required env:
  TELEGRAM_API_ID       int   from https://my.telegram.org/apps
  TELEGRAM_API_HASH     str   from same
  TELEGRAM_SESSION      path  to a .session file (created on first run)
  TELEGRAM_PHONE        str   E.164 phone for the account (only needed
                              for the very first interactive login)

How to obtain TELEGRAM_API_ID + TELEGRAM_API_HASH (the short version):
  1. Sign in at https://my.telegram.org with your (burner!) Telegram phone.
  2. Open "API development tools".
  3. Fill in App title (e.g. "research-monitor") and Short name (e.g.
     "rmon"). Platform: Desktop. URL/description can be left blank.
  4. Click "Create application". The page shows your api_id (integer) and
     api_hash (32-char hex). Save them once — re-displaying them is awkward.
  5. One application per account. If you fat-finger it, you cannot delete;
     create a new account or live with the name.
  Full step-by-step with safety notes: `references/telegram-setup.md`.

Usage:
  # Offline self-test (no Telegram, no network, no credentials needed):
  telegram_monitor.py --self-test

  # Validate config without connecting:
  telegram_monitor.py --dry-run --channels-file channels.txt \\
                      --selectors-file selectors.txt

  # Pull last N historical messages (live):
  telegram_monitor.py --i-understand-opsec --once --history 200 \\
                      --channels @vxunderground \\
                      --selectors-file selectors.txt

  # Stream new messages forever (live):
  telegram_monitor.py --i-understand-opsec --watch \\
                      --channels-file channels.txt \\
                      --selectors-file selectors.txt --out hits.jsonl

Selector file format: same as keyword_match.py (literal:/regex:/domain:/email:
prefixes; '#' comments and blank lines ignored).

Exit codes:
  0  success
  1  runtime / Telethon error
  2  missing TELEGRAM_API_ID/HASH/SESSION (only when not --dry-run/--self-test)
  3  bad arguments
  4  telethon not installed (only when not --dry-run/--self-test)
  5  --i-understand-opsec not supplied for a live operation
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

API_ID = os.environ.get("TELEGRAM_API_ID", "")
API_HASH = os.environ.get("TELEGRAM_API_HASH", "")
SESSION = os.environ.get("TELEGRAM_SESSION", "")
PHONE = os.environ.get("TELEGRAM_PHONE", "")

PREFIXES = ("literal:", "regex:", "domain:", "email:")


def die(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def load_selectors(path):
    selectors = []
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            line = raw.rstrip("\n").strip()
            if not line or line.startswith("#"):
                continue
            kind = "literal"
            value = line
            for p in PREFIXES:
                if line.startswith(p):
                    kind = p[:-1]
                    value = line[len(p):]
                    break
            try:
                if kind == "literal":
                    pattern = re.compile(re.escape(value), re.IGNORECASE)
                elif kind == "regex":
                    pattern = re.compile(value, re.IGNORECASE)
                elif kind == "domain":
                    pattern = re.compile(rf"(?<![\w.-]){value}(?![\w.-])", re.IGNORECASE)
                elif kind == "email":
                    pattern = re.compile(rf"[\w.+-]+{value}", re.IGNORECASE)
            except re.error as e:
                die(f"bad selector on line: {line!r}: {e}", 3)
            selectors.append({"raw": line, "kind": kind, "pattern": pattern})
    return selectors


def load_channels(args):
    channels = []
    if args.channels:
        channels.extend([c.strip() for c in args.channels.split(",") if c.strip()])
    if args.channels_file:
        with open(args.channels_file, "r", encoding="utf-8", errors="replace") as fh:
            for raw in fh:
                line = raw.rstrip("\n").strip()
                if not line or line.startswith("#"):
                    continue
                channels.append(line)
    # Normalize: strip leading t.me/, ensure leading '@'
    out = []
    seen = set()
    for c in channels:
        c = c.strip()
        for prefix in ("https://t.me/", "http://t.me/", "t.me/"):
            if c.lower().startswith(prefix):
                c = c[len(prefix):]
                break
        if not c.startswith("@"):
            c = "@" + c
        if c.lower() in seen:
            continue
        seen.add(c.lower())
        out.append(c)
    return out


def emit_match(out_fh, channel, msg, sel, match_text, before, after):
    rec = {
        "source": "telegram_monitor",
        "captured_at": now_iso(),
        "channel": channel,
        "message_id": getattr(msg, "id", None),
        "message_date": getattr(msg, "date", None).isoformat() if getattr(msg, "date", None) else None,
        "selector": sel["raw"],
        "selector_kind": sel["kind"],
        "match": match_text,
        "context_before": before,
        "context_after": after,
        "message_text": (getattr(msg, "message", "") or "")[:2000],
    }
    line = json.dumps(rec, ensure_ascii=False)
    print(line)
    if out_fh:
        out_fh.write(line + "\n")
        out_fh.flush()


def scan_text(text, selectors, radius):
    for sel in selectors:
        for m in sel["pattern"].finditer(text):
            start, end = m.span()
            yield sel, m.group(0), text[max(0, start - radius):start], text[end:end + radius]


def cmd_dry_run(args, selectors, channels):
    print(json.dumps({
        "dry_run": True,
        "mode": "watch" if args.watch else ("once" if args.once else "unspecified"),
        "channels_loaded": len(channels),
        "channels_preview": channels[:5],
        "selectors_loaded": len(selectors),
        "selector_kinds": sorted({s["kind"] for s in selectors}),
        "history_per_channel": args.history if args.once else None,
        "context_radius": args.context,
        "opsec_ack": bool(args.i_understand_opsec),
        "env": {
            "TELEGRAM_API_ID": "<set>" if API_ID else "<unset>",
            "TELEGRAM_API_HASH": "<set>" if API_HASH else "<unset>",
            "TELEGRAM_SESSION": SESSION or "<unset>",
            "TELEGRAM_PHONE": "<set>" if PHONE else "<unset>",
        },
        "out_file": args.out,
    }, indent=2))


OPSEC_REFUSAL_BANNER = """\
================================================================================
REFUSING to connect to Telegram without --i-understand-opsec.

This script connects with USER credentials (your Telegram account, registered
to your phone). Joining a channel — and even just *resolving* its handle
under your session — is visible to channel admins and to Telegram itself.

Before you supply --i-understand-opsec, confirm ALL of the following:
  [ ] You read references/opsec.md and references/telegram-setup.md.
  [ ] The Telegram account is a BURNER, registered to a number that is not
      tied to your real identity (MySudo / JMP / pre-paid SIM).
  [ ] You are running this from a research-only VM or dedicated host —
      NOT your daily-driver machine.
  [ ] Network egress is via a research-only VPN or Tor; NOT your home /
      office IP.
  [ ] You have already manually joined every target channel from the
      Telegram client on the burner account. The script will NOT auto-join.
  [ ] You have read the channel list and accepted that monitoring criminal
      channels (RaaS comms, IAB storefronts, infostealer log shops,
      hacktivist ops) will burn the persona over time.

For a first-run sanity check, point at defender-run safe channels only:
  @vxunderground   @FalconFeedsio   @cyberknow_   (see references/telegram-channels.md § 6)

For an OFFLINE smoke-test (no Telegram, no network, no credentials):
  python3 telegram_monitor.py --self-test
================================================================================
"""


PRE_CONNECT_BANNER_TEMPLATE = """\
--------------------------------------------------------------------------------
ABOUT TO CONNECT TO TELEGRAM with USER credentials.

  account session : {session}
  channels        : {channel_count}  ({first_few}{more})
  mode            : {mode}
  output          : {output}

Your Telegram identity will be visible to those channels' admins. If any of
the channels above is criminal-affiliated and you are NOT on a burner +
research-VM + Tor/VPN stack, abort now (Ctrl+C in the next 5 seconds).

Read references/opsec.md if you have not already.
--------------------------------------------------------------------------------
"""


def emit_pre_connect_banner(args, channels, mode):
    first_few = ", ".join(channels[:3])
    more = "" if len(channels) <= 3 else f" + {len(channels) - 3} more"
    banner = PRE_CONNECT_BANNER_TEMPLATE.format(
        session=SESSION,
        channel_count=len(channels),
        first_few=first_few,
        more=more,
        mode=mode,
        output=args.out or "stdout",
    )
    print(banner, file=sys.stderr)
    if sys.stderr.isatty():
        import time as _t
        for n in range(5, 0, -1):
            print(f"  connecting in {n}s … (Ctrl+C to abort)", file=sys.stderr)
            _t.sleep(1)


SELF_TEST_FIXTURE = (
    "BREAKING: LockBit affiliate claims breach of Acme Corp.\n"
    "Database (12GB) for sale. Contact alice@acme.com for samples.\n"
    "CVE-2024-12345 used for initial access. Mirror: acme.com/leaked.\n"
    "(This is synthetic test data; no real victim.)"
)

SELF_TEST_SELECTORS_RAW = [
    "literal:LockBit",
    "domain:acme\\.com",
    "email:@acme\\.com",
    "regex:CVE-202[3-6]-\\d{4,5}",
]

SELF_TEST_EXPECTED = {
    "literal:LockBit": "LockBit",
    "domain:acme\\.com": "acme.com",
    "email:@acme\\.com": "alice@acme.com",
    "regex:CVE-202[3-6]-\\d{4,5}": "CVE-2024-12345",
}


def run_self_test():
    print("# telegram_monitor.py --self-test", file=sys.stderr)
    print("# offline; no network; no Telegram; no credentials needed.", file=sys.stderr)
    selectors = []
    for raw in SELF_TEST_SELECTORS_RAW:
        kind = "literal"
        value = raw
        for p in PREFIXES:
            if raw.startswith(p):
                kind = p[:-1]; value = raw[len(p):]; break
        if kind == "literal":
            pat = re.compile(re.escape(value), re.IGNORECASE)
        elif kind == "regex":
            pat = re.compile(value, re.IGNORECASE)
        elif kind == "domain":
            pat = re.compile(rf"(?<![\w.-]){value}(?![\w.-])", re.IGNORECASE)
        elif kind == "email":
            pat = re.compile(rf"[\w.+-]+{value}", re.IGNORECASE)
        selectors.append({"raw": raw, "kind": kind, "pattern": pat})

    seen = {}
    matches = list(scan_text(SELF_TEST_FIXTURE, selectors, 60))
    for sel, match_text, before, after in matches:
        seen.setdefault(sel["raw"], match_text)
        rec = {
            "source": "telegram_monitor.self_test",
            "checked_at": now_iso(),
            "channel": "@self_test_fixture",
            "message_id": 1,
            "selector": sel["raw"],
            "selector_kind": sel["kind"],
            "match": match_text,
            "context_before": before,
            "context_after": after,
            "message_text": SELF_TEST_FIXTURE,
        }
        print(json.dumps(rec, ensure_ascii=False))

    failures = []
    for raw, expected in SELF_TEST_EXPECTED.items():
        got = seen.get(raw)
        status = "PASS" if got == expected else "FAIL"
        if status == "FAIL":
            failures.append((raw, expected, got))
        print(f"  {status}  selector={raw!r}  expected={expected!r}  got={got!r}", file=sys.stderr)
    print(json.dumps({
        "source": "telegram_monitor",
        "operation": "self_test",
        "checked_at": now_iso(),
        "selectors": len(SELF_TEST_SELECTORS_RAW),
        "matches_emitted": len(matches),
        "result": "PASS" if not failures else "FAIL",
        "failures": failures,
    }, indent=2))
    sys.exit(0 if not failures else 1)


def main():
    ap = argparse.ArgumentParser(
        prog="telegram_monitor.py",
        description="Read-only Telegram channel monitor (Telethon)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("--channels", help="comma-separated handles (e.g. @a,@b)")
    ap.add_argument("--channels-file", help="path to file with one handle per line")
    ap.add_argument("--selectors-file", help="path to selector list (required for live + dry-run, ignored by --self-test)")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--once", action="store_true", help="pull last N historical messages and exit")
    mode.add_argument("--watch", action="store_true", help="event-driven; stream new messages forever")
    ap.add_argument("--history", type=int, default=200, help="messages to pull per channel in --once mode (default 200)")
    ap.add_argument("--context", type=int, default=120, help="chars of context before/after each match (default 120)")
    ap.add_argument("--out", help="append matches to this JSONL file (in addition to stdout)")
    ap.add_argument("--dry-run", action="store_true", help="validate config without connecting to Telegram")
    ap.add_argument("--self-test", action="store_true",
                    help="run an offline parser+matcher self-test (no Telegram, no network, no credentials)")
    ap.add_argument("--i-understand-opsec", action="store_true",
                    help="REQUIRED for --once / --watch. Acknowledges you read references/opsec.md "
                         "and references/telegram-setup.md and are running on a burner account from a "
                         "research-only host behind Tor/VPN. The flag is not protection — it is acknowledgement.")
    ap.add_argument("--skip-pre-connect-banner", action="store_true",
                    help="suppress the 5-second pre-connect banner (use only for unattended supervisord runs)")
    args = ap.parse_args()

    if args.self_test:
        run_self_test(); return

    if not args.selectors_file:
        die("--selectors-file is required (except for --self-test)", 3)
    if not (args.channels or args.channels_file):
        die("must supply --channels or --channels-file", 3)

    selectors = load_selectors(args.selectors_file)
    if not selectors:
        die("no selectors loaded", 3)
    channels = load_channels(args)
    if not channels:
        die("no channels loaded", 3)

    if args.dry_run:
        cmd_dry_run(args, selectors, channels); return

    if not (args.once or args.watch):
        die("must supply --once, --watch, --dry-run, or --self-test", 3)

    if not args.i_understand_opsec:
        print(OPSEC_REFUSAL_BANNER, file=sys.stderr)
        sys.exit(5)

    if not (API_ID and API_HASH and SESSION):
        die("TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_SESSION must all be set", 2)

    try:
        from telethon import TelegramClient, events  # type: ignore
        from telethon.errors import ChannelPrivateError, UsernameNotOccupiedError  # type: ignore
    except ImportError:
        die("telethon not installed. Run: pip install telethon", 4)

    try:
        api_id = int(API_ID)
    except ValueError:
        die("TELEGRAM_API_ID must be an integer", 2)

    out_fh = open(args.out, "a", encoding="utf-8") if args.out else None
    client = TelegramClient(SESSION, api_id, API_HASH)

    if not args.skip_pre_connect_banner:
        emit_pre_connect_banner(args, channels, "watch" if args.watch else "once")

    async def resolve_channels():
        resolved = []
        for handle in channels:
            try:
                ent = await client.get_entity(handle)
                resolved.append((handle, ent))
            except (ChannelPrivateError, UsernameNotOccupiedError, ValueError) as e:
                print(f"warn: cannot resolve {handle}: {e}", file=sys.stderr)
        return resolved

    async def run_once():
        await client.start(phone=lambda: PHONE or input("phone (E.164): "))
        resolved = await resolve_channels()
        for handle, ent in resolved:
            count = 0
            async for msg in client.iter_messages(ent, limit=args.history):
                text = (msg.message or "") if hasattr(msg, "message") else ""
                if not text:
                    continue
                for sel, match_text, before, after in scan_text(text, selectors, args.context):
                    emit_match(out_fh, handle, msg, sel, match_text, before, after)
                    count += 1
            print(f"info: {handle} scanned ({count} matches)", file=sys.stderr)

    async def run_watch():
        await client.start(phone=lambda: PHONE or input("phone (E.164): "))
        resolved = await resolve_channels()
        entities = [ent for _, ent in resolved]
        handle_by_id = {ent.id: handle for handle, ent in resolved}
        if not entities:
            die("no channels resolved; nothing to watch", 1)

        @client.on(events.NewMessage(chats=entities))
        async def _handler(event):
            text = (event.message.message or "") if hasattr(event.message, "message") else ""
            if not text:
                return
            handle = handle_by_id.get(getattr(event.chat, "id", None), str(getattr(event.chat, "id", "?")))
            for sel, match_text, before, after in scan_text(text, selectors, args.context):
                emit_match(out_fh, handle, event.message, sel, match_text, before, after)

        print(f"info: watching {len(entities)} channels (Ctrl+C to stop)", file=sys.stderr)
        await client.run_until_disconnected()

    try:
        if args.once:
            client.loop.run_until_complete(run_once())
        else:
            client.loop.run_until_complete(run_watch())
    finally:
        if out_fh:
            out_fh.close()
        try:
            client.disconnect()
        except Exception:
            pass


if __name__ == "__main__":
    main()
