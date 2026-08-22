# proxmox-release-tracker — Documentation

Proxmox publishes announcements as an RSS feed and nothing else. GitHub can watch a repository's
releases and email you, or feed them into anything that speaks Atom. This repository is the
adapter between the two: a scheduled job reads the Proxmox feed and creates a GitHub Release for
each new entry.

Watch this repository's releases and you get a notification whenever Proxmox announces something.

```text
docs/
├── README.md            this index
├── usage.md             subscribing, and running the tracker by hand
├── architecture.md      the script, the workflow, and how duplicates are avoided
├── development.md       running it locally, and what to watch when changing tags
├── troubleshooting.md   why a release is missing, duplicated, or oddly named
├── roadmap.md           known gaps and deliberate non-goals
└── internal/
    └── known-issues.md  defects found while documenting (not fixed)
```

## What it does

Every six hours, `scripts/track_releases.py` fetches
`https://my.proxmox.com/index.php/en/announcements/rss`, derives a tag from each item's title,
and creates a GitHub Release for any tag that does not already exist. The release body links to
the full announcement and records the publication date.

## What it is not

It does not mirror packages, ISOs, or release notes — only the announcement titles, dates, and
links. Everything it publishes points back at Proxmox.

It also does not distinguish a product release from any other announcement: the feed carries
both, and everything in it becomes a Release here. See
[`internal/known-issues.md`](./internal/known-issues.md).
