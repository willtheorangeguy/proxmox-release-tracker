# proxmox-release-tracker — Architecture

One Python script, one workflow, no dependencies beyond the standard library and the `gh` CLI.

```text
RSS feed  ->  parse  ->  derive tag  ->  does the release exist?  --yes-->  skip
                                                 |
                                                 no
                                                 v
                                        gh api ... POST /releases
```

## The script

`scripts/track_releases.py`, 136 lines, standard library only — `urllib.request` for the fetch,
`xml.etree.ElementTree` for the parse, `email.utils.parsedate_to_datetime` for the RFC 2822
dates. No `requests`, no `feedparser`.

| Function | Does |
|---|---|
| `fetch_rss` | `urllib.request.urlopen` with a 30-second timeout |
| `parse_rss` | Pulls `title`, `pubDate`, and `link` from each `<item>`; skips items missing a title or link |
| `make_tag` | Title to git tag |
| `pub_date_to_iso` | RFC 2822 to ISO 8601 in UTC, or `None` if it cannot parse |
| `release_exists` | `gh release view <tag>`, checking the exit code |
| `create_release` | `gh api repos/{owner}/{repo}/releases --method POST` |

## Tags are the deduplication key

There is no state file and no database. The tag derived from the title *is* the record that an
announcement has been seen: `release_exists` asks GitHub, and a tag that already exists is
skipped. Re-running the script is therefore free, and the workflow can run as often as it likes.

The cost is that the tag has to be stable. `make_tag` lowercases the title, strips a trailing
`released` or `released!`, replaces every run of non-alphanumeric characters with a hyphen, and
trims. If Proxmox retitles an announcement, or phrases one differently, the derived tag differs
and a second release appears for the same thing. That is also why the `available` suffix survives
on some tags and `released` does not — only one of the two is stripped. See
[`internal/known-issues.md`](./internal/known-issues.md).

## Why `--raw-field` for one argument

```python
raw_fields = {"make_latest": "false"}
```

The GitHub API wants `make_latest` as the *string* `"true"`, `"false"`, or `"legacy"`. The `gh`
CLI type-coerces `--field` values, turning `false` into a JSON boolean and getting a 422 back.
`--raw-field` sends it untouched. The comment in the source says as much, and it is the kind of
detail worth leaving written down.

Everything else — `tag_name`, `name`, `body`, `published_at` — goes through `--field`.

## Backdating

`published_at` is set from the feed's own `pubDate`, normalised to UTC. Without it every release
would carry the time the cron job ran, and the list would be ordered by when the tracker noticed
things rather than when Proxmox announced them.

## The workflow

`.github/workflows/track-releases.yml`: cron `0 */6 * * *` plus `workflow_dispatch`, Python 3.12,
`permissions: contents: write`, and `GH_TOKEN` from the built-in `secrets.GITHUB_TOKEN`. No
external actions beyond checkout and setup-python, and no secrets to manage.

`contents: write` is the minimum for creating releases, and the script needs nothing else.

## Failure behaviour

A failed fetch exits non-zero and the workflow run goes red. A failed release creation prints the
`gh` stderr and moves on to the next item, so one bad announcement does not block the rest. Both
are reasonable for a job that will run again in six hours.
