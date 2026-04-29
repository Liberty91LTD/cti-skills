#!/usr/bin/env python3
"""
seed-misp-test-data.py — seed a MISP instance with 100 demo events for
Diamond-Model-overlap discovery training and demonstrations.

Each event has a unique fake intrusion-set name. Patterns are encoded
across the OTHER three Diamond Model dimensions (Capability, Infrastructure,
Victim) so an analyst can identify clusters by walking those dimensions and
then merge the over-fragmented intrusion-set names into the underlying
actor groups.

Cluster design (100 events, 100 unique IS names):

  ID  count  pattern                                                strength
  A   12     Capability + Infrastructure (shared malware + C2 IPs)  STRONG
  B   10     Capability + Victim (shared malware + healthcare/US)   STRONG
  C    9     Infrastructure + Victim (shared cert + DACH/mfg)       STRONG
  D    8     Capability + Infra + Victim (APT — gov/APAC)           VERY STRONG
  E    7     Capability only (shared phishing kit)                  WEAK
  F    6     Infrastructure only (shared JARM fingerprint)          WEAK
  G    5     Victim only (same target org over time)                NOISE / REJECT
  H    5     Naming similarity (CipherSnake-1..5) but no D-M tie    TRAP / REJECT
  -   38     Singletons — distinct everything                       NOISE

Authentication: same as tools/clis/misp.py.
  MISP_URL       (e.g. https://misp.example.org)
  MISP_API_KEY   (or MISP_KEY)

Usage:
  tools/seed-misp-test-data.py --insecure                          # all 100
  tools/seed-misp-test-data.py --insecure --limit 5                # smoke test
  tools/seed-misp-test-data.py --insecure --dry-run                # preview events as JSON
  tools/seed-misp-test-data.py --insecure --cluster A              # only cluster A

Notes:
  - Idempotency: each run creates NEW events (MISP assigns fresh IDs).
    Running twice doubles the data. Delete via the MISP UI / API if you
    need to reset.
  - Determinism: random seed is fixed (42), so the per-event IOCs and
    victim names are stable across runs. Re-running with the same seed
    creates structurally-identical events with new MISP IDs.
  - Tags applied: tlp:amber, intrusion-set:<FakeName>, malware:<Family>,
    misp-galaxy:mitre-attack-pattern style. None of the fake intrusion
    sets exist in the curated misp-galaxy — they're free-text tags.
"""

import argparse
import json
import os
import random
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

API_KEY = os.environ.get("MISP_API_KEY") or os.environ.get("MISP_KEY") or ""
BASE_URL = os.environ.get("MISP_URL", "").rstrip("/")

random.seed(42)


# --------------------------------------------------------------------------
# Cluster definitions
# --------------------------------------------------------------------------

# Each cluster declares the ELEMENTS that overlap across its events. The
# generator below picks values from these pools to build per-event content.

CLUSTERS = {
    "A": {
        "name_seed": ["RoseGarden", "ScarletViper", "CrimsonStag", "RubyOrchid",
                      "GarnetBat", "AmaranthFox", "MaroonSparrow", "CarmineDolphin",
                      "VermilionStarling", "CherryWolf", "CoralLynx", "BurgundyDrake"],
        "size": 12,
        "shared_malware": ["ChromaWolf", "ChromaWolf-Loader"],
        "shared_c2_ips": ["185.220.101.42", "185.220.101.55", "185.220.101.99"],
        "shared_domain_pattern": ["cloud-billing", "payment-secure", "verify-account"],
        "shared_tld_pool": [".net", ".io", ".cloud"],
        "shared_cert_sha256": "a1b2c3d4e5f6071829304152637485969a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d",
        "victim_sectors": ["banking", "insurance", "fintech"],
        "victim_countries": ["DE", "NL", "FR", "BE", "LU", "AT"],
        "ttps": ["T1566.001", "T1059.001", "T1071.001", "T1112"],
        "summary": "EU financial sector intrusions; ChromaWolf stealer + loader",
    },
    "B": {
        "name_seed": ["SaffronTigris", "AmberLynx", "TopazPanther", "OchreLion",
                      "MarigoldFalcon", "CitrineGoshawk", "GoldenHarrier",
                      "HoneyKestrel", "ApricotEagle", "PeachOwl"],
        "size": 10,
        "shared_malware": ["LunarMoth", "LunarMoth-RAT"],
        "shared_c2_ips": [],  # different infra each event
        "shared_domain_pattern": [],  # different infra each event
        "shared_tld_pool": [".com", ".net", ".org"],
        "shared_cert_sha256": None,
        "victim_sectors": ["hospital", "pharmaceutical", "medical-research", "health-insurance"],
        "victim_countries": ["US"],  # same victim country
        "ttps": ["T1190", "T1078.004", "T1486", "T1567.002"],
        "summary": "US healthcare sector intrusions; LunarMoth RAT pivoting to ransomware",
    },
    "C": {
        "name_seed": ["ObsidianRaven", "IronCorvid", "BasaltMagpie", "GraphiteRook",
                      "OnyxJackdaw", "CharcoalCrow", "SlateNightingale",
                      "CoalThrush", "AnthraciteFinch"],
        "size": 9,
        "shared_malware": [],  # different malware each event — infra+victim only
        "shared_c2_ips": [],
        "shared_domain_pattern": [],
        "shared_tld_pool": [".xyz", ".pw", ".click"],
        "shared_cert_sha256": "feed1234beef5678cafe9012deadabcd1357024689bdcef02468ace13579fdb0",
        "shared_asn": "AS49447",
        "victim_sectors": ["manufacturing", "automotive", "industrial-machinery", "chemicals"],
        "victim_countries": ["DE", "AT", "CH"],
        "ttps": ["T1133", "T1486", "T1567.002"],
        "summary": "DACH manufacturing; varied ransomware behind a single shared TLS cert + bulletproof ASN",
    },
    "D": {
        "name_seed": ["VerdantMantis", "JadeStrand", "EmeraldOrchid",
                      "MalachiteWisp", "OliveOgre", "ForestSerpent",
                      "MossKraken", "FernViper"],
        "size": 8,
        "shared_malware": ["GlacierShade", "GlacierShade-Stage2"],
        "shared_c2_ips": ["192.0.2.41", "192.0.2.66"],
        "shared_domain_pattern": ["sharepoint-cdn", "office-edge", "teams-update"],
        "shared_tld_pool": [".com"],
        "shared_cert_sha256": "deadbeefcafebabe1234567890abcdefdeadbeefcafebabe1234567890abcdef",
        "shared_jarm": "27d40d40d29d40d1dc27d40d40d40d301a3eaa9aa7a32cb3a7af23b0c6dac1b6",
        "victim_sectors": ["government", "defence-contractor", "diplomatic"],
        "victim_countries": ["AU", "NZ", "JP", "TW", "PH", "ID"],
        "ttps": ["T1190", "T1505.003", "T1071.004", "T1041"],
        "summary": "APAC gov/defence — all three D-M dimensions overlap (highest-confidence cluster)",
    },
    "E": {
        "name_seed": ["AzureFalcon", "IndigoHawk", "CobaltKite", "TealOsprey",
                      "PrussianBuzzard", "DenimVulture", "SapphireMerlin"],
        "size": 7,
        "shared_malware": ["TidewashKit"],   # phishing kit family
        "shared_c2_ips": [],   # different infra each event — CAPABILITY-ONLY overlap
        "shared_domain_pattern": [],
        "shared_tld_pool": [".com", ".net", ".io", ".app"],
        "shared_cert_sha256": None,
        "victim_sectors": ["saas-vendor", "tech-startup", "cloud-platform", "developer-tools"],
        "victim_countries": ["US", "GB", "CA", "AU", "DE"],
        "ttps": ["T1566.002", "T1539", "T1110.003"],
        "summary": "TidewashKit AiTM phishing — same kit, different operators (or are they?)",
    },
    "F": {
        "name_seed": ["TerracottaSerpent", "BronzeAdder", "CopperCobra",
                      "RustViper", "OxideAsp", "SiennaPython"],
        "size": 6,
        "shared_malware": [],
        "shared_c2_ips": [],
        "shared_domain_pattern": [],
        "shared_tld_pool": [".net", ".io", ".dev"],
        "shared_cert_sha256": None,
        "shared_jarm": "29d29d20d29d29d21c29d29d29d29d8f8e7e6f5d4c3b2a1908f7e6d5c4b3a291",   # JARM-only signal
        "victim_sectors": ["legal", "consulting", "media", "real-estate", "logistics", "retail"],
        "victim_countries": ["US", "GB", "FR", "JP", "BR", "MX"],
        "ttps": ["T1071.001", "T1027"],   # commodity TTPs — should not cluster on these
        "summary": "Shared JARM only — INFRA-only signal, weak. Probably a popular C2 framework.",
    },
    "G": {
        "name_seed": ["GhostSiren", "VeiledHarpy", "SilentNymph", "QuietDryad", "MutedOread"],
        "size": 5,
        "shared_malware": [],
        "shared_c2_ips": [],
        "shared_domain_pattern": [],
        "shared_tld_pool": [".com"],
        "shared_cert_sha256": None,
        # SAME VICTIM ORG over time — should NOT be treated as same actor.
        "fixed_victim_org": "Helios Maritime Logistics",
        "victim_sectors": ["maritime-logistics"],
        "victim_countries": ["GR"],
        "ttps": ["T1566.001"],
        "summary": "Helios Maritime Logistics targeted 5x by different actors — VICTIM-only, do NOT merge",
    },
    "H": {
        "name_seed": ["CipherSnake-1", "CipherSnake-2", "CipherSnake-3",
                      "CipherSnake-4", "CipherSnake-5"],
        "size": 5,
        "shared_malware": [],
        "shared_c2_ips": [],
        "shared_domain_pattern": [],
        "shared_tld_pool": [".com", ".net", ".org", ".io", ".app"],
        "shared_cert_sha256": None,
        "victim_sectors": ["education", "non-profit", "media", "energy", "agriculture"],
        "victim_countries": ["US", "BR", "IN", "ZA", "TR"],
        "ttps": ["T1059.001", "T1071.001"],
        "summary": "Sequential names suggest cluster — but Diamond Model dimensions don't overlap. TRAP.",
    },
}

# 38 singleton intrusion-set names — random unique pairings for noise.
SINGLETON_NAMES = [
    "WisteriaPanther", "MagentaRook", "CeruleanShark", "TanRabbit", "PlumOctopus",
    "BeigeWalrus", "SilverBoar", "SnowyAlbatross", "FrostHedgehog", "SootBeetle",
    "MintTurtle", "PistachioRaccoon", "LimeBadger", "MossOtter", "AvocadoFox",
    "CinnamonFerret", "CocoaMink", "MochaWeasel", "EspressoSable", "TaupeStoat",
    "LavenderToad", "LilacBat", "OrchidNewt", "VioletAxolotl", "MauveSalamander",
    "MustardCheetah", "PaprikaJaguar", "CurryOcelot", "TurmericServal", "SaffronCaracal",
    "DenimGoat", "ChambrayDeer", "OxbloodMoose", "WineElk", "PortReindeer",
    "SeafoamSeahorse", "AquaSquid", "TealJellyfish",
]


# --------------------------------------------------------------------------
# Generators
# --------------------------------------------------------------------------

VICTIM_ORG_PREFIXES = [
    "Apex", "Boreal", "Cascade", "Delta", "Equinox", "Fjord", "Granite",
    "Helios", "Iberia", "Juniper", "Keystone", "Lyra", "Meridian", "Nimbus",
    "Orion", "Polaris", "Quasar", "Riviera", "Sierra", "Talisman", "Umbra",
    "Vesper", "Wexford", "Xanadu", "Yarrow", "Zenith",
]
VICTIM_ORG_SUFFIXES = {
    "banking": ["Bank", "Financial Group", "Banque", "Sparkasse", "Volksbank"],
    "insurance": ["Insurance", "Assurance", "Versicherung", "Mutual"],
    "fintech": ["Pay", "Wallet", "Capital", "Markets"],
    "hospital": ["Medical Center", "Hospital", "Health System", "Clinic"],
    "pharmaceutical": ["Pharma", "Therapeutics", "Biosciences", "Labs"],
    "medical-research": ["Research Institute", "Genomics", "Foundation"],
    "health-insurance": ["Health", "Care Plans", "BlueShield"],
    "manufacturing": ["Industries", "Werke", "Manufacturing", "Group"],
    "automotive": ["Motors", "Automobile", "AG", "Mobility"],
    "industrial-machinery": ["Engineering", "Maschinenbau", "Systems"],
    "chemicals": ["Chemicals", "Chemie", "Specialty"],
    "government": ["Ministry", "Department", "Agency", "Authority"],
    "defence-contractor": ["Defence", "Aerospace", "Systems Group", "Industries"],
    "diplomatic": ["Embassy", "Consulate", "Mission"],
    "saas-vendor": [], "tech-startup": [], "cloud-platform": [], "developer-tools": [],
    "legal": ["LLP", "& Partners", "Law Group"],
    "consulting": ["Consulting", "Advisors", "Strategy"],
    "media": ["Media", "Press", "Broadcasting"],
    "real-estate": ["Properties", "Realty", "Estates"],
    "logistics": ["Logistics", "Freight", "Cargo"],
    "retail": ["Retail", "Stores", "Markets"],
    "maritime-logistics": ["Maritime", "Shipping", "Logistics"],
    "education": ["University", "College", "Academy"],
    "non-profit": ["Foundation", "Trust", "Initiative"],
    "energy": ["Energy", "Power", "Utilities"],
    "agriculture": ["Agro", "AgriCorp", "Farms"],
}
SAAS_NAMES = ["TaskFlow", "PipelineHQ", "DeployStack", "MetricsCloud",
              "GitOps Lab", "ObservatoryCRM", "WorkbenchAI"]


def fake_hash(seed_str, length=64):
    """Deterministic-looking hex hash of a given length."""
    import hashlib
    h = hashlib.sha256(seed_str.encode()).hexdigest()
    while len(h) < length:
        h += hashlib.sha256((seed_str + h).encode()).hexdigest()
    return h[:length]


def fake_ip():
    return f"{random.randint(45, 199)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


def fake_domain(token_pool, tld_pool, salt):
    if token_pool:
        token = random.choice(token_pool)
    else:
        token = random.choice(["update", "secure", "verify", "portal", "api", "cdn", "files",
                               "auth", "mail", "vpn", "remote", "share"])
    suffix = random.choice(["", "-app", "-cloud", "-hub", "-edge", "-prod", str(random.randint(10, 99))])
    tld = random.choice(tld_pool) if tld_pool else random.choice([".com", ".net", ".org", ".io"])
    return f"{token}{suffix}{tld}".lstrip("-")


def fake_victim(sector, country, fixed=None):
    if fixed:
        return {"name": fixed, "sector": sector, "country": country}
    prefix = random.choice(VICTIM_ORG_PREFIXES)
    if sector in ("saas-vendor", "tech-startup", "cloud-platform", "developer-tools"):
        return {"name": random.choice(SAAS_NAMES), "sector": sector, "country": country}
    suffix = random.choice(VICTIM_ORG_SUFFIXES.get(sector, ["Group", "Holdings", "Co"]))
    return {"name": f"{prefix} {suffix}", "sector": sector, "country": country}


def build_event(intrusion_set, cluster_id, cluster, idx):
    """Return a MISP event payload (the inner Event dict)."""
    is_singleton = cluster_id == "-"
    info = (
        f"[{cluster_id}] Intrusion attributed to {intrusion_set} — "
        f"{cluster.get('summary', 'singleton incident')}"
    )

    # Pick capability
    if cluster["shared_malware"]:
        malware = random.choice(cluster["shared_malware"])
    else:
        # Synthetic per-event malware name — must NOT contain '-' so the
        # tag-prefix split below leaves a unique tag per event (otherwise
        # all 'Stealer-NNN' values collapse to a ghost 'malware:Stealer'
        # cluster, masquerading as a real Capability-dimension pattern).
        malware = (
            f"Stealer{idx:03d}{random.randint(100,999)}"
            if random.random() < 0.5
            else f"Backdoor{idx:03d}{random.randint(100,999)}"
        )

    # Pick infrastructure
    c2_ip = random.choice(cluster["shared_c2_ips"]) if cluster["shared_c2_ips"] else fake_ip()
    secondary_ip = fake_ip()
    domain = fake_domain(cluster.get("shared_domain_pattern", []),
                         cluster.get("shared_tld_pool", []), idx)
    sample_sha256 = fake_hash(f"{intrusion_set}|{malware}|{idx}")
    cert_sha256 = cluster["shared_cert_sha256"] or fake_hash(f"cert|{intrusion_set}|{idx}")[:64]
    jarm = cluster.get("shared_jarm")

    # Pick victim
    sector = random.choice(cluster["victim_sectors"])
    country = random.choice(cluster["victim_countries"])
    victim = fake_victim(sector, country, fixed=cluster.get("fixed_victim_org"))

    # Pick TTPs
    ttps = list(cluster.get("ttps", [])) or random.sample(
        ["T1059.001", "T1071.001", "T1566.001", "T1547.001", "T1041"], k=2)

    # Build attribute list
    attributes = [
        {"type": "ip-dst", "category": "Network activity", "value": c2_ip,
         "comment": f"C2 (cluster {cluster_id})", "to_ids": True},
        {"type": "ip-dst", "category": "Network activity", "value": secondary_ip,
         "comment": "secondary C2 / staging", "to_ids": True},
        {"type": "domain", "category": "Network activity", "value": domain,
         "comment": "C2 domain", "to_ids": True},
        {"type": "sha256", "category": "Payload delivery", "value": sample_sha256,
         "comment": f"{malware} sample", "to_ids": True},
        {"type": "x509-fingerprint-sha256", "category": "Network activity",
         "value": cert_sha256, "comment": "TLS cert SHA-256", "to_ids": False},
        {"type": "target-org", "category": "Targeting data", "value": victim["name"]},
        {"type": "target-location", "category": "Targeting data", "value": victim["country"]},
        {"type": "comment", "category": "External analysis",
         "value": f"Victim sector: {victim['sector']}; country: {victim['country']}"},
        {"type": "text", "category": "External analysis",
         "value": f"Threat actor (free-text): {intrusion_set}"},
        {"type": "text", "category": "External analysis",
         "value": f"Malware family: {malware}"},
    ]
    if jarm:
        attributes.append({
            "type": "jarm-fingerprint", "category": "Network activity",
            "value": jarm, "comment": "JARM fingerprint", "to_ids": False,
        })

    # Build tags
    tags = [
        {"name": "tlp:amber"},
        {"name": f"intrusion-set:{intrusion_set}"},
        {"name": f"malware:{malware.split('-')[0]}"},
        {"name": f"sector:{sector}"},
        {"name": f"country:{country}"},
        {"name": "demo:diamond-model-seed"},   # so the user can bulk-delete later
        {"name": f"demo:cluster-{cluster_id}"},
    ]
    for t in ttps[:3]:
        tags.append({"name": f"misp-galaxy:mitre-attack-pattern={t}"})

    return {
        "Event": {
            "info": info,
            "distribution": "0",   # Your org only — demo data, don't propagate
            "threat_level_id": "2",
            "analysis": "1",
            "published": False,
            "Attribute": attributes,
            "Tag": tags,
        }
    }


# --------------------------------------------------------------------------
# Cluster expansion → list of (intrusion_set, cluster_id, cluster, event_idx)
# --------------------------------------------------------------------------

def expand_plan(only_cluster=None):
    plan = []
    for cid, cdef in CLUSTERS.items():
        if only_cluster and cid != only_cluster:
            continue
        names = list(cdef["name_seed"])
        # Ensure unique names per event in cluster — extend if needed
        while len(names) < cdef["size"]:
            names.append(f"{cid}-Extra-{len(names)}")
        for i in range(cdef["size"]):
            plan.append((names[i], cid, cdef, i))
    if not only_cluster or only_cluster == "-":
        # singletons
        for i, name in enumerate(SINGLETON_NAMES):
            singleton_def = {
                "shared_malware": [], "shared_c2_ips": [], "shared_domain_pattern": [],
                "shared_tld_pool": [], "shared_cert_sha256": None,
                "victim_sectors": ["banking", "manufacturing", "tech-startup", "retail",
                                   "media", "logistics", "energy"],
                "victim_countries": ["US", "GB", "DE", "FR", "JP", "BR", "AU", "IN"],
                "ttps": ["T1059.001", "T1566.001", "T1071.001"],
                "summary": "isolated incident, no cluster signal",
            }
            plan.append((name, "-", singleton_def, i))
    return plan


# --------------------------------------------------------------------------
# MISP API
# --------------------------------------------------------------------------

def post_event(event_payload, insecure=False, dry_run=False):
    if dry_run:
        return {"dry_run": True, "Event": event_payload["Event"]}
    if not BASE_URL:
        sys.exit("MISP_URL not set")
    if not API_KEY:
        sys.exit("MISP_API_KEY not set")
    url = f"{BASE_URL}/events/add"
    body = json.dumps(event_payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": API_KEY,
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    ctx = None
    if insecure:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    try:
        with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
            txt = r.read().decode("utf-8", errors="replace")
            return json.loads(txt) if txt else {}
    except urllib.error.HTTPError as e:
        body_txt = e.read().decode("utf-8", errors="replace") if e.fp else ""
        sys.exit(f"HTTP {e.code} on POST /events/add: {body_txt[:500]}")
    except urllib.error.URLError as e:
        sys.exit(f"network error: {e.reason}")


def main():
    ap = argparse.ArgumentParser(description="Seed MISP with 100 demo events for Diamond-Model overlap discovery.")
    ap.add_argument("--insecure", action="store_true", help="skip TLS verify (self-signed MISP certs)")
    ap.add_argument("--dry-run", action="store_true", help="emit event JSON to stdout, don't POST")
    ap.add_argument("--limit", type=int, default=0, help="cap number of events (default: all)")
    ap.add_argument("--cluster", help="seed only this cluster (A..H, or '-' for singletons)")
    ap.add_argument("--rate-limit-ms", type=int, default=100,
                    help="sleep this many ms between POSTs (default 100)")
    args = ap.parse_args()

    plan = expand_plan(only_cluster=args.cluster)
    if args.limit:
        plan = plan[:args.limit]

    print(f"# plan: {len(plan)} events", file=sys.stderr)
    cluster_counts = {}
    for _, cid, _, _ in plan:
        cluster_counts[cid] = cluster_counts.get(cid, 0) + 1
    for cid in sorted(cluster_counts):
        print(f"#   cluster {cid}: {cluster_counts[cid]} events", file=sys.stderr)

    created = []
    failed = []
    for i, (intrusion_set, cid, cdef, idx) in enumerate(plan, 1):
        ev = build_event(intrusion_set, cid, cdef, idx)
        if args.dry_run:
            print(json.dumps(ev, indent=2))
            continue
        resp = post_event(ev, insecure=args.insecure, dry_run=False)
        evid = (resp.get("Event") or {}).get("id") if isinstance(resp, dict) else None
        if evid:
            created.append((evid, intrusion_set, cid))
            print(f"  [{i:3d}/{len(plan)}] cluster={cid} is={intrusion_set:32s} -> event id {evid}", file=sys.stderr)
        else:
            failed.append((intrusion_set, cid, str(resp)[:200]))
            print(f"  [{i:3d}/{len(plan)}] FAILED is={intrusion_set}: {resp}", file=sys.stderr)
        if args.rate_limit_ms > 0:
            time.sleep(args.rate_limit_ms / 1000.0)

    if args.dry_run:
        return

    print("\n# summary", file=sys.stderr)
    print(f"#   created: {len(created)}", file=sys.stderr)
    print(f"#   failed:  {len(failed)}", file=sys.stderr)
    if created:
        ids = [evid for evid, _, _ in created]
        print(f"#   event id range: {min(int(i) for i in ids)} – {max(int(i) for i in ids)}", file=sys.stderr)
    print(json.dumps({
        "summary": {
            "created": len(created),
            "failed": len(failed),
        },
        "created_events": [
            {"id": evid, "intrusion_set": is_, "cluster": cid}
            for evid, is_, cid in created
        ],
        "failed_events": [
            {"intrusion_set": is_, "cluster": cid, "error": err}
            for is_, cid, err in failed
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
