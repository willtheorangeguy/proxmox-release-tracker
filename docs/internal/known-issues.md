# Known Issues — proxmox-release-tracker

Concrete defects and gaps found while writing this repository's documentation in
August 2026. **Nothing here was changed** — each one needs a code, configuration, or
licensing decision rather than a documentation one.

Ordered by severity. See [`docs/roadmap.md`](../roadmap.md) for the narrative version,
which also covers deliberate non-goals.

**4 open:** 3 medium, 1 low.

## 1. The Latest release pointer is stuck two months behind

**Severity:** Medium
**Where:** `scripts/track_releases.py` -> `create_release`, `raw_fields`

**What:** Every release is created with `make_latest` set to the string `false`, unconditionally. GitHub therefore never moves the pointer when a newer release arrives. Checked against the live repository: `GET /releases/latest` returns Proxmox Virtual Environment 9.2, published 2026-05-21, while the newest release is Proxmox Mail Gateway 9.1 from 2026-07-29 -- and 24 releases exist in total.

**Why it matters:** The whole purpose of this repository is to be the thing people watch for Proxmox news, and the Latest badge is the first thing a visitor reads. It currently advertises a release two months old as the current one, which is the single most misleading thing the repository could say. Anyone checking whether they are up to date gets the wrong answer confidently.

The `make_latest=false` line is clearly deliberate -- there is a careful comment above it explaining the `--raw-field` workaround for the gh CLI type coercion -- so the value was chosen, probably to stop a backfill run from marking an old announcement as latest. The reasoning is sound; the consequence was not followed through.

**Suggested fix:** Pass `"legacy"` rather than `"false"`, which tells GitHub to work it out from the dates and is exactly right here given releases are backdated. Alternatively set `"true"` only when the item is the newest in the feed. Either way the existing pointer needs moving once by hand.

## 2. Only one of the two announcement suffixes is stripped from tags

**Severity:** Medium
**Where:** `scripts/track_releases.py` -> `make_tag`

**What:** The regex strips a trailing `released` or `released!` and nothing else. Proxmox also phrases announcements as `... available!` and `... (stable)`, which survive into the tag. The live release list shows all three shapes side by side: `proxmox-backup-server-4.2`, `proxmox-virtual-environment-9.2-available`, and `proxmox-datacenter-manager-1.0-stable`.

**Why it matters:** Tags are this repository primary artifact -- they are what a release URL contains and what anyone scripting against it would match on -- and they are inconsistent for reasons that have nothing to do with the product. The same product across two announcements can produce two differently shaped tags depending on the wording Proxmox chose that week, so there is no reliable way to parse a product and version back out.

It also interacts badly with the deduplication design: because the tag is the only record that an announcement was seen, any future change to this function republishes everything currently in the feed as duplicates. That makes the fix more delicate than it looks, which is worth knowing before someone treats it as a one-line change.

**Suggested fix:** Extend the pattern to strip `available`, `released`, and a trailing parenthesised word, all optional. Then rename the existing tags to match before merging, or accept and clean up the duplicate releases -- `docs/development.md` now spells out that sequence.

## 3. Announcements that are not releases are published as releases

**Severity:** Medium
**Where:** `scripts/track_releases.py` -> `main`; the Proxmox RSS feed

**What:** Every item with a title and a link becomes a GitHub Release. The Proxmox feed carries service notices and articles alongside product announcements, and both are in the published list: `Changed ip-addresses of shop.proxmox.com` and `Migrating to Proxmox VE` are Releases here, tagged `changed-ip-addresses-of-shop.proxmox.com` and `migrating-to-proxmox-ve`.

**Why it matters:** The repository description promises Proxmox releases tracked as GitHub Releases, and someone watching it for upgrade notifications gets pinged for an IP address change and a migration guide. Notification value degrades quickly with noise -- a feed that cries release for things that are not one stops being read carefully, which defeats the purpose of the repository existing.

A tag like `changed-ip-addresses-of-shop.proxmox.com` is also a strange permanent artifact to have created, since git tags are cheap to make and awkward to remove once anyone has fetched them.

**Suggested fix:** Require something release-shaped in the title before publishing -- a version number is the obvious test, and it correctly admits `Proxmox Datacenter Manager 1.0 (stable)` while rejecting both current false positives. Decide separately whether the notices should be dropped or surfaced some other way; dropping them is the simpler choice and matches what the description already claims.

## 4. Announcements older than the feed window are never picked up

**Severity:** Low
**Where:** `scripts/track_releases.py` -> `main`; `.github/workflows/track-releases.yml`

**What:** The script only ever sees what the RSS feed contains at the moment it runs, and there is no stored history -- the existence of a tag is the only record. The feed holds a limited window of recent items, so anything that scrolls off between runs is never seen, and nothing backfills. The six-hourly schedule makes that unlikely rather than impossible.

**Why it matters:** The gap is silent and permanent: a missed announcement leaves no trace anywhere, so nobody can tell the difference between a quiet period and a missed run. A GitHub Actions outage, a workflow disabled for inactivity -- which GitHub does to scheduled workflows in repositories with no recent pushes -- or a burst of announcements would each produce it. That last one is the realistic risk here, since this repository is deliberately low-activity.

**Suggested fix:** Low, because six hours against a feed that moves this slowly is a wide margin. If it matters, Proxmox publishes an announcements archive page that could be scraped once to backfill, and after that the schedule alone is enough. Worth also keeping an eye on the scheduled-workflow disabling, which is the more likely way this fails.

---

## Also, across every repository

**`.bandit` is present on disk but untracked in git.** Verified in PyWorkout, treklogger,
skyscanner-cli, booking-cli, piggy, and aibot — the config file exists locally in each but
`git ls-files` does not know about it, so none of it reached GitHub.

The August 2026 security sweep therefore looks complete locally and landed nowhere. Worth
checking across all 44 repositories it covered.
