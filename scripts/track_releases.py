#!/usr/bin/env python3
"""Fetch the Proxmox RSS feed and create GitHub Releases for new entries."""

import re
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import timezone
from email.utils import parsedate_to_datetime

RSS_URL = "https://my.proxmox.com/index.php/en/announcements/rss"


def fetch_rss(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=30) as response:
        return response.read()


def parse_rss(xml_data: bytes) -> list[dict]:
    root = ET.fromstring(xml_data)
    channel = root.find("channel")
    if channel is None:
        return []

    items = []
    for item in channel.findall("item"):
        title = item.findtext("title", "").strip()
        pub_date = item.findtext("pubDate", "").strip()
        link = item.findtext("link", "").strip()
        if title and link:
            items.append({"title": title, "pub_date": pub_date, "link": link})
    return items


def make_tag(title: str) -> str:
    """Derive a valid git tag from an RSS item title.

    Examples
    --------
    "Proxmox Backup Server 4.2 released!"  -> "proxmox-backup-server-4.2"
    "Proxmox VE 8.4 released!"             -> "proxmox-ve-8.4"
    """
    tag = title.lower()
    # Strip trailing "released!" / "released" (with optional whitespace)
    tag = re.sub(r"\s+released!?\s*$", "", tag)
    # Replace any run of non-alphanumeric/dot characters with a single hyphen
    tag = re.sub(r"[^a-z0-9.]+", "-", tag)
    tag = tag.strip("-")
    return tag


def pub_date_to_iso(pub_date: str) -> str | None:
    """Convert an RFC 2822 date string to ISO 8601 (UTC)."""
    try:
        dt = parsedate_to_datetime(pub_date)
        # Normalise to UTC so the 'Z' suffix is always accurate.
        dt = dt.astimezone(timezone.utc)
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return None


def release_exists(tag: str) -> bool:
    result = subprocess.run(
        ["gh", "release", "view", tag],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def create_release(tag: str, title: str, body: str, published_at: str | None) -> bool:
    # Fields passed with --field are type-coerced by the gh CLI (booleans,
    # numbers, etc.).  The GitHub API requires make_latest to be a *string*
    # ("true", "false", or "legacy"), so it must be sent with --raw-field to
    # prevent the gh CLI from converting "false" into a JSON boolean.
    raw_fields: dict = {
        "make_latest": "false",
    }
    typed_fields: dict = {
        "tag_name": tag,
        "name": title,
        "body": body,
    }
    if published_at:
        typed_fields["published_at"] = published_at

    # Build the gh api arguments
    # The `{owner}/{repo}` placeholder is resolved automatically by the gh CLI
    # from the current repository's git remote configuration.
    cmd = ["gh", "api", "repos/{owner}/{repo}/releases", "--method", "POST"]
    for key, value in raw_fields.items():
        cmd += ["--raw-field", f"{key}={value}"]
    for key, value in typed_fields.items():
        cmd += ["--field", f"{key}={value}"]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  Error creating release '{tag}': {result.stderr.strip()}", file=sys.stderr)
        return False

    print(f"  Created release: {title}")
    return True


def main() -> None:
    print(f"Fetching RSS feed from {RSS_URL} …")
    try:
        xml_data = fetch_rss(RSS_URL)
    except Exception as exc:
        print(f"Failed to fetch RSS feed: {exc}", file=sys.stderr)
        sys.exit(1)

    items = parse_rss(xml_data)
    print(f"Found {len(items)} item(s) in the RSS feed.")

    for item in items:
        tag = make_tag(item["title"])
        print(f"\nChecking: {item['title']!r} (tag: {tag!r})")

        if release_exists(tag):
            print("  Already exists — skipping.")
            continue

        iso_date = pub_date_to_iso(item["pub_date"])
        body_lines = [f"[Read the full announcement]({item['link']})"]
        if item["pub_date"]:
            body_lines.append(f"\n**Published:** {item['pub_date']}")
        body = "\n".join(body_lines)

        create_release(tag, item["title"], body, iso_date)


if __name__ == "__main__":
    main()
