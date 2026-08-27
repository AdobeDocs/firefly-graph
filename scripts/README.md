# Scripts

Maintenance scripts for this documentation site.

## `gen-platform-pages.py`

Regenerates the **Platform Library Reference** pages under
`src/pages/guides/platform-versions/` — one page per platform version plus an index —
from the platform bundle output.

For each version it reads `platform-modules.json` from that version's
`graph-platform-exports-*.tgz` and lists every importable library, its version range, and
the exact import specifiers. `platform-modules.json` is the source of truth for what a
plugin can import; it is intentionally narrower than the full dependency closure (which
includes internal-only packages such as `@graph/logging` and `@graph/cache`).

### Usage

```bash
# Regenerate every version page + index from a full bundle directory (backfill):
python3 scripts/gen-platform-pages.py [BUNDLE_DIR]

# Generate a single version's page, then rebuild the index from all pages on disk:
python3 scripts/gen-platform-pages.py --version 2.18 [BUNDLE_DIR]
```

`BUNDLE_DIR` defaults to `$PLATFORM_BUNDLE_DIR`, then to
`~/platform-bundle-backfill/output-all`. It must contain one subdirectory per version
(e.g. `1.1`, `2.17`), each holding a `graph-platform-exports-*.tgz`.

The index is built from the version pages that exist on disk, so `--version` can add one
page without needing every other version's bundle present. The script overwrites the pages
it generates, so re-run it whenever a new platform version bundle is produced. Requires
Python 3 and `tar` on `PATH`; no third-party packages.

## `sync-platform-versions.py`

Detects platform versions that have been published to prod but don't yet have a
documentation page, and downloads each new version's `@graph/platform-exports` bundle so
`gen-platform-pages.py --version` can render it. Used by the **Check for new platform
version** workflow (`.github/workflows/check-platform-version.yml`), which runs it daily
and opens a PR when it finds anything new.

It reads the public, unauthenticated archival endpoints on `graph.adobe.com`
(`/graph/platform/major/<n>` and `/graph/platform/version/<v>/`, GRAPH-3604), walking each
major down from its latest minor until it reaches a version that already has a page.

### Usage

```bash
# Prints new version numbers (one per line) and downloads their bundles into BUNDLE_DIR:
python3 scripts/sync-platform-versions.py BUNDLE_DIR [--base-url URL]
```

Prints nothing when everything published is already documented. Stdlib only — no `tar` or
third-party packages needed (it only downloads the tarball; `gen-platform-pages.py` unpacks
it). Use `--base-url` to point at a non-prod endpoint for testing.
