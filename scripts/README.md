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
python3 scripts/gen-platform-pages.py [BUNDLE_DIR]
```

`BUNDLE_DIR` defaults to `$PLATFORM_BUNDLE_DIR`, then to
`~/platform-bundle-backfill/output-all`. It must contain one subdirectory per version
(e.g. `1.1`, `2.17`), each holding a `graph-platform-exports-*.tgz`.

The script overwrites the generated pages, so re-run it whenever a new platform version
bundle is produced. Requires Python 3 and `tar` on `PATH`; no third-party packages.
