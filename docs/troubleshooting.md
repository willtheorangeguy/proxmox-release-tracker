# proxmox-release-tracker — Troubleshooting

## An announcement is missing

**Check the feed still carries it.** The tracker only ever sees what is in the RSS feed at the
moment it runs. Proxmox's feed holds a limited window of recent items, so anything that scrolled
off before a run — an outage of more than six hours, say — is never picked up, and nothing
backfills it.

**Check the workflow ran.** The Actions tab shows every six-hourly run. A red run means the fetch
or the parse failed; the log has the error.

**Trigger it by hand.** Actions → Track Proxmox Releases → Run workflow.

## The same release appears twice

Two different titles produced two different tags. The tag is derived from the title, and there is
no other record that an announcement was seen, so a retitled or rephrased announcement is a new
release as far as the script is concerned.

Delete the duplicate release *and its tag* — leaving the tag behind means the entry will not be
recreated, which may or may not be what you want.

## The tag has `-available` on the end

`make_tag` strips a trailing `released` or `released!` but not `available`, so
"Proxmox VE 9.2 available!" becomes `proxmox-virtual-environment-9.2-available` while
"Proxmox Backup Server 4.2 released!" becomes `proxmox-backup-server-4.2`. Both forms exist in
the release list. Recorded in [`internal/known-issues.md`](./internal/known-issues.md).

## "Latest release" points at an old one

Every release is created with `make_latest=false`, so GitHub never moves the pointer. It is
currently stuck on Proxmox Virtual Environment 9.2 from May while newer releases exist.

Use the full release list, or the Atom feed, rather than the Latest badge. Also in
[`internal/known-issues.md`](./internal/known-issues.md).

## Something that is not a release appears as one

The Proxmox feed carries service notices and articles alongside product announcements —
"Changed ip-addresses of shop.proxmox.com" and "Migrating to Proxmox VE" are both in the list —
and the script publishes everything it finds. There is no filter.

## `gh` errors when running locally

`gh auth login` first. The script shells out to `gh release view` and `gh api`, and both need an
authenticated CLI. A `403` means the token lacks `contents: write` on the target repository.

## Running it locally published to the wrong repository

`gh api repos/{owner}/{repo}/...` resolves the placeholder from the current directory's git
remote. Run it from a clone of this repository, or the releases land wherever your remote points.

## The dates are wrong

Releases are backdated to the feed's own `pubDate`. If one shows the time the job ran instead,
`pub_date_to_iso` failed to parse that item's date and returned `None` — the release is still
created, just without the backdate.
