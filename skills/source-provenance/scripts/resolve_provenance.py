#!/usr/bin/env python3
"""
resolve_provenance.py — resolve an article's provenance chain to its originating source.

Deterministic. Standard library only. No model in the loop: the chain this script
returns is data, and every field it could not determine is null with a reason.

Usage:
  resolve_provenance.py resolve <url> [<url> ...] [--max-hops 1|2] [--no-cache]
                                [--cache-dir DIR] [--fixtures MAP.json] [--today YYYY-MM-DD]
  resolve_provenance.py classify <url> [<url> ...]
  resolve_provenance.py text <url> [--no-cache] [--cache-dir DIR] [--fixtures MAP.json]

  resolve   follow links and named attributions to the primary; emit JSON on stdout
  classify  look a URL up in references/source-types.md; no network
  text      fetch a page, extract the article body to the local cache, print the
            path to the text file (used by /claim-extraction; the text is never
            included in any JSON output)

Exit codes:
  0  every input resolved to a primary (provenance_basis: script-resolved)
  1  usage or internal error
  2  at least one input did not resolve to a primary
  3  refused: more than 50 URLs or more than 2 hops requested

Fetcher policy (fixed; there is no override flag for robots.txt):
  - User agent: cti-skills-provenance/2.0 (+https://github.com/Liberty91LTD/cti-skills)
  - robots.txt honoured. A blocked page is reported; paste the text to continue.
  - One request in flight per host, 2 seconds between requests to the same host,
    at most 4 hosts in flight.
  - 429/503: honour Retry-After, else exponential backoff from 10s; three attempts,
    then the host is skipped for the rest of the run.
  - Local cache keyed by URL, revalidated with ETag / Last-Modified.
    TTL 7 days for press, 30 days for primaries. Never uploaded, never committed.
  - Hard cap: 50 URLs and 2 hops per invocation.
  - Timeouts 10s connect, 20s read. 5 MB size limit. PDFs are not parsed here.
  - Output contains extracted fields and anchor sentences only. Full text stays
    in the local cache.
"""

import argparse
import datetime as dt
import hashlib
import html
import http.client
import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path

USER_AGENT = "cti-skills-provenance/2.0 (+https://github.com/Liberty91LTD/cti-skills)"
ROBOTS_AGENT = "cti-skills-provenance"
CONNECT_TIMEOUT = 10
READ_TIMEOUT = 20
MAX_BYTES = 5 * 1024 * 1024
HOST_SPACING = 2.0
MAX_HOSTS_IN_FLIGHT = 4
MAX_URLS = 50
MAX_HOPS = 2
BACKOFF_START = 10
MAX_ATTEMPTS = 3
TTL_PRESS = 7 * 86400
TTL_PRIMARY = 30 * 86400
TTL_ROBOTS = 86400
MAX_PRESS_FOLLOW = 3
MAX_PRIMARY_TRIES = 4
# A primary published long before the article is background, not the origin.
WINDOW_BEFORE_DAYS = 60
WINDOW_AFTER_DAYS = 3
# Outlets that link their source do so early. A candidate whose date cannot be checked
# is accepted as the primary only when it is linked within the first paragraphs.
EARLY_PARAGRAPHS = 4
# Access types a primary of each type can hold. A vendor report that discusses a leak
# site has not thereby obtained its information by actor statement.
ACCESS_BY_TYPE = {
    "vendor": {"telemetry", "ir_engagement", "sample_analysis", "osint"},
    "government": {"telemetry", "ir_engagement", "sample_analysis", "osint", "victim_statement"},
    "researcher": {"telemetry", "ir_engagement", "sample_analysis", "osint"},
    "victim": {"victim_statement"},
    "actor": {"actor_statement"},
}

SKILL_DIR = Path(__file__).resolve().parent.parent
SOURCE_TYPES = SKILL_DIR / "references" / "source-types.md"

PRIMARY_TYPES = {"vendor", "government", "victim", "actor", "researcher"}
INTERMEDIARY_TYPES = {"press", "aggregator", "social", "unknown"}

# --- pattern lists (documented in references/attribution-phrases.md) -----------------

ATTRIBUTION_PATTERNS = [
    r"\baccording to\b",
    r"\bresearchers (?:at|from|with)\b",
    r"\bin an? (?:new |recent |joint )?(?:report|blog post|advisory|analysis|write-up|technical write-up)\b",
    r"\b(?:said|wrote|noted|stated|explained|warned) in (?:a|an|its|their)\b",
    r"\bpublished by\b",
    r"\b(?:a|an|the) (?:joint )?advisory\b",
    r"\bdisclosed\b",
    r"\btold [A-Z]",
    r"\b(?:first )?(?:reported|spotted|discovered|uncovered|documented|detailed) by\b",
    r"\b(?:findings|data|telemetry) from\b",
    r"\bshared with\b",
    r"\b(?:8-K|SEC) filing\b|\bfiled with\b",
    r"\b(?:data )?leak site\b|\bposted on (?:its|their) [^.]{0,40}(?:site|blog|channel)\b",
]

UNATTRIBUTED_PATTERNS = [
    r"\bresearchers (?:say|said|have|warn)\b",
    r"\bsecurity experts\b|\bexperts (?:say|warn)\b",
    r"\bsources (?:say|said|familiar with)\b",
    r"\breports (?:suggest|indicate)\b|\bit is (?:believed|reported)\b",
]

CONFIDENCE_PATTERNS = [
    r"\bassess(?:es|ed|ment)?\b[^.]{0,40}\b(?:with )?(?:low|moderate|medium|high) confidence\b",
    r"\b(?:low|moderate|medium|high)[- ]confidence\b",
    r"\bwith (?:low|moderate|medium|high) confidence\b",
    r"\bconfidence (?:level|is)\b",
]

HEDGE_PATTERNS = [
    r"\blikely\b", r"\bunlikely\b", r"\bsuspected\b", r"\bpossibly\b", r"\bpotentially\b",
    r"\bprobably\b", r"\bmay have\b", r"\bmight\b", r"\bappears? to\b", r"\bwe believe\b",
    r"\bbelieved to\b", r"\bconsistent with\b", r"\boverlaps? with\b", r"\blinked to\b",
    r"\battributed\b", r"\bcannot confirm\b", r"\bcould not confirm\b", r"\bunconfirmed\b",
    r"\balleged(?:ly)?\b", r"\bclaim(?:s|ed)\b",
]

# Order matters: ties between access types resolve in this order.
ACCESS_PATTERNS = [
    ("telemetry", [
        r"\bour telemetry\b",
        r"\b(?:our|its|their) (?:own )?(?:sensors|telemetry|visibility|customer base|honeypots?)\b",
        r"\bwe (?:have )?observed\b", r"\bwe (?:have )?detected\b",
        r"\b(?:observed|detected|blocked) (?:by|in) (?:our|its)\b",
        r"\b(?:product|endpoint|network) telemetry\b",
    ]),
    ("ir_engagement", [
        r"\bincident response (?:engagement|investigation|case)s?\b",
        r"\bduring (?:an|a recent|our|the) (?:investigation|engagement|response)\b",
        r"\b(?:were|was) engaged (?:by|to)\b",
        r"\bresponded to (?:an|a|the) (?:incident|intrusion|breach)\b",
        r"\bforensic (?:analysis|investigation|examination)\b",
    ]),
    ("sample_analysis", [
        r"\bsamples? (?:was |were )?(?:submitted|uploaded|obtained|shared)\b",
        r"\buploaded to VirusTotal\b",
        r"\bwe (?:analy[sz]ed|reverse[- ]engineered)\b",
        r"\b(?:static|dynamic) analysis\b", r"\breverse engineering\b",
    ]),
    ("osint", [
        r"\bopen[- ]source (?:reporting|information|intelligence|research)\b",
        r"\bpublicly (?:available|reported)\b", r"\bpublic reporting\b",
        r"\bpreviously (?:reported|documented) by\b",
    ]),
    ("victim_statement", [
        r"\b(?:8-K|10-K|SEC) filing\b", r"\bnotification (?:letter|to affected)\b",
        r"\bwe (?:recently )?(?:discovered|identified|detected|became aware of) "
        r"(?:unauthorized|unauthorised|suspicious)\b",
        r"\bbreach notification\b",
    ]),
    ("actor_statement", [
        r"\bleak site\b", r"\bransom note\b",
        r"\bposted on (?:a|an|the) (?:forum|Telegram)\b", r"\bclaimed responsibility\b",
    ]),
]


def _compile(patterns):
    return [re.compile(p, re.IGNORECASE) for p in patterns]


RE_ATTRIBUTION = _compile(ATTRIBUTION_PATTERNS)
RE_UNATTRIBUTED = _compile(UNATTRIBUTED_PATTERNS)
RE_CONFIDENCE = _compile(CONFIDENCE_PATTERNS)
RE_HEDGE = _compile(HEDGE_PATTERNS)
RE_ACCESS = [(name, _compile(pats)) for name, pats in ACCESS_PATTERNS]
RE_SENTENCE = re.compile(r"(?<=[.!?])[\"”’)]*\s+(?=[\"“‘(]?[A-Z0-9])")
RE_ISO_DATE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
RE_URL_DATE = re.compile(r"/(20\d{2})/(\d{1,2})/(?:(\d{1,2})/)?")
RE_PROMO_QUERY = re.compile(r"(?:^|&)(?:utm_[a-z]+|ref|campaign|gclid|fbclid)=", re.IGNORECASE)
RE_PROMO_PATH = re.compile(
    r"^/(?:[a-z]{2}(?:-[a-z]{2})?/)?(?:enterprise|pricing|plans|demo|request-demo|get-demo|"
    r"contact|contact-us|contact-sales|signup|sign-up|register|login|trial|free-trial|"
    r"products?|platform|solutions|services|why-[\w-]+|about|about-us|careers|partners|"
    r"webinars?|events|subscribe|newsletter|download)(?:/|$)", re.IGNORECASE)


class Refused(Exception):
    pass


# --- source-types table --------------------------------------------------------------

class SourceTable:
    """Lookup table parsed from references/source-types.md. Longest prefix wins."""

    COLUMNS = ["domain", "organisation", "type", "access_profile", "interest", "notes"]

    def __init__(self, path=SOURCE_TYPES):
        self.rows = []
        self._parse(Path(path).read_text(encoding="utf-8"))
        self.by_host = {}
        for row in self.rows:
            self.by_host.setdefault(row["host"], []).append(row)
        for rows in self.by_host.values():
            rows.sort(key=lambda r: len(r["path"]), reverse=True)

    def _parse(self, text):
        in_table = False
        for line in text.splitlines():
            if not line.startswith("|"):
                in_table = False
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if [c.lower() for c in cells] == self.COLUMNS:
                in_table = True
                continue
            if not in_table or set(cells[0]) <= {"-", ":"} or len(cells) != len(self.COLUMNS):
                continue
            row = dict(zip(self.COLUMNS, cells))
            host, _, path = row["domain"].lower().partition("/")
            row["host"] = host
            row["path"] = "/" + path if path else ""
            row["names"] = [n.strip() for n in row["organisation"].split(" / ") if n.strip()]
            row["is_primary_capable"] = not row["notes"].lower().startswith("not a primary")
            self.rows.append(row)

    def lookup(self, url):
        parts = urllib.parse.urlsplit(url)
        host = (parts.hostname or "").lower()
        path = parts.path or "/"
        if host.endswith(".onion"):
            return {"domain": host, "organisation": None, "type": "actor",
                    "access_profile": "actor_statement", "interest": "actor",
                    "notes": "onion host: built-in rule", "is_primary_capable": True,
                    "matched": "rule:onion"}
        labels = host.split(".")
        for i in range(len(labels) - 1):
            candidate = ".".join(labels[i:])
            for row in self.by_host.get(candidate, []):
                if not row["path"] or path.lower().startswith(row["path"]):
                    out = {k: row[k] for k in self.COLUMNS}
                    out["organisation"] = row["names"][0]
                    out["is_primary_capable"] = row["is_primary_capable"]
                    out["matched"] = row["domain"]
                    return out
        return {"domain": host, "organisation": None, "type": "unknown",
                "access_profile": "undisclosed", "interest": None,
                "notes": "host not in source-types.md", "is_primary_capable": False,
                "matched": None}

    def names(self):
        """(compiled name pattern, row) for every organisation name, longest first."""
        out = []
        for row in self.rows:
            for name in row["names"]:
                if len(name) < 3:
                    continue
                out.append((re.compile(r"(?<![\w-])" + re.escape(name) + r"(?![\w-])"), name, row))
        out.sort(key=lambda t: len(t[1]), reverse=True)
        return out


# --- fetcher ---------------------------------------------------------------------------

class _HTTPSConnection(http.client.HTTPSConnection):
    def connect(self):
        super().connect()
        self.sock.settimeout(READ_TIMEOUT)


class _HTTPConnection(http.client.HTTPConnection):
    def connect(self):
        super().connect()
        self.sock.settimeout(READ_TIMEOUT)


class _HTTPSHandler(urllib.request.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(_HTTPSConnection, req)


class _HTTPHandler(urllib.request.HTTPHandler):
    def http_open(self, req):
        return self.do_open(_HTTPConnection, req)


class FetchResult:
    def __init__(self, url, status, body=None, content_type=None, final_url=None,
                 error=None, from_cache=False):
        self.url = url
        self.status = status          # ok | pdf | blocked_by_robots | http_error | ...
        self.body = body
        self.content_type = content_type
        self.final_url = final_url or url
        self.error = error
        self.from_cache = from_cache

    @property
    def ok(self):
        return self.status == "ok"

    def log(self):
        return {"url": self.url, "final_url": self.final_url, "status": self.status,
                "from_cache": self.from_cache, "reason": self.error}


class Fetcher:
    def __init__(self, table, cache_dir=None, use_cache=True, fixtures=None):
        self.table = table
        self.use_cache = use_cache
        self.cache_dir = Path(cache_dir or os.environ.get("CTI_SKILLS_CACHE")
                              or Path.home() / ".cache" / "cti-skills" / "provenance")
        self.fixtures = fixtures or {}
        self.opener = urllib.request.build_opener(_HTTPHandler, _HTTPSHandler)
        self.host_locks = {}
        self.host_last = {}
        self.skipped_hosts = {}
        self.robots = {}
        self.lock = threading.Lock()
        self.global_slots = threading.Semaphore(MAX_HOSTS_IN_FLIGHT)
        self.fetch_count = 0
        self.log = []

    # cache ---------------------------------------------------------------------------
    def _cache_paths(self, url):
        key = hashlib.sha256(url.encode("utf-8")).hexdigest()
        return self.cache_dir / (key + ".body"), self.cache_dir / (key + ".json")

    def _cache_read(self, url):
        body_p, meta_p = self._cache_paths(url)
        if not (self.use_cache and body_p.exists() and meta_p.exists()):
            return None, None
        try:
            return body_p.read_bytes(), json.loads(meta_p.read_text())
        except (OSError, ValueError):
            return None, None

    def _cache_write(self, url, body, meta):
        if not self.use_cache:
            return
        try:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            body_p, meta_p = self._cache_paths(url)
            body_p.write_bytes(body)
            meta_p.write_text(json.dumps(meta))
        except OSError:
            pass

    def text_path(self, url):
        key = hashlib.sha256(url.encode("utf-8")).hexdigest()
        return self.cache_dir / (key + ".txt")

    def _ttl(self, url):
        if url.endswith("/robots.txt"):
            return TTL_ROBOTS
        return TTL_PRIMARY if self.table.lookup(url)["type"] in PRIMARY_TYPES else TTL_PRESS

    # robots --------------------------------------------------------------------------
    def _allowed(self, url):
        parts = urllib.parse.urlsplit(url)
        origin = f"{parts.scheme}://{parts.netloc}"
        with self.lock:
            rp = self.robots.get(origin)
        if rp is None:
            res = self._get(origin + "/robots.txt", check_robots=False)
            rp = urllib.robotparser.RobotFileParser()
            if res.ok:
                rp.parse(res.body.decode("utf-8", "replace").splitlines())
            elif res.status == "http_error" and res.error and res.error.startswith("HTTP 4"):
                rp.parse([])                                  # RFC 9309: 4xx means no restrictions
            else:
                rp.parse(["User-agent: *", "Disallow: /"])    # unreachable: assume disallow
            with self.lock:
                self.robots[origin] = rp
        return rp.can_fetch(ROBOTS_AGENT, url)

    # fetch ---------------------------------------------------------------------------
    def fetch(self, url):
        res = self._get(url, check_robots=True)
        with self.lock:
            self.log.append(res.log())
        return res

    def _get(self, url, check_robots):
        if url in self.fixtures:
            return self._from_fixture(url)
        if self.fixtures:
            return FetchResult(url, "http_error", error="HTTP 404 (not in fixture map)")
        parts = urllib.parse.urlsplit(url)
        if parts.scheme not in ("http", "https") or not parts.hostname:
            return FetchResult(url, "unsupported_url", error="only http and https are fetched")
        host = parts.hostname.lower()
        if host.endswith(".onion"):
            return FetchResult(url, "not_fetched", error="onion hosts are never fetched")
        if host in self.skipped_hosts:
            return FetchResult(url, "host_skipped", error=self.skipped_hosts[host])

        body, meta = self._cache_read(url)
        now = time.time()
        if meta and now - meta.get("fetched_at", 0) < self._ttl(url):
            return self._result_from_cache(url, body, meta)

        if check_robots and not self._allowed(url):
            return FetchResult(url, "blocked_by_robots",
                               error="robots.txt disallows this path; paste the text to continue")

        with self.lock:
            if check_robots:
                self.fetch_count += 1
                if self.fetch_count > MAX_URLS:
                    return FetchResult(url, "cap_reached",
                                       error=f"hard cap of {MAX_URLS} URLs per invocation reached")
            host_lock = self.host_locks.setdefault(host, threading.Lock())

        with self.global_slots, host_lock:
            return self._request(url, host, body, meta)

    def _request(self, url, host, cached_body, cached_meta):
        delay = BACKOFF_START
        for attempt in range(1, MAX_ATTEMPTS + 1):
            wait = HOST_SPACING - (time.time() - self.host_last.get(host, 0))
            if wait > 0:
                time.sleep(wait)
            req = urllib.request.Request(url, headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/pdf;q=0.8,*/*;q=0.5",
                "Accept-Language": "en",
            })
            if cached_meta:
                if cached_meta.get("etag"):
                    req.add_header("If-None-Match", cached_meta["etag"])
                if cached_meta.get("last_modified"):
                    req.add_header("If-Modified-Since", cached_meta["last_modified"])
            try:
                with self.opener.open(req, timeout=CONNECT_TIMEOUT) as resp:
                    self.host_last[host] = time.time()
                    ctype = (resp.headers.get("Content-Type") or "").split(";")[0].strip().lower()
                    final_url = resp.geturl()
                    if ctype == "application/pdf" or final_url.lower().split("?")[0].endswith(".pdf"):
                        return FetchResult(url, "pdf", content_type=ctype, final_url=final_url,
                                           error="PDF: route to the pdf skill")
                    body = resp.read(MAX_BYTES + 1)
                    if len(body) > MAX_BYTES:
                        return FetchResult(url, "size_limit", final_url=final_url,
                                           error="response larger than 5 MB")
                    meta = {"fetched_at": time.time(), "etag": resp.headers.get("ETag"),
                            "last_modified": resp.headers.get("Last-Modified"),
                            "content_type": ctype, "final_url": final_url}
                    self._cache_write(url, body, meta)
                    return FetchResult(url, "ok", body, ctype, final_url)
            except urllib.error.HTTPError as e:
                self.host_last[host] = time.time()
                if e.code == 304 and cached_meta:
                    cached_meta["fetched_at"] = time.time()
                    self._cache_write(url, cached_body, cached_meta)
                    return self._result_from_cache(url, cached_body, cached_meta)
                if e.code in (429, 503):
                    if attempt == MAX_ATTEMPTS:
                        reason = f"HTTP {e.code} after {MAX_ATTEMPTS} attempts; host skipped for this run"
                        self.skipped_hosts[host] = reason
                        return FetchResult(url, "rate_limited", error=reason)
                    retry_after = e.headers.get("Retry-After") if e.headers else None
                    try:
                        pause = min(float(retry_after), 120.0) if retry_after else delay
                    except ValueError:
                        pause = delay
                    time.sleep(pause)
                    delay *= 2
                    continue
                return FetchResult(url, "http_error", error=f"HTTP {e.code}")
            except (urllib.error.URLError, OSError, http.client.HTTPException) as e:
                self.host_last[host] = time.time()
                return FetchResult(url, "network_error", error=str(getattr(e, "reason", e)))
        return FetchResult(url, "network_error", error="exhausted attempts")

    def _result_from_cache(self, url, body, meta):
        ctype = meta.get("content_type")
        if ctype == "application/pdf":
            return FetchResult(url, "pdf", content_type=ctype, final_url=meta.get("final_url"),
                               error="PDF: route to the pdf skill", from_cache=True)
        return FetchResult(url, "ok", body, ctype, meta.get("final_url"), from_cache=True)

    def _from_fixture(self, url):
        entry = self.fixtures[url]
        if isinstance(entry, dict):
            return FetchResult(url, entry.get("status", "http_error"), error=entry.get("reason"))
        try:
            return FetchResult(url, "ok", Path(entry).read_bytes(), "text/html", url, from_cache=True)
        except OSError as e:
            return FetchResult(url, "network_error", error=f"fixture unreadable: {e}")


# --- HTML extraction -------------------------------------------------------------------

VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
             "param", "source", "track", "wbr"}
# Removed wherever they appear.
SKIP_TAGS = {"nav", "footer", "aside", "script", "style", "form", "noscript", "svg",
             "iframe", "figure", "button", "select", "template"}
# Class, id or role tokens that suggest boilerplate. A matching subtree inside the
# article is dropped only when it is link-dense or a minor share of the article text,
# so a wrapper such as "sidebar-page-main" around the whole story is kept.
BOILERPLATE = re.compile(
    r"(?:^|[\s_-])(?:related|share|sharing|social|sidebar|footer|nav|navbar|menu|comments?|"
    r"newsletter|promo|widget|breadcrumbs?|popular|trending|recommended|subscribe|"
    r"advert|ads?|cookie|author-bio|byline|more-stories|read-more|also-read|latest|"
    r"webinars?|sponsored)(?:$|[\s_-])",
    re.IGNORECASE)
BLOCK_TAGS = {"p", "li", "blockquote", "h1", "h2", "h3", "h4", "td"}
LINK_DENSE = 0.4
MINOR_SHARE = 0.25


class Node:
    __slots__ = ("tag", "attrs", "children", "parent", "_text_len", "_link_len")

    def __init__(self, tag, attrs=None, parent=None):
        self.tag = tag
        self.attrs = attrs or {}
        self.children = []
        self.parent = parent
        self._text_len = None
        self._link_len = None

    def marker(self):
        return " ".join(filter(None, [self.attrs.get("class"), self.attrs.get("id"),
                                      self.attrs.get("role")]))

    def iter(self):
        yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.iter()

    def measure(self):
        """(text length, text length inside links) for the subtree."""
        if self._text_len is None:
            text = link = 0
            for child in self.children:
                if isinstance(child, Node):
                    t, l = child.measure()
                    text += t
                    link += t if child.tag == "a" else l
                else:
                    text += len(child.strip())
            self._text_len, self._link_len = text, link
        return self._text_len, self._link_len


class ArticleParser(HTMLParser):
    """Builds a small tree, then selects the article body by paragraph-text score."""

    def __init__(self, base_url):
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.root = Node("root")
        self.current = self.root
        self.meta = {}
        self.jsonld = []
        self.title = None
        self.time_datetimes = []
        self._capture = None        # "title" | "jsonld" | "skip"
        self._capture_tag = None
        self._buffer = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self._capture:
            return
        if tag == "meta":
            key = (a.get("property") or a.get("name") or a.get("itemprop") or "").lower()
            if key and a.get("content"):
                self.meta.setdefault(key, a["content"].strip())
            return
        if tag == "time" and a.get("datetime"):
            self.time_datetimes.append(a["datetime"])
        if tag in VOID_TAGS:
            return
        if tag == "title" and self.title is None:
            self._capture, self._capture_tag, self._buffer = "title", tag, []
            return
        if tag == "script":
            kind = "jsonld" if (a.get("type") or "").lower() == "application/ld+json" else "skip"
            self._capture, self._capture_tag, self._buffer = kind, tag, []
            return
        if tag == "style":
            self._capture, self._capture_tag, self._buffer = "skip", tag, []
            return
        if tag == "p" and self.current.tag == "p":
            self.current = self.current.parent          # implicit </p>
        node = Node(tag, a, self.current)
        self.current.children.append(node)
        self.current = node

    def handle_endtag(self, tag):
        if self._capture:
            if tag == self._capture_tag:
                if self._capture == "title":
                    self.title = " ".join("".join(self._buffer).split())
                elif self._capture == "jsonld":
                    self.jsonld.append("".join(self._buffer))
                self._capture = None
            return
        node = self.current
        while node is not None and node.tag != tag:
            node = node.parent
        if node is not None and node.parent is not None:
            self.current = node.parent

    def handle_data(self, data):
        if self._capture:
            self._buffer.append(data)
        else:
            self.current.children.append(data)

    # selection -----------------------------------------------------------------------
    def _prune(self, node, in_article=False):
        kept = []
        for child in node.children:
            if isinstance(child, Node):
                if child.tag in SKIP_TAGS and not (
                        child.tag == "figure" and any(n.tag == "table" for n in child.iter())):
                    continue                        # a figure that wraps a table is kept
                if child.tag == "header" and not in_article:
                    continue
                self._prune(child, in_article or child.tag == "article")
            kept.append(child)
        node.children = kept

    def _content_root(self):
        scores = {}
        held = {}                   # <article>/<main> -> paragraph text inside it
        page_total = 0
        for node in self.root.iter():
            if node.tag != "p" or node.parent is None:
                continue
            length = node.measure()[0]
            if length < 60:
                continue
            page_total += length
            parent = node.parent
            scores[parent] = scores.get(parent, 0) + length
            if parent.parent is not None:
                scores[parent.parent] = scores.get(parent.parent, 0) + length / 2
            up = parent
            while up is not None:
                if up.tag in ("article", "main"):
                    held[up] = held.get(up, 0) + length
                up = up.parent
        if not scores:
            return self.root
        best = max(scores, key=scores.get)
        # Widen to an enclosing <article> or <main> when it holds most of the same text,
        # or when the body is split across sibling sections and the enclosing element
        # holds most of the paragraph text on the page.
        node = best.parent
        while node is not None and node.parent is not None:
            if node.tag in ("article", "main") and (
                    best.measure()[0] >= 0.6 * node.measure()[0]
                    or held.get(node, 0) >= 0.6 * page_total):
                return node
            node = node.parent
        return best

    def blocks(self):
        self._prune(self.root)
        root = self._content_root()
        total = max(root.measure()[0], 1)
        out = []
        self._collect(root, root, total, out)
        if not any(b["tag"] == "h1" for b in out):
            for node in self.root.iter():
                if node.tag == "h1":
                    text, _ = self._flatten(node)
                    if text:
                        out.insert(0, {"tag": "h1", "text": text, "links": []})
                    break
        return out

    def _collect(self, node, root, total, out):
        for child in node.children:
            if not isinstance(child, Node):
                continue
            marker = child.marker()
            if child is not root and marker and BOILERPLATE.search(marker):
                text_len, link_len = child.measure()
                if text_len == 0 or link_len / text_len >= LINK_DENSE or text_len / total < MINOR_SHARE:
                    continue
            if child.tag == "tr":
                cells, links = [], []
                for cell in child.children:
                    if isinstance(cell, Node) and cell.tag in ("td", "th"):
                        text, found = self._flatten(cell)
                        shift = len(" | ".join(cells + [""])) if cells else 0
                        for link in found:
                            link["offset"] += shift
                        cells.append(text)
                        links.extend(found)
                if any(cells):
                    out.append({"tag": "tr", "text": " | ".join(cells), "links": links})
                continue
            if child.tag in BLOCK_TAGS and not any(
                    n.tag in BLOCK_TAGS for n in child.iter() if n is not child):
                text, links = self._flatten(child)
                if text:
                    out.append({"tag": child.tag, "text": text, "links": links})
            else:
                self._collect(child, root, total, out)

    def _flatten(self, node):
        parts, links = [], []

        def walk(n, link):
            for child in n.children:
                if isinstance(child, Node):
                    if child.tag == "a" and child.attrs.get("href") and link is None:
                        entry = {"href": urllib.parse.urljoin(self.base_url,
                                                              child.attrs["href"].strip()),
                                 "start": len("".join(parts)), "text": []}
                        walk(child, entry)
                        entry["text"] = " ".join("".join(entry["text"]).split())
                        links.append(entry)
                    else:
                        if child.tag == "br":
                            parts.append(" ")
                        walk(child, link)
                else:
                    parts.append(child)
                    if link is not None:
                        link["text"].append(child)

        walk(node, None)
        raw = "".join(parts)
        for link in links:
            link["offset"] = len(" ".join(raw[:link["start"]].split()))
        return " ".join(raw.split()), links


def iso_date(value):
    if not value:
        return None
    m = RE_ISO_DATE.search(str(value))
    if not m:
        return None
    try:
        return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3))).isoformat()
    except ValueError:
        return None


def _walk_jsonld(node):
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from _walk_jsonld(v)
    elif isinstance(node, list):
        for v in node:
            yield from _walk_jsonld(v)


def split_sentences(text):
    return [s.strip() for s in RE_SENTENCE.split(text) if s.strip()]


def sentence_at(text, offset):
    pos = 0
    for sentence in split_sentences(text):
        start = text.find(sentence, pos)
        if start < 0:
            continue
        end = start + len(sentence)
        if start <= offset <= end:
            return sentence
        pos = end
    return text if len(text) <= 600 else text[:600]


class Page:
    """Extracted fields for one fetched document."""

    def __init__(self, url, body_bytes):
        self.url = url
        charset = "utf-8"
        head = body_bytes[:4096].decode("ascii", "replace")
        m = re.search(r"charset=[\"']?([\w-]+)", head, re.IGNORECASE)
        if m:
            charset = m.group(1)
        try:
            markup = body_bytes.decode(charset, "replace")
        except LookupError:
            markup = body_bytes.decode("utf-8", "replace")
        parser = ArticleParser(url)
        try:
            parser.feed(markup)
            parser.close()
        except Exception:                # malformed markup: keep what was parsed so far
            pass
        try:
            self.blocks = parser.blocks()
        except RecursionError:
            self.blocks = []
        self.meta = parser.meta
        self.jsonld = []
        for raw in parser.jsonld:
            try:
                self.jsonld.extend(_walk_jsonld(json.loads(raw)))
            except ValueError:
                continue
        self._title_tag = parser.title
        self._times = parser.time_datetimes

    @property
    def title(self):
        for node in self.jsonld:
            if node.get("headline"):
                return html.unescape(str(node["headline"])).strip()
        for key in ("og:title", "twitter:title"):
            if self.meta.get(key):
                return self.meta[key]
        for b in self.blocks:
            if b["tag"] == "h1":
                return b["text"]
        return self._title_tag or None

    @property
    def date_published(self):
        for node in self.jsonld:
            d = iso_date(node.get("datePublished"))
            if d:
                return d
        for key in ("article:published_time", "og:article:published_time", "date", "pubdate",
                    "publish-date", "publish_date", "parsely-pub-date", "dc.date.issued",
                    "dc.date", "dcterms.created", "sailthru.date", "datepublished"):
            d = iso_date(self.meta.get(key))
            if d:
                return d
        for value in self._times:
            d = iso_date(value)
            if d:
                return d
        return None

    @property
    def paragraphs(self):
        return [b for b in self.blocks if b["tag"] in ("p", "li", "blockquote", "td", "tr")]

    def text(self):
        return "\n\n".join(b["text"] for b in self.blocks)

    def sentences(self):
        for index, block in enumerate(self.paragraphs):
            for sentence in split_sentences(block["text"]):
                yield index, sentence

    def body_links(self):
        for index, block in enumerate(self.paragraphs):
            for link in block["links"]:
                parts = urllib.parse.urlsplit(link["href"])
                if parts.scheme not in ("http", "https"):
                    continue
                href = urllib.parse.urlunsplit(parts._replace(fragment=""))
                yield {"href": href, "text": link["text"], "paragraph": index,
                       "sentence": sentence_at(block["text"], link["offset"])}


def url_date(url):
    m = RE_URL_DATE.search(urllib.parse.urlsplit(url).path)
    if not m:
        return None
    try:
        return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3) or 1)).isoformat()
    except ValueError:
        return None


def within_window(article_date, primary_date, month_only=False):
    a = dt.date.fromisoformat(article_date)
    p = dt.date.fromisoformat(primary_date)
    before = WINDOW_BEFORE_DAYS + (31 if month_only else 0)
    return -WINDOW_AFTER_DAYS - (31 if month_only else 0) <= (a - p).days <= before


RE_NEGATION = re.compile(r"\b(?:no|not|never|without|neither|nor)\b|n['’]t\b", re.IGNORECASE)


def matches_affirmed(patterns, text):
    """Like matches_any, but a match that follows a negation in the same clause is ignored:
    "we did not observe a ransom note" is not evidence of access to an actor's statement."""
    for pattern in patterns:
        for m in pattern.finditer(text):
            clause = re.split(r"[,;:]", text[:m.start()])[-1]
            if not RE_NEGATION.search(clause[-60:]):
                return True
    return False


def matches_any(patterns, text):
    return any(p.search(text) for p in patterns)


def same_org(a, b):
    return bool(a and b and a == b)


# --- resolution ------------------------------------------------------------------------

class Resolver:
    def __init__(self, table, fetcher, max_hops=MAX_HOPS, today=None):
        self.table = table
        self.fetcher = fetcher
        self.max_hops = max_hops
        self.today = today or dt.date.today()
        self.names = table.names()

    def resolve(self, url):
        out = {
            "input_url": url, "status": "unresolved", "provenance_basis": "script-resolved",
            "chain": [], "primary_source": None, "other_primaries": [], "primary_cites": [],
            "background_references": [], "unclassified_candidates": [],
            "circular_citations": False,
            "recency": {"date_observed": None, "date_published": None, "age_days": None,
                        "superseded_by": None},
            "attribution_sentences": [], "unattributed_sourcing": [],
            "unresolved": [{"field": "recency.date_observed",
                            "reason": "when the activity happened is stated in prose, if at "
                                      "all; recorded by /claim-extraction"}],
            "summary": None,
        }
        self._walk(url, 0, {url}, out, via=None)
        primary = out["primary_source"]
        if primary and primary.get("url"):
            out["status"] = "resolved"
            published = primary.get("date_published")
            out["recency"]["date_published"] = published
            if published:
                out["recency"]["age_days"] = (self.today - dt.date.fromisoformat(published)).days
        elif not any(u["field"] == "primary_source" for u in out["unresolved"]):
            out["unresolved"].append({"field": "primary_source",
                                      "reason": "no originating document located"})
        out["unclassified_candidates"].sort(
            key=lambda c: (not c["in_attribution_sentence"], c["paragraph"]))
        del out["unclassified_candidates"][10:]
        out["summary"] = self._summary(out)
        return out

    def _hop(self, url, cls, page=None, fidelity=None, notes=None, anchor=None):
        return {"org": cls["organisation"], "type": cls["type"], "url": url,
                "date_published": page.date_published if page else None,
                "title": page.title if page else None,
                "fidelity": fidelity, "anchor_in_previous_hop": anchor, "notes": notes}

    def _read_primary(self, url, cls, anchor):
        """Fetch a primary-type document. Returns (primary, hop)."""
        res = self.fetcher.fetch(url)
        page = Page(res.final_url, res.body) if res.ok else None
        note = None if res.ok else f"primary located but not read: {res.error}"
        hop = self._hop(url, cls, page, anchor=anchor, notes=note,
                        fidelity=None if res.ok else "unresolved")
        return self._primary(url, cls, page, res), hop, page

    def _cites(self, page, url, cls, out):
        """Other originating organisations the primary itself links to or names as a source."""
        if page is None:
            return
        self._attribution(page, url, out)
        candidates, _, _ = self._candidates(page, url, cls, set(), out)
        # From a primary, keep an unclassified host only where it is named as a source.
        out["unclassified_candidates"] = [
            c for c in out["unclassified_candidates"]
            if c["found_in"] != url or c["in_attribution_sentence"]]
        seen = {c["org"] for c in out["primary_cites"]}
        for cand in candidates:
            org = cand["cls"]["organisation"]
            if org in seen or len(out["primary_cites"]) >= 10:
                continue
            seen.add(org)
            out["primary_cites"].append({
                "org": org, "type": cand["cls"]["type"], "url": cand["href"],
                "anchor_in_primary": cand["sentence"],
                "in_attribution_sentence": bool(cand["attributed"]), "read": False,
                "note": "linked from the primary; not read. A claim the primary relays from "
                        "this organisation belongs to it and needs its own chain"})
        relayed = [a for a in out["attribution_sentences"] if a["document_url"] == url]
        if relayed:
            out["primary_relays"] = {
                "sentences": len(relayed),
                "note": "the primary attributes at least one statement to another source. "
                        "Read attribution_sentences for this document: the claims in them "
                        "are relayed, and this organisation's access does not apply to them"}

    def _walk(self, url, depth, visited, out, via):
        """Returns True once a primary has been recorded."""
        cls = self.table.lookup(url)
        if cls["type"] in PRIMARY_TYPES and cls["is_primary_capable"]:
            primary, hop, page = self._read_primary(url, cls, via)
            out["chain"].append(hop)
            out["primary_source"] = primary
            self._cites(page, url, cls, out)
            if primary["resolution"] == "linked_not_read":
                out["unresolved"].append({"field": "primary_source.document", "url": url,
                                          "reason": hop["notes"]})
            return True

        res = self.fetcher.fetch(url)
        if not res.ok:
            out["chain"].append(self._hop(url, cls, fidelity="unresolved", anchor=via,
                                          notes=f"fetch failed: {res.error}"))
            out["unresolved"].append({"field": "chain", "url": url, "reason": res.error})
            return False

        page = Page(res.final_url, res.body)
        out["chain"].append(self._hop(url, cls, page, anchor=via))
        hop_index = len(out["chain"]) - 1
        self._attribution(page, url, out)

        candidates, press_links, circular = self._candidates(page, url, cls, visited, out)
        if self._pick_primary(candidates, page, out):
            return True

        if depth + 1 < self.max_hops:
            for link in press_links[:MAX_PRESS_FOLLOW]:
                visited.add(link["href"])
                mark = len(out["unresolved"])
                if self._walk(link["href"], depth + 1, visited, out, via=link["sentence"]):
                    return True
                del out["chain"][hop_index + 1:]      # dead end: drop the failed branch
                del out["unresolved"][mark:]

        out["chain"][hop_index]["fidelity"] = "unresolved"
        if out["primary_source"] is not None:
            return False
        named = [a for a in out["attribution_sentences"]
                 if a["document_url"] == url and a["organisations"] and not a["links"]]
        if named:
            org = named[0]["organisations"][0]
            out["primary_source"] = {
                "org": org["org"], "type": org["type"], "title": None, "date_published": None,
                "url": None, "access": "undisclosed", "access_evidence": [],
                "stated_confidence": "not stated", "confidence_evidence": [], "hedges": [],
                "interest": org["interest"], "resolution": "named_not_linked",
                "named_in": named[0]["sentence"],
            }
            reason = (f"{org['org']} is named as the source but no document is linked; "
                      "the primary was not read")
        elif circular or out["circular_citations"]:
            reason = "circular press citations, no primary found"
        elif press_links and depth + 1 >= self.max_hops:
            reason = f"only press links found and the hop limit ({self.max_hops}) was reached"
        else:
            reason = "no link to a vendor, government, victim, actor or researcher document"
        extras = []
        if any(b["found_in"] == url for b in out["background_references"]):
            extras.append("linked primary-type documents were treated as background")
        cited = sorted({urllib.parse.urlsplit(c["url"]).hostname
                        for c in out["unclassified_candidates"] if c["found_in"] == url})
        if cited:
            extras.append("the article cites " + ", ".join(cited[:4])
                          + ", which the script does not classify")
        out["unresolved"].append({"field": "primary_source", "url": url,
                                  "reason": "; ".join([reason] + extras)})
        return False

    def _pick_primary(self, candidates, page, out):
        """Read the top candidates. Prefer one whose date places it at the article's origin."""
        article_date = page.date_published
        verified, unverified, seen_orgs = [], [], set()
        tries = 0
        for cand in candidates:
            org = cand["cls"]["organisation"]
            if org in seen_orgs:
                continue
            hint = url_date(cand["href"])
            if article_date and hint and not within_window(article_date, hint, month_only=True):
                self._background(cand, hint, page, out,
                                 f"published more than {WINDOW_BEFORE_DAYS} days before the "
                                 "article (date in the URL)")
                continue
            if tries >= MAX_PRIMARY_TRIES:
                seen_orgs.add(org)
                out["other_primaries"].append({
                    "org": org, "type": cand["cls"]["type"], "url": cand["href"],
                    "anchor_in_article": cand["sentence"], "read": False,
                    "note": "linked from the article; not read (per-article read limit)"})
                continue
            tries += 1
            primary, hop, ppage = self._read_primary(cand["href"], cand["cls"], cand["sentence"])
            published = primary["date_published"]
            if article_date and published and not within_window(article_date, published):
                self._background(cand, published, page, out,
                                 f"published more than {WINDOW_BEFORE_DAYS} days before the "
                                 "article (page metadata)")
            elif published and article_date:
                seen_orgs.add(org)
                verified.append((cand, primary, hop, ppage))
            elif cand["early"]:
                seen_orgs.add(org)
                primary["date_check"] = ("not verified: the script could not compare "
                                         "publication dates, so it could not confirm this "
                                         "document is the origin of the article")
                unverified.append((cand, primary, hop, ppage))
            else:
                self._background(cand, None, page, out,
                                 "publication date could not be checked and the link sits "
                                 f"below paragraph {EARLY_PARAGRAPHS} of the article")
        accepted = verified + unverified
        if not accepted:
            return False
        cand, primary, hop, ppage = accepted[0]
        out["chain"].append(hop)
        out["primary_source"] = primary
        self._cites(ppage, cand["href"], cand["cls"], out)
        if primary["resolution"] == "linked_not_read":
            out["unresolved"].append({"field": "primary_source.document", "url": cand["href"],
                                      "reason": hop["notes"]})
        read = []
        for cand, other, _, _ in accepted[1:]:
            other["anchor_in_article"] = cand["sentence"]
            other["read"] = other["resolution"] == "linked"
            other["note"] = ("linked from the same article. Claims found in this document "
                             "belong to this organisation. Independence from the first "
                             "primary is not established by the link alone")
            read.append(other)
        out["other_primaries"] = read + out["other_primaries"]
        return True

    def _background(self, cand, date, page, out, why):
        out["background_references"].append({
            "org": cand["cls"]["organisation"], "url": cand["href"], "date": date,
            "found_in": page.url, "anchor_in_article": cand["sentence"],
            "note": f"{why}; treated as background, not as the originating source"})

    def _candidates(self, page, url, cls, visited, out):
        candidates, press, circular = [], [], False
        seen = set()
        for link in page.body_links():
            href = link["href"]
            if href in seen or href == url:
                continue
            seen.add(href)
            lcls = self.table.lookup(href)
            if same_org(lcls["organisation"], cls["organisation"]):
                continue
            parts = urllib.parse.urlsplit(href)
            path = parts.path.strip("/")
            if not path or RE_PROMO_QUERY.search(parts.query) or RE_PROMO_PATH.match(parts.path):
                continue                          # homepage, tracked or marketing link
            attributed = matches_any(RE_ATTRIBUTION, link["sentence"])
            early = link["paragraph"] < EARLY_PARAGRAPHS
            if lcls["type"] in PRIMARY_TYPES and lcls["is_primary_capable"]:
                link.update(cls=lcls, early=early, attributed=attributed,
                            rank=(0 if early and attributed else 1 if early else
                                  2 if attributed else 3, link["paragraph"]))
                candidates.append(link)
            elif lcls["type"] == "press":
                if href in visited:
                    circular = out["circular_citations"] = True
                    continue
                press.append(link)
            elif lcls["type"] in ("unknown", "social"):
                out["unclassified_candidates"].append({
                    "url": href, "type": lcls["type"], "found_in": url,
                    "paragraph": link["paragraph"] + 1,
                    "anchor_in_article": link["sentence"],
                    "in_attribution_sentence": attributed,
                    "note": ("social post: the account holder is the source; identity not "
                             "verified by this script" if lcls["type"] == "social" else
                             "host not in source-types.md; not classified and not followed. "
                             "Add a row if this organisation is a known source")})
        candidates.sort(key=lambda c: c["rank"])
        press.sort(key=lambda l: (0 if matches_any(RE_ATTRIBUTION, l["sentence"]) else 1,
                                  l["paragraph"]))
        return candidates, press, circular

    def _named_orgs(self, sentence, own):
        """Organisations from the table named in a sentence. Longest name claims its span."""
        claimed, orgs, seen = [], [], set()
        for pattern, name, row in self.names:
            for m in pattern.finditer(sentence):
                if any(m.start() < e and s < m.end() for s, e in claimed):
                    continue
                claimed.append((m.start(), m.end()))
                org = row["names"][0]
                if org == own or org in seen:
                    continue
                seen.add(org)
                orgs.append({"org": org, "matched_name": name, "type": row["type"],
                             "interest": row["interest"], "position": m.start()})
        orgs.sort(key=lambda o: o.pop("position"))
        return orgs

    def _attribution(self, page, url, out):
        links_by_sentence = {}
        for link in page.body_links():
            links_by_sentence.setdefault(link["sentence"], []).append(link["href"])
        own = self.table.lookup(url)["organisation"]
        for index, sentence in page.sentences():
            if matches_any(RE_ATTRIBUTION, sentence):
                orgs = self._named_orgs(sentence, own)
                if orgs or sentence in links_by_sentence:
                    out["attribution_sentences"].append({
                        "document_url": url, "location": f"paragraph {index + 1}",
                        "sentence": sentence, "organisations": orgs,
                        "links": links_by_sentence.get(sentence, [])})
            elif matches_any(RE_UNATTRIBUTED, sentence):
                out["unattributed_sourcing"].append({
                    "document_url": url, "location": f"paragraph {index + 1}",
                    "sentence": sentence})

    def _primary(self, url, cls, page, res):
        primary = {"org": cls["organisation"], "type": cls["type"], "title": None,
                   "date_published": None, "url": url, "access": "undisclosed",
                   "access_evidence": [], "stated_confidence": "not stated",
                   "confidence_evidence": [], "hedges": [], "interest": cls["interest"],
                   "resolution": "linked", "null_reasons": {}}
        if cls["notes"].lower().startswith("press release wire"):
            primary["org_note"] = ("press release wire: the issuing organisation named in the "
                                   "release is the source, not the wire")
        if page is None:
            reason = res.error or "document not read"
            primary["resolution"] = "linked_not_read"
            primary["null_reasons"] = {"title": reason, "date_published": reason}
            primary["access_note"] = "undisclosed because the document was not read"
            return primary
        primary["title"] = page.title
        primary["date_published"] = page.date_published
        if not primary["title"]:
            primary["null_reasons"]["title"] = "no title in page metadata"
        if not primary["date_published"]:
            primary["null_reasons"]["date_published"] = "no publication date in page metadata"
        counts = {}
        for index, sentence in page.sentences():
            location = f"paragraph {index + 1}"
            if matches_any(RE_CONFIDENCE, sentence):
                primary["confidence_evidence"].append({"sentence": sentence, "location": location})
            elif matches_any(RE_HEDGE, sentence) and len(primary["hedges"]) < 25:
                primary["hedges"].append({"sentence": sentence, "location": location})
            for name, patterns in RE_ACCESS:
                if matches_affirmed(patterns, sentence):
                    counts[name] = counts.get(name, 0) + 1
                    if len(primary["access_evidence"]) < 25:
                        primary["access_evidence"].append(
                            {"access": name, "sentence": sentence, "location": location})
        allowed = ACCESS_BY_TYPE.get(cls["type"], set())
        counts = {k: v for k, v in counts.items() if k in allowed}
        if counts:
            order = [name for name, _ in ACCESS_PATTERNS]
            primary["access"] = max(order, key=lambda n: (counts.get(n, 0), -order.index(n)))
        if primary["confidence_evidence"]:
            primary["stated_confidence"] = primary["confidence_evidence"][0]["sentence"]
        return primary

    def _summary(self, out):
        chain = out["chain"]
        if not chain:
            return "Nothing could be fetched."
        first = chain[0]
        name = first["org"] or urllib.parse.urlsplit(first["url"]).hostname
        primary = out["primary_source"]
        if out["status"] != "resolved":
            reasons = "; ".join(dict.fromkeys(
                u["reason"] for u in out["unresolved"]
                if u["field"] in ("primary_source", "chain")))
            return (f"This {name} page could not be traced to an originating source: "
                    f"{reasons}. Provenance is unresolved: access level untraced, claim "
                    "support tentative at best.")
        if len(chain) == 1:
            lead = f"This is a primary document from {primary['org']} ({primary['type']})"
        else:
            via = [h["org"] or urllib.parse.urlsplit(h["url"]).hostname for h in chain[1:-1]]
            route = "".join(f" via {v}'s coverage" for v in via)
            lead = (f"This {name} article{route} traces to a document from {primary['org']}"
                    f" ({primary['type']})")
        title = f", \"{primary['title']}\"" if primary.get("title") else ""
        date = (f", published {primary['date_published']}" if primary.get("date_published")
                else ", publication date not found")
        extra = ""
        if out["other_primaries"]:
            orgs = ", ".join(dict.fromkeys(o["org"] for o in out["other_primaries"]))
            extra = f" The article also links {orgs}; independence not established."
        if primary.get("date_check"):
            extra += " The primary's date could not be checked against the article's."
        if primary.get("resolution") == "linked_not_read":
            return (f"{lead}{date}. The document was located but not read "
                    f"({primary['null_reasons'].get('title')}): access and confidence "
                    f"unknown.{extra}")
        access = (f"Its text indicates access by {primary['access'].replace('_', ' ')}"
                  if primary["access"] != "undisclosed" else "It does not state how it knows")
        conf = ("it states its confidence" if primary["stated_confidence"] != "not stated"
                else "no confidence statement was found")
        return f"{lead}{title}{date}. {access}; {conf}.{extra}"


# --- CLI -------------------------------------------------------------------------------

def load_fixtures(path):
    if not path:
        return {}
    base = Path(path).resolve().parent
    mapping = json.loads(Path(path).read_text())
    out = {}
    for url, target in mapping.items():
        out[url] = target if isinstance(target, dict) else str((base / target).resolve())
    return out


def cmd_classify(args, table):
    print(json.dumps([dict(url=u, **table.lookup(u)) for u in args.urls], indent=2))
    return 0


def cmd_text(args, table):
    fetcher = Fetcher(table, args.cache_dir, not args.no_cache, load_fixtures(args.fixtures))
    res = fetcher.fetch(args.url)
    if not res.ok:
        print(json.dumps({"url": args.url, "status": res.status, "reason": res.error}, indent=2))
        return 2
    page = Page(res.final_url, res.body)
    path = fetcher.text_path(args.url)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(page.text(), encoding="utf-8")
    print(json.dumps({"url": args.url, "status": "ok", "title": page.title,
                      "date_published": page.date_published, "text_file": str(path),
                      "paragraphs": len(page.paragraphs),
                      "note": "full text is local only; do not upload or commit it"}, indent=2))
    return 0


def cmd_resolve(args, table):
    urls = list(dict.fromkeys(args.urls))
    if len(urls) > MAX_URLS or args.max_hops > MAX_HOPS:
        raise Refused(
            f"Refused: this script resolves at most {MAX_URLS} URLs and {MAX_HOPS} hops per "
            "invocation. Bulk provenance is served by the Liberty91 API, where chains are "
            "resolved once at ingest (see /lookup-liberty91).")
    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    fetcher = Fetcher(table, args.cache_dir, not args.no_cache, load_fixtures(args.fixtures))
    resolver = Resolver(table, fetcher, max(1, args.max_hops), today)
    with ThreadPoolExecutor(max_workers=MAX_HOSTS_IN_FLIGHT) as pool:
        results = list(pool.map(resolver.resolve, urls))
    print(json.dumps({
        "tool": "resolve_provenance", "version": "2.0",
        "resolved_at": today.isoformat(), "max_hops": resolver.max_hops,
        "source_types_rows": len(table.rows),
        "results": results, "fetch_log": fetcher.log,
        "note": "fidelity is null on resolved hops: it is a model judgement made by "
                "/quality-of-information-check, not by this script",
    }, indent=2, ensure_ascii=False))
    return 0 if all(r["status"] == "resolved" for r in results) else 2


def main(argv=None):
    parser = argparse.ArgumentParser(description="Resolve provenance chains deterministically.")
    sub = parser.add_subparsers(dest="command", required=True)

    def common(p):
        p.add_argument("--no-cache", action="store_true", help="do not read or write the local cache")
        p.add_argument("--cache-dir", help="default ~/.cache/cti-skills/provenance or $CTI_SKILLS_CACHE")
        p.add_argument("--fixtures", help="JSON map of URL to local HTML file; disables the network")

    p = sub.add_parser("resolve", help="resolve one or more URLs to their primary")
    p.add_argument("urls", nargs="+")
    p.add_argument("--max-hops", type=int, default=MAX_HOPS,
                   help="1 = article to primary; 2 = article to article to primary (default 2)")
    p.add_argument("--today", help="override the assessment date (YYYY-MM-DD), for tests")
    common(p)

    p = sub.add_parser("classify", help="classify URLs against source-types.md; no network")
    p.add_argument("urls", nargs="+")

    p = sub.add_parser("text", help="extract article text to the local cache")
    p.add_argument("url")
    common(p)

    args = parser.parse_args(argv)
    try:
        table = SourceTable()
    except OSError as e:
        print(f"ERROR: cannot read {SOURCE_TYPES}: {e}", file=sys.stderr)
        return 1
    try:
        return {"resolve": cmd_resolve, "classify": cmd_classify, "text": cmd_text}[args.command](args, table)
    except Refused as e:
        print(str(e), file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
