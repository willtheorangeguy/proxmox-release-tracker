# proxmox-release-tracker — Development

## Running it locally

```bash
gh auth login
python scripts/track_releases.py
```

Python 3.10 or newer — the script uses `str | None` annotations. No dependencies to install.

**It creates real releases.** `gh api repos/{owner}/{repo}/...` resolves the repository from the
current directory's git remote, so running it from a clone of this repository publishes to this
repository. There is no dry-run flag; if you want one, the change is to skip `create_release` and
print the arguments instead.

## Changing `make_tag` is the risky change

Tags are the deduplication key — there is no state file. Changing how a tag is derived means
every announcement in the current feed derives a *new* tag, does not match an existing release,
and gets published again as a duplicate.

If you change it:

1. Work out what the new tags would be for everything currently in the feed.
2. Rename the existing releases' tags to match, or accept the duplicates and delete them
   afterwards.
3. Only then merge.

The safest version of a rename is to make the new rule produce the same tags for everything
already published, and differ only for titles not seen yet.

## Testing a change without publishing

Point it at a scratch repository: clone this into a fresh repo with a different remote, or
temporarily replace `repos/{owner}/{repo}` with an explicit `owner/repo` you own. The `gh` CLI
resolves the placeholder from the remote, so the remote is the only thing that decides where
releases land.

There is no test suite. `make_tag` and `pub_date_to_iso` are both pure functions with docstring
examples, so they are the natural place to start if one is wanted.

## The workflow

`.github/workflows/track-releases.yml` runs every six hours and on demand. To change the
schedule, edit the cron; to test a change, push the branch and use **Run workflow** from the
Actions tab, which honours the branch you select.

`GH_TOKEN` is the built-in `secrets.GITHUB_TOKEN` with `contents: write`. Nothing needs
configuring, and there is no secret to rotate.

## Contributing

See the org-wide
[Contributing Guide](https://github.com/willtheorangeguy/.github/blob/main/CONTRIBUTING.md).

[`internal/known-issues.md`](./internal/known-issues.md) lists three real defects, of which the
`available` suffix and the stale "Latest" pointer are both small.
