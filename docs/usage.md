# proxmox-release-tracker — Usage

## Subscribing

The point of the repository is the notification, and there is nothing to install.

**In the GitHub UI:** open the repository, click **Watch → Custom → Releases**. GitHub then
emails you whenever a new one appears.

**By feed:** GitHub publishes releases as Atom, so any reader works:

```text
https://github.com/willtheorangeguy/proxmox-release-tracker/releases.atom
```

That is often the better route — it is the original RSS use case, just with GitHub's uptime in
front of Proxmox's feed and with each entry already deduplicated.

## What a release looks like

| Field | Content |
|---|---|
| Tag | Derived from the title, lowercased and hyphenated — `proxmox-backup-server-4.2` |
| Name | The announcement title, verbatim |
| Body | A link to the full announcement, and the publication date |
| Date | Backdated to the announcement's own `pubDate`, not the time the job ran |

Backdating matters: it means the release list reads in the order Proxmox announced things, not
the order this tracker happened to notice them.

## Running it by hand

The workflow can be triggered from the **Actions** tab with **Run workflow**, which is the
quickest way to pick up an announcement without waiting for the next six-hourly run.

Locally:

```bash
gh auth login
python scripts/track_releases.py
```

It needs the `gh` CLI authenticated, and it creates releases in whatever repository the current
directory's git remote points at — the script passes `{owner}/{repo}` to `gh api` and lets the
CLI resolve it. Run it from a clone of this repository and nowhere else.

The script is safe to re-run: it checks whether each tag already exists and skips it. See
[Architecture](./architecture.md).

## Caveats worth knowing

**Not everything here is a release.** The Proxmox feed carries service notices and articles
alongside product announcements, and all of them become Releases.

**GitHub's "Latest release" is not the newest one.** Every release is created with
`make_latest=false`, so the pointer is stuck on an older entry. Read the list, not the badge.

Both are in [`internal/known-issues.md`](./internal/known-issues.md).
