---
title: Submitting Plugins - Firefly Graph
description: Submit your Graph plugin project for review and publish it to the plugin registry.
---

# Submitting Plugins

## Introduction

Once you've developed and tested your plugins locally, the next step is submitting them for review. This page covers the complete submission workflow.

With the Graph CLI, submission is **whole-project**: your entire plugin project — every plugin under `src/` — is packaged and submitted together as a single unit, identified by your project's `package.json` name and versioned by the registry **channel** you submit it to (for example `release` or `beta`).

## The Submission Workflow

The plugin submission process follows a clear, linear workflow:

```text
Develop → Test → Submit → Review → Available
```

1. **Develop** — Build and iterate locally with `graph dev`
2. **Test** — Validate your plugins work correctly in the Graph Editor
3. **Submit** — Package and upload your project with `graph submit`
4. **Review** — Your submission is set to "ProcessingPlugins" and queued for review
5. **Available** — Once approved, your plugins become available in the Graph Plugin Registry

## Submitting

```bash
graph submit --changelog "Fixed a bug with node evaluation order"
```

`graph submit` requires a `--changelog` (`-l`) describing what changed — it must be **10–500 characters**. There is no interactive prompt in this version of the CLI; if you omit `--changelog`, the command fails immediately with a validation error.

By default, submissions go to the `release` channel. To submit to a different channel (for example, to test a pre-release build), use `--channel` (`-c`):

```bash
graph submit --channel beta --changelog "Fixed a bug with node evaluation order"
```

A channel name must be **3–30 characters**, using only lowercase letters, digits, and hyphens.

<InlineAlert variant="warning" slots="text"/>

There is no way to submit only specific plugins, no `--status` flag to check submission state, and no `--force` / `--new-only` / `--skip-build` options in this version of the CLI. Every `graph submit` call packages and uploads your entire `src/` directory as one archive under your project's package name.

## What Gets Submitted

`graph submit` builds a ZIP archive directly from your project's `src/` directory, excluding `.plugin-dependencies/` and `.platform-dependencies/` (those are installed artifacts, not your source). The archive is identified by the `name` field in your project's `package.json`, which must follow the `@scope/package-name` convention (lowercase letters, digits, and hyphens only in each segment).

<InlineAlert variant="info" slots="text"/>

`submit` does not run `graph build` first and does not read from `dist/`. Make sure you've built and tested your plugins with `graph dev` or `graph build` before submitting, so you know the `src/` you're uploading actually works — the CLI does not verify that for you at submit time.

## Versioning with Channels

Older versions of the SDK versioned each plugin independently with a major/minor changelog prompt. The Graph CLI instead versions the **whole package** by the **channel** you submit to:

* **`release`** (the default) — your production channel. Use this for submissions you want available to consumers of your package.
* **Custom channels** (e.g. `beta`, `internal`) — use these to stage a build for testing before promoting it to `release`.

<InlineAlert variant="info" slots="text"/>

Channel semantics and promotion between channels are governed by the plugin registry, not the CLI. If you're unsure which channel to use, ask in the Graph team Slack channel below.

## Stage vs Production

For testing your submission workflow before going to production, use the stage environment:

```bash
# Submit to stage
GRAPH_SDK_ENV="stage" graph submit --changelog "Testing on stage"
```

Or export in your shell profile for persistent use:

```bash
export GRAPH_SDK_ENV="stage"
```

<InlineAlert variant="info" slots="text"/>

The stage environment has separate credentials and a separate registry. Use it to validate your submission process before publishing to production. See the [CLI Reference](../cli-reference/index.md#environment-configuration) for the full list of what `GRAPH_SDK_ENV` affects.

## Complete Example Workflow

Here's a realistic end-to-end scenario for submitting a plugin project:

```bash
# 1. Make your changes
# (edit src/node-add/plugin.ts, etc.)

# 2. Build and test locally
graph build
graph dev
# (verify in Graph Editor)

# 3. Submit the whole project to the release channel
graph submit --changelog "Improved number formatting"
```

## Troubleshooting

Common issues:

* **"Not authenticated"** — Run `graph login` first
* **Package name rejected** — Your `package.json` `name` field must follow `@scope/package-name`, using only lowercase letters, digits, and hyphens in each segment
* **"Changelog must be at least 10 characters" / "Changelog must be at most 500 characters"** — The value provided via `--changelog` is outside the 10–500 character range. Provide a more detailed description or shorten it.
* **Channel name rejected** — Channel names must be 3–30 characters, lowercase letters, digits, and hyphens only
* **"Package archive is empty"** — Nothing was found under `src/` to archive; make sure you're running `submit` from the project root and that `src/` contains your plugin directories
* **Submitting to the wrong environment** — Check the `GRAPH_SDK_ENV` value in your shell

<InlineAlert variant="info" slots="text"/>

**Need help?** Reach out to the Graph team in the [#prj-graph-plugins](https://adobe.enterprise.slack.com/archives/C0ANK4FL49W) Slack channel.
