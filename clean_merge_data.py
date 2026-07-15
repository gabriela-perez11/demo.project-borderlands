#!/usr/bin/env python3
"""
clean_merge_data.py
--------------------
Project Borderlands — Community Dashboard data pipeline.

What this does:
1. Reads raw_coalition_contacts.csv (real, messy source data pulled directly
   from the Project Borderlands proposal doc — inconsistent "Local?" values
   like "Yes?", "Maybe - PNW?", "No - Montana", free-text tag strings, blank
   handles, etc.)
2. Cleans/normalizes that data (locality status, region, tag lists, discovery
   channel).
3. Merges it with a second, separately-maintained data source — the
   structured "program" data (founding coalition members, local Indigenous
   partner orgs, Learning Lab pilot concepts, physical gathering locations,
   project goals) that lives in this script as PROGRAM_DATA.
4. Writes the combined, analysis-ready result to borderlands_data.json,
   which the dashboard (index.html) fetches and renders.

Run:
    python3 clean_merge_data.py
"""

import csv
import json
import re
from collections import Counter
from datetime import datetime, timezone

RAW_CSV_PATH = "raw_coalition_contacts.csv"
OUTPUT_JSON_PATH = "borderlands_data.json"


# ---------------------------------------------------------------------------
# Source 2: structured program data (would normally live in its own sheet /
# CMS — kept here as a plain dict so the whole pipeline runs standalone).
# ---------------------------------------------------------------------------
PROGRAM_DATA = {
    "founding_coalition": [
        {
            "name": "Gabi Perez",
            "role": "Founder",
            "org": "Project Borderlands",
            "bio_short": "Community organizer & storyteller weaving digital storytelling with place-based practice.",
        },
        {
            "name": "Stephanie Nestlerode",
            "role": "Systems Strategist",
            "org": "7th Generation Labs",
            "bio_short": "40+ years in organizational and civic transformation, guided by Indigenous wisdom teachings.",
        },
        {
            "name": "Tony Cladusbid",
            "role": "Coast Salish Knowledge Keeper",
            "org": "swədəbš Cultural Center / Beaver Tales Coffee",
            "bio_short": "Swinomish Native, Coast Salish canoe builder, artist, and storyteller.",
        },
        {
            "name": "Michelle Cladusbid",
            "role": "Community Weaver",
            "org": "swədəbš Cultural Center / Beaver Tales Coffee",
            "bio_short": "Holds space for allyship and creative gatherings rooted in humility and reciprocity.",
        },
    ],
    "local_orgs": [
        {"name": "sʷədəbš Cultural Center and Creative Hub", "location": "Coupeville, WA"},
        {"name": "The Swinomish Youth and Community Center", "location": "La Conner, WA"},
        {"name": "Children of the Setting Sun", "location": "Salish Sea region, WA"},
    ],
    # Overall size of the Coalition Space network. The detailed contact table
    # below only shows a handful of PLACEHOLDER sample entries (named after
    # native PNW flora/fauna) to demonstrate the data pipeline — this total
    # reflects the actual current size of the coalition.
    "total_coalition_members": 40,
    "coalition_note": "The Borderlands coalition currently has 40 members. The contact table below shows a small set of PLACEHOLDER sample entries (named after native Pacific Northwest flora and fauna) to demonstrate how the data pipeline structures and cleans contact data — it is not the full roster.",
    "learning_lab_pilot_concepts": [
        {"title": "Intergenerational Cooking Circles", "desc": "A Native grandmother and a non-Indigenous grandmother cook together and exchange ancestral food stories."},
        {"title": "Child-Led Storytelling Hikes", "desc": "Connect land, imagination, nature literacy, and place-based learning."},
        {"title": "Elder–Youth Roundtables", "desc": "Indigenous and non-Indigenous elders and youth share memory and relational knowledge across generations."},
        {"title": "Rewilding a Public Plot", "desc": "Community teams tend, observe, and document Indigenous planting methods over time."},
        {"title": "Animated Indigenous Legends", "desc": "Screenings of animated Indigenous stories followed by facilitated question circles for children and families."},
        {"title": "Youth-Designed Cultural Celebrations", "desc": "Youth-designed, adult-supported events centering cross-cultural exchange and joyful connection."},
    ],
    "physical_locations": [
        {"name": "Beaver Tales Coffee / swədəbš Cultural Center", "type": "Learning Lab host site", "lat": 48.2199, "lon": -122.6857},
        {"name": "Swinomish Youth and Community Center", "type": "Coalition partner", "lat": 48.3960, "lon": -122.4993},
        {"name": "Salish Sea Pilot Region", "type": "Program region", "lat": 48.3000, "lon": -122.6000},
    ],
    "digital_platforms": ["TikTok", "Instagram", "Facebook", "YouTube"],
    # PLACEHOLDER content performance numbers — filler demo data standing in
    # for real analytics once content is actually posted. Do not present
    # these as real metrics.
    "demo_content_metrics": [
        {"platform": "TikTok", "title": "Learning Lab teaser — Cooking Circle", "views": 1240, "likes": 310, "comments": 42, "shares": 58},
        {"platform": "Instagram", "title": "Elder-youth roundtable clip", "views": 860, "likes": 190, "comments": 21, "shares": 15},
        {"platform": "Facebook", "title": "Rewilding day recap", "views": 430, "likes": 75, "comments": 9, "shares": 22},
        {"platform": "YouTube", "title": "Full Learning Lab short documentary", "views": 2100, "likes": 340, "comments": 51, "shares": 40},
    ],
    "goals": [
        "Strengthen cross-cultural relationships",
        "Protect and uplift Indigenous knowledge and ways of knowing",
        "Use storytelling as a catalyst for transformation",
        "Build collective capacity for social and political action",
        "Regenerate connection to people, place, and land",
    ],
}


def normalize_locality(raw_value: str):
    """Turn messy free-text locality strings into a clean status + region."""
    if not raw_value or not raw_value.strip():
        return {"status": "unknown", "region": None}

    text = raw_value.strip()
    lowered = text.lower()

    if lowered.startswith("yes"):
        status = "confirmed_local"
    elif lowered.startswith("maybe"):
        status = "possibly_local"
    elif lowered.startswith("no"):
        status = "not_local"
    else:
        status = "unknown"

    # Pull a region string out of things like "No - Montana" / "Maybe - PNW?"
    region_match = re.split(r"[-?]", text, maxsplit=1)
    region = None
    if len(region_match) > 1:
        region = region_match[1].strip(" ?-") or None

    return {"status": status, "region": region}


CHANNEL_KEYWORDS = [
    ("tiktok", "TikTok"),
    ("facebook", "Facebook"),
    ("word of mouth", "Word of mouth"),
    ("monthly gathering", "Monthly gatherings"),
    ("coupeville arts center", "Coupeville Arts Center"),
    ("personal site", "Personal website"),
    ("website", "Personal website"),
]


def normalize_channel(raw_value: str):
    """Collapse free-text discovery channels (tiktok, facebook, word of mouth,
    monthly gatherings, Coupeville Arts Center, etc.) into a small set of
    clean categories."""
    if not raw_value or not raw_value.strip():
        return "unknown"
    lowered = raw_value.lower()
    for keyword, label in CHANNEL_KEYWORDS:
        if keyword in lowered:
            return label
    return raw_value.strip().title()


def parse_tags(raw_value: str):
    """Parse comma-separated role/skill tags, e.g. 'journalist, lawyer'."""
    if not raw_value:
        return []
    return [t.strip() for t in raw_value.split(",") if t.strip()]


def clean_coalition_contacts(csv_path: str):
    cleaned = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            locality = normalize_locality(row.get("local_raw", ""))
            channel = normalize_channel(row.get("found_via", ""))
            tags = parse_tags(row.get("tags_raw", ""))
            cleaned.append({
                "name": row.get("name", "").strip(),
                "handle": row.get("handle", "").strip() or None,
                "role": row.get("role", "").strip(),
                "about": row.get("about", "").strip(),
                "locality_status": locality["status"],
                "region": locality["region"],
                "discovery_channel": channel,
                "tags": tags,
            })
    return cleaned


def summarize_contacts(contacts):
    locality_counts = Counter(c["locality_status"] for c in contacts)
    channel_counts = Counter(c["discovery_channel"] for c in contacts)
    tag_counts = Counter(tag for c in contacts for tag in c["tags"])

    return {
        "total_contacts": len(contacts),
        "by_locality_status": dict(locality_counts),
        "by_discovery_channel": dict(channel_counts),
        "top_tags": [{"tag": tag, "count": count} for tag, count in tag_counts.most_common()],
    }


def main():
    contacts = clean_coalition_contacts(RAW_CSV_PATH)
    stats = summarize_contacts(contacts)

    merged = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "founding_coalition": PROGRAM_DATA["founding_coalition"],
        "local_orgs": PROGRAM_DATA["local_orgs"],
        "coalition_contacts": contacts,
        "coalition_stats": stats,
        "total_coalition_members": PROGRAM_DATA["total_coalition_members"],
        "coalition_note": PROGRAM_DATA["coalition_note"],
        "learning_lab_pilot_concepts": PROGRAM_DATA["learning_lab_pilot_concepts"],
        "physical_locations": PROGRAM_DATA["physical_locations"],
        "digital_platforms": PROGRAM_DATA["digital_platforms"],
        "demo_content_metrics": PROGRAM_DATA["demo_content_metrics"],
        "goals": PROGRAM_DATA["goals"],
    }

    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2)

    print(f"Cleaned {len(contacts)} coalition contacts.")
    print(f"Locality breakdown: {stats['by_locality_status']}")
    print(f"Top tags: {stats['top_tags']}")
    print(f"Wrote merged dataset -> {OUTPUT_JSON_PATH}")


if __name__ == "__main__":
    main()
