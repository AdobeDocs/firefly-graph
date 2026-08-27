#!/usr/bin/env python3
# © Copyright 2015-2020 Adobe. All rights reserved.
"""Find platform versions published to prod that have no documentation page yet.

For every new version it downloads that version's `@graph/platform-exports` tarball into a
local bundle directory, laid out as `BUNDLE_DIR/<major.minor>/graph-platform-exports-*.tgz`
so `gen-platform-pages.py --version <major.minor> BUNDLE_DIR` can turn it into a page. The
newly downloaded version numbers are printed to stdout, one per line (nothing is printed
when everything is already documented), which the CI workflow feeds into the generator.

Discovery uses the public, unauthenticated archival endpoints (GRAPH-3604) on
`graph.adobe.com` — deliberately un-gated because the bundle is only type declarations:
  - GET {BASE}/major/<n>                          302 -> .../version/<major.minor>
      the latest minor for that major (backed by a release-updated redirect table)
  - GET {BASE}/version/<v>/platform-closure.json  the per-version closure manifest
  - GET {BASE}/version/<v>/<tarball>              each closure package's tarball

Majors are walked upward from 1 until the major redirect 404s (this also surfaces a brand
new major). Within a major, minors are walked downward from the latest until one already
has a page — so a run that spans several new minors backfills all of them, while a
historical gap (e.g. the 2.2 that never shipped) 404s on the endpoint and is skipped.

The version number always comes from the endpoint *path*, never from a tarball filename:
the exports tarball keeps its own package version (e.g. graph-platform-exports-2.11.2.tgz
lives under version/2.17/), so the two must not be conflated.

Usage:
    python3 scripts/sync-platform-versions.py BUNDLE_DIR [--base-url URL]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.join(SCRIPT_DIR, "..", "src", "pages", "guides", "platform-versions")
DEFAULT_BASE_URL = "https://graph.adobe.com/graph/platform"
EXPORTS_PACKAGE = "@graph/platform-exports"


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Surface 3xx responses as HTTPError instead of following them.

    The `major` endpoint answers with a 302 whose Location names the latest minor; we need
    to read that Location rather than chase it to an S3 directory path that does not serve a
    document on its own.
    """

    def http_error_302(self, req, fp, code, msg, headers):
        raise urllib.error.HTTPError(req.full_url, code, msg, headers, fp)

    http_error_301 = http_error_303 = http_error_307 = http_error_308 = http_error_302


_no_redirect_opener = urllib.request.build_opener(_NoRedirect)


def latest_minor_for_major(base_url: str, major: int) -> int | None:
    """Return the latest published minor for a major, or None if the major does not exist."""
    url = f"{base_url}/major/{major}"
    try:
        _no_redirect_opener.open(url, timeout=30).close()
    except urllib.error.HTTPError as err:
        if err.code == 404:
            return None
        if err.code in (301, 302, 303, 307, 308):
            location = err.headers.get("Location", "")
            match = re.search(r"/version/(\d+)\.(\d+)", location)
            if not match:
                raise RuntimeError(f"unexpected redirect target for major {major}: {location!r}")
            return int(match.group(2))
        raise
    raise RuntimeError(f"expected a redirect from {url}, got a direct response")


def version_exists_on_endpoint(base_url: str, version: str) -> bool:
    """Return True if the endpoint serves a closure manifest for this version."""
    try:
        urllib.request.urlopen(f"{base_url}/version/{version}/platform-closure.json", timeout=30).close()
        return True
    except urllib.error.HTTPError as err:
        if err.code in (403, 404):
            return False
        raise


def download_exports_tarball(base_url: str, version: str, dest_dir: str) -> None:
    """Download a version's @graph/platform-exports tarball into dest_dir/<version>/."""
    with urllib.request.urlopen(f"{base_url}/version/{version}/platform-closure.json", timeout=30) as resp:
        closure = json.load(resp)
    entry = next((e for e in closure if e.get("name") == EXPORTS_PACKAGE), None)
    if entry is None:
        raise RuntimeError(f"{EXPORTS_PACKAGE} not found in closure for version {version}")
    tarball = entry["tarball"]
    out_dir = os.path.join(dest_dir, version)
    os.makedirs(out_dir, exist_ok=True)
    with urllib.request.urlopen(f"{base_url}/version/{version}/{tarball}", timeout=60) as resp:
        data = resp.read()
    with open(os.path.join(out_dir, tarball), "wb") as f:
        f.write(data)


def documented_versions() -> set:
    """Return the set of versions that already have a page on disk (e.g. {"2.17", "1.7"})."""
    if not os.path.isdir(PAGES_DIR):
        return set()
    return {
        name
        for name in os.listdir(PAGES_DIR)
        if re.fullmatch(r"\d+\.\d+", name)
        and os.path.isfile(os.path.join(PAGES_DIR, name, "index.md"))
    }


def find_new_versions(base_url: str, bundle_dir: str) -> list:
    """Download every published-but-undocumented version's bundle; return their numbers."""
    documented = documented_versions()
    new_versions = []
    major = 1
    while True:
        latest = latest_minor_for_major(base_url, major)
        if latest is None:
            break
        for minor in range(latest, 0, -1):
            version = f"{major}.{minor}"
            if version in documented:
                break
            if not version_exists_on_endpoint(base_url, version):
                continue
            download_exports_tarball(base_url, version, bundle_dir)
            new_versions.append(version)
        major += 1
    new_versions.sort(key=lambda v: tuple(int(p) for p in v.split(".")))
    return new_versions


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("bundle_dir", help="Directory to receive BUNDLE_DIR/<version>/*.tgz.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help=f"Default: {DEFAULT_BASE_URL}")
    args = parser.parse_args()

    os.makedirs(args.bundle_dir, exist_ok=True)
    new_versions = find_new_versions(args.base_url.rstrip("/"), args.bundle_dir)
    for version in new_versions:
        print(version)


if __name__ == "__main__":
    main()
