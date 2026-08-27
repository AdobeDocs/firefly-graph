#!/usr/bin/env python3
# © Copyright 2015-2020 Adobe. All rights reserved.
"""Generate the Platform Library Reference pages under src/pages/guides/platform-versions/.

For each platform version bundle, this reads the authoritative `platform-modules.json`
(found inside that version's `graph-platform-exports-*.tgz`) and writes one Markdown page
listing every importable library, its version range, and the exact import specifiers a
plugin can use. It also writes an index page linking to every version.

`platform-modules.json` is the source of truth for what a plugin can import at a given
platform version — deliberately narrower than the full dependency closure, which includes
internal packages (e.g. @graph/logging, @graph/cache) that plugins cannot import.

Usage:
    python3 scripts/gen-platform-pages.py [BUNDLE_DIR]

BUNDLE_DIR defaults to $PLATFORM_BUNDLE_DIR, then to ~/platform-bundle-backfill/output-all.
It must contain one subdirectory per version (e.g. "1.1", "2.17"), each holding a
`graph-platform-exports-*.tgz`. Output is written relative to this script's location, so
the script can be run from anywhere.

Re-run this whenever a new platform version bundle is produced; it overwrites the pages.
"""

import glob
import json
import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(SCRIPT_DIR, "..", "src", "pages", "guides", "platform-versions")


def bundle_dir() -> str:
    if len(sys.argv) > 1:
        return os.path.expanduser(sys.argv[1])
    return os.path.expanduser(
        os.environ.get("PLATFORM_BUNDLE_DIR", "~/platform-bundle-backfill/output-all")
    )


def load_modules(base: str, version: str) -> dict:
    """Extract and parse platform-modules.json from a version's platform-exports tarball."""
    matches = glob.glob(os.path.join(base, version, "graph-platform-exports-*.tgz"))
    if not matches:
        raise FileNotFoundError(f"no graph-platform-exports-*.tgz in {os.path.join(base, version)}")
    raw = subprocess.run(
        ["tar", "-xzOf", matches[0], "package/platform-modules.json"],
        capture_output=True,
        check=True,
    ).stdout
    return json.loads(raw)["modules"]


def specifiers(name: str, exports: list) -> list:
    """Turn export subpaths into full import specifiers (e.g. "lit" + "./x.js" -> "lit/x.js")."""
    out = []
    for e in exports:
        if e == ".":
            out.append(name)
        elif e.startswith("./"):
            out.append(name + e[1:])
        else:
            out.append(name + "/" + e)
    return out


def version_key(v: str) -> tuple:
    major, minor = v.split(".")
    return (int(major), int(minor))


def write_version_page(base: str, version: str) -> None:
    major, minor = version.split(".")
    mods = load_modules(base, version)
    lines = [
        "---",
        f"title: Platform {version} Libraries - Firefly Graph",
        f"description: Libraries and import specifiers available to plugins targeting Graph platform version {version}.",
        "---",
        "",
        f"# Platform {version} — Available Libraries",
        "",
        f"This page lists every library a plugin can import when it targets Graph platform **{version}**. "
        f'To target this release, set `platformVersion` to `{{ "major": {major}, "minor": {minor} }}` in the plugin\'s manifest. '
        "Each library below is provided by the platform at runtime, so you import it directly — there's no need to add it to your project's dependencies. "
        "Versions are the ranges guaranteed available in this release.",
        "",
        "See [Platform Versioning](../../platform-versioning/index.md) for how targeting and runtime compatibility work, "
        "and the [reference index](../index.md) for the other platform versions.",
        "",
        "## Libraries",
        "",
    ]
    for name, info in mods.items():
        lines.append(f"### {name} — `{info.get('version', '')}`")
        lines.append("")
        lines.append("```text")
        lines.extend(specifiers(name, info.get("exports", [])))
        lines.append("```")
        lines.append("")
    os.makedirs(os.path.join(OUT_DIR, version), exist_ok=True)
    with open(os.path.join(OUT_DIR, version, "index.md"), "w") as f:
        f.write("\n".join(lines).rstrip() + "\n")


def write_index(versions: list, latest: str) -> None:
    lines = [
        "---",
        "title: Platform Library Reference - Firefly Graph",
        "description: The libraries and versions available to plugins at each Graph platform version.",
        "---",
        "",
        "# Platform Library Reference",
        "",
        "Every Graph platform release ships a fixed set of libraries your plugins can import directly at runtime — "
        "Lit, Spectrum Web Components, the `@graph/*` platform packages, and more. This reference shows exactly which "
        "libraries, and which versions, each platform release gives you. Pick a plugin's platform version by setting "
        "`platformVersion` in its manifest (see [Platform Versioning](../platform-versioning/index.md)), then use the "
        "matching page below to see what you can import.",
        "",
    ]
    majors: dict = {}
    for v in versions:
        majors.setdefault(v.split(".")[0], []).append(v)
    for maj in sorted(majors, key=int, reverse=True):
        lines.append(f"## Platform {maj}.x")
        lines.append("")
        for v in sorted(majors[maj], key=version_key, reverse=True):
            suffix = " — latest" if v == latest else ""
            lines.append(f"* [Platform {v}]({v}/index.md){suffix}")
        lines.append("")
    with open(os.path.join(OUT_DIR, "index.md"), "w") as f:
        f.write("\n".join(lines).rstrip() + "\n")


def main() -> None:
    base = bundle_dir()
    if not os.path.isdir(base):
        sys.exit(f"bundle directory not found: {base}")
    versions = sorted(
        (os.path.basename(p) for p in glob.glob(os.path.join(base, "*")) if os.path.isdir(p)),
        key=version_key,
    )
    if not versions:
        sys.exit(f"no version subdirectories found in {base}")
    latest = versions[-1]
    for v in versions:
        write_version_page(base, v)
    write_index(versions, latest)
    print(f"Generated {len(versions)} version pages + index (latest: {latest})")
    print(f"Output: {os.path.normpath(OUT_DIR)}")


if __name__ == "__main__":
    main()
