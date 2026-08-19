<!-- Logo -->
<h1 align="center">proxmox-release-tracker</h1>

<!-- Tagline -->
<h4 align="center">Every Proxmox announcement published as a GitHub Release, so you can watch them the way you watch everything else.</h4>

<!-- Badges -->
<div align="center">
  <!-- Tracker -->
  <img alt="Track Releases State" src="https://github.com/willtheorangeguy/proxmox-release-tracker/actions/workflows/track-releases.yml/badge.svg">
  <!-- Issues -->
  <img alt="GitHub Issues" src="https://img.shields.io/github/issues/willtheorangeguy/proxmox-release-tracker">
  <!-- Pull Requests -->
  <img alt="GitHub Pull Requests" src="https://img.shields.io/github/issues-pr/willtheorangeguy/proxmox-release-tracker">
  <!-- License -->
  <img alt="License" src="https://img.shields.io/github/license/willtheorangeguy/proxmox-release-tracker">
</div>

<!-- Nav -->
<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#usage">Usage</a> •
  <a href="#installation">Installation</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#support">Support</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a>
</p>

Proxmox publishes announcements as an RSS feed and nothing else. This repository is the adapter: a scheduled job reads that feed and creates a GitHub Release for each new entry, so Proxmox news arrives through whatever already handles your GitHub notifications.

## Key Features

* Watch this repository's releases and get notified whenever Proxmox announces something.
* Releases are backdated to the announcement's own publication date, so the list reads in the order Proxmox published, not the order the job noticed.
* Tags are derived from titles and act as the deduplication key — there is no state file, and re-running is free.
* Runs every six hours on GitHub Actions, and on demand from the Actions tab.
* 136 lines of standard-library Python, no dependencies, no secrets beyond the built-in token.

## Usage

Click **Watch → Custom → Releases** on this repository, or point a feed reader at:

```
https://github.com/willtheorangeguy/proxmox-release-tracker/releases.atom
```

Each release carries the announcement title, a link to the full text on Proxmox's site, and the publication date. Nothing is mirrored — every release points back at the source.

Two things to know: not everything in the feed is a product release, since Proxmox mixes service notices in with them, and GitHub's "Latest release" badge is stuck on an older entry because every release is created with `make_latest=false`. Both are recorded in [`docs/internal/known-issues.md`](docs/internal/known-issues.md).

## Installation

Nothing to install to *use* it. To run the tracker yourself:

```bash
gh auth login
python scripts/track_releases.py
```

Python 3.10+ and an authenticated `gh` CLI. It creates real releases in whatever repository your git remote points at — there is no dry-run flag. [`docs/development.md`](docs/development.md) covers running it safely.

## Documentation

Full documentation lives in [`docs/`](docs/README.md):
[Usage](docs/usage.md) · [Architecture](docs/architecture.md) · [Development](docs/development.md) · [Troubleshooting](docs/troubleshooting.md) · [Roadmap](docs/roadmap.md)

## Support

File an [issue](https://github.com/willtheorangeguy/proxmox-release-tracker/issues/new/choose).

## Contributing

Contributions welcome. See the org-wide [Contributing Guide](https://github.com/willtheorangeguy/.github/blob/main/CONTRIBUTING.md) and [Code of Conduct](https://github.com/willtheorangeguy/.github/blob/main/CODE_OF_CONDUCT.md).

Note that tags are the deduplication key, so changing how they are derived republishes everything currently in the feed. [`docs/development.md`](docs/development.md) explains what to do about that.

## Credits

* [Proxmox Server Solutions GmbH](https://www.proxmox.com/) — the [announcements feed](https://my.proxmox.com/index.php/en/announcements/rss) this tracks.
* The [GitHub CLI](https://cli.github.com/), which does all the API work.

## License

MIT — see [`LICENSE.md`](LICENSE.md).

Not affiliated with, endorsed by, or sponsored by Proxmox Server Solutions GmbH. Announcement titles and links are reproduced from their public feed; the announcements themselves remain theirs.
