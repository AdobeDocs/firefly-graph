---
title: Platform Versioning - Firefly Graph
description: How the Graph platform API is versioned, how plugins target a version, and how the CLI resolves the matching bundle.
---

# Platform Versioning

By the end of this page you'll know what the `platformVersion` field in your manifest actually controls, how to pick a value for it, and what the CLI does with it behind the scenes. The short version: every plugin declares which release of the Graph platform API it was built against, and the CLI fetches a matching bundle for exactly that version. Two plugins in the same project can target two different platform versions without stepping on each other.

## The platformVersion Field

Every plugin manifest declares a `platformVersion`. It names the release of the Graph platform API — the types, base classes, and runtime your plugin builds against — that the plugin targets:

```json
{
  "name": "@adobe/node-add",
  "version": "1.0",
  "platformVersion": { "major": 2, "minor": 0 },
  "type": "node"
}
```

`platformVersion` is a `{ "major": <n>, "minor": <n> }` object. An older scalar form (a bare `1`) is still accepted for backward compatibility, but new plugins should use the object form.

## Major and Minor

The two parts carry different weight:

* **Major** changes when the platform makes a breaking change — an API is removed, a signature changes, or behavior shifts in a way that existing plugins can't absorb without edits.
* **Minor** changes when the platform adds something backward-compatible. A plugin on a higher minor may rely on additions that a lower minor doesn't have, so the minor is part of a plugin's compatibility contract, not just a label.

## One Version Per Plugin

`platformVersion` is set per plugin, not per project. Each plugin in your `src/` tree targets its own version, and plugins on different versions coexist in the same project. A stable node can sit on `2.0` while you develop a second node against `2.3` with newer capabilities — no global upgrade, no coordinated migration. Moving a plugin to a new platform version is a one-line change to its manifest.

## How the CLI Resolves a Version

When you run `graph install`, the CLI reads the `platformVersion` of every plugin it finds and provisions a platform bundle for each distinct `major.minor` in the project. The bundles land under `.platform-dependencies/`, one directory per exact version:

```text
.platform-dependencies/
├── 2.0/
└── 2.3/
```

Each directory is installed independently and holds its own `node_modules`. Plugins link to the directory for their own exact `major.minor`. Sharing a major does not mean sharing an install — `2.0` and `2.3` never share dependencies, which is what keeps two platform versions from conflicting inside one project.

<InlineAlert variant="info" slots="text"/>

This is why the platform packages don't belong in your project's `package.json`. `graph install` downloads them as versioned bundles keyed to each plugin's `platformVersion`, rather than resolving them as ordinary npm dependencies. See [Creating Plugins](../creating-plugins/index.md) for how a project is set up.

## Choosing a Version

Target the current stable platform version for new plugins. Bump a plugin's `platformVersion` when you want an API added in a later release, or when the platform ships a new major and you're ready to move. Because each bump is isolated to one plugin, you can upgrade one plugin at a time and leave the rest untouched.
