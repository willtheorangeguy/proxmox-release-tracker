# proxmox-release-tracker — Roadmap

A small adapter that does one thing. Defects are in
[`internal/known-issues.md`](./internal/known-issues.md).

## Where it is

A 136-line standard-library script and a six-hourly workflow, with 24 releases published. No
dependencies, no state file, no secrets. Watching the repository, or its Atom feed, gets you
Proxmox announcements in whatever already handles your GitHub notifications.

## Considered

**Filtering announcements from releases.** The feed carries both, and everything becomes a
Release here. A rule as simple as requiring a version number in the title would separate them,
though it would also have to decide what happens to the notices — dropped, or published as
something other than a release.

**Normalising the tag suffixes.** `released` is stripped and `available` is not, so the same
product yields differently shaped tags depending on the wording Proxmox chose that day.

**Marking the newest release as latest.** `make_latest=false` on every release leaves the pointer
frozen. Passing `"true"` for the newest, or `"legacy"` throughout, would make the badge mean
something.

**A per-product view.** Proxmox ships VE, Backup Server, Mail Gateway, and Datacenter Manager,
and someone watching this repository gets all four. Labels on the releases, or separate
repositories, would let people follow one.

**Backfilling.** The feed is a window, so announcements older than it are simply absent. Proxmox
publishes an archive page; scraping it once would fill in the history.

**A dry-run flag.** There is no way to run the script without publishing, which makes changing
`make_tag` more nerve-wracking than it should be.

## Non-goals

**Mirroring downloads.** No ISOs, no packages, no repository mirroring. Every release links back
to Proxmox and that is the extent of it.

**Reproducing the release notes.** The body is a link and a date on purpose: copying Proxmox's
announcement text here would create a second copy that ages badly and answers to nobody.

**Watching other vendors.** The tag derivation, the feed URL, and the assumptions about titles
are all Proxmox-shaped. A general RSS-to-releases tool is a different project.

**A service.** It is a cron job in a repository, which is why it needs no infrastructure and no
secrets.
