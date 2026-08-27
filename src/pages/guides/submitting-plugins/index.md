---
title: Submitting Plugins - Firefly Graph
description: Submit your Graph plugin project for review and publish it to the plugin registry.
---

# Submitting Plugins

This page gets your project from your machine into the plugin registry. Submission is whole-project. You'll learn how `graph submit` packages everything at once, why the `--changelog` is required, how channels like `release` and `beta` version your work, and the difference between submitting to stage and production. A full worked example closes it out, plus troubleshooting for when a submit gets rejected.

## Introduction

The unit of submission is the **package** — your entire plugin project — not an individual plugin. When you run `graph submit`, the CLI zips up your `src/` tree, uploads it to the registry, and the registry unpacks it and queues every plugin inside for review. One command ships all of your datatypes, widgets, nodes, and utilities together, versioned by the **channel** you send them to.

Your package identity comes from the `name` field in `package.json`. It must be a scoped name like `@adobe/my-plugins`, using only lowercase letters, digits, and hyphens in each segment. The registry stores it in an encoded form: the leading `@` is dropped and the `/` becomes `_`, so `@adobe/my-plugins` is tracked as `adobe_my-plugins`.

## How Submission Works

Submission is a short pipeline. Most of it runs on the registry side after your upload lands:

```text
Develop → Test → Submit → Process → Review → Available
```

When you run `graph submit`, the CLI:

1. Validates your package name, channel name, and changelog before touching the network, so a typo fails fast with a clear message instead of a server error.
2. Zips your `src/` directory and computes a SHA-256 checksum of the resulting archive. The checksum is how the registry identifies this exact set of bytes.
3. Asks the registry to start an upload for that checksum on your target channel. The registry hands back a one-time upload URL — unless it already holds an archive with the same checksum, in which case it tells the CLI to skip the upload entirely.
4. Uploads the archive bytes to that URL (when step 3 asked it to).
5. Marks the upload complete. The package moves into the **ProcessingPlugins** state, where the registry unpacks the archive and processes each plugin it contains.

After that, the plugins go through review, and once approved they become available on the channel you submitted to.

<InlineAlert variant="info" slots="text"/>

Because the archive is identified by its checksum, re-running `submit` on an unchanged `src/` won't re-upload the same bytes — the registry recognizes the archive it already has and just re-runs the completion step. Change any source file and the checksum changes, which produces a new archive to upload.

## Submitting

```bash
graph submit --changelog "Fixed a bug with node evaluation order"
```

`graph submit` requires a `--changelog` (`-l`) describing what changed. It must be **10–500 characters**. There is no interactive prompt: if you omit `--changelog`, the command fails immediately before doing any work.

By default, submissions go to the `release` channel. To send a build somewhere else — for example, to stage a pre-release for testing — use `--channel` (`-c`):

```bash
graph submit --channel beta --changelog "Beta build of the new blend node"
```

<InlineAlert variant="warning" slots="text"/>

There is no way to submit only some plugins, and no `--status`, `--force`, `--new-only`, or `--skip-build` flags in this version of the CLI. Every `graph submit` packages and uploads your whole `src/` tree as one archive under your package name.

## What Gets Uploaded

The archive is built directly from your project's `src/` directory. It includes everything under `src/`, dotfiles and all, with two exceptions that are stripped out: `.plugin-dependencies/` and `.platform-dependencies/`. Those hold installed artifacts from `graph install`, not source you own, so they never belong in a submission.

The registry receives your **source**, taken straight from `src/`. It is not read from `dist/`.

<InlineAlert variant="info" slots="text"/>

`graph submit` does not run `graph build` for you. Build and test with `graph dev` or `graph build` first, so you know the `src/` you're uploading actually works — the CLI does not verify that at submit time.

## Channels and Versioning

Earlier versions of the SDK versioned each plugin on its own with a major/minor changelog prompt. The Graph CLI versions the **whole package** instead, keyed by the **channel** you submit to:

* **`release`** (the default) — your production channel. Use it for builds you want consumers of your package to get.
* **Custom channels** (for example `beta` or `internal`) — use these to stage a build for testing before you promote it to `release`.

Channel names must be **3–30 characters**, using only lowercase letters, digits, and hyphens.

<InlineAlert variant="info" slots="text"/>

Channel semantics — and how a build is promoted from one channel to another — are governed by the plugin registry, not the CLI. If you're unsure which channel to use, ask in the Graph team Slack channel below.

## Stage vs Production

To rehearse the submission flow before it counts, point the CLI at the stage environment with `GRAPH_SDK_ENV`:

```bash
GRAPH_SDK_ENV="stage" graph submit --changelog "Testing the submit flow on stage"
```

Or export it in your shell profile to make it stick for the session:

```bash
export GRAPH_SDK_ENV="stage"
```

<InlineAlert variant="info" slots="text"/>

Stage has separate credentials and a separate registry from production. Use it to validate your process end to end before publishing for real. See the [CLI Reference](../cli-reference/index.md#environment-configuration) for the full list of what `GRAPH_SDK_ENV` affects.

## Complete Example Workflow

A realistic end-to-end pass, from edit to submitted:

```bash
# 1. Make your changes
# (edit src/node-add/plugin.ts, etc.)

# 2. Build and test locally
graph build
graph dev
# (verify in the Graph Editor)

# 3. Submit the whole project to the release channel
graph submit --changelog "Improved number formatting"
```

To see which plugins the CLI finds in your project before you submit, run:

```bash
graph plugins
```

This version of the CLI has no command to poll a submission's review status. Track progress through the registry, or ask the Graph team.

## Troubleshooting

Common failures and what they mean:

* **"Not authenticated"** — Run `graph login` first.
* **Package name rejected** — The `name` in `package.json` must be a scoped name like `@adobe/my-plugins`, with only lowercase letters, digits, and hyphens in each segment. The CLI reports exactly which part is wrong (missing `@`, missing `/`, an empty segment, or the specific invalid character).
* **"Changelog must be at least 10 characters" / "Changelog must be at most 500 characters"** — Your `--changelog` is outside the 10–500 character range. Add detail, or trim it.
* **Channel name rejected** — Channel names must be 3–30 characters, lowercase letters, digits, and hyphens only.
* **"No src/ directory found ..."** — You're not at the project root, or the project has no `src/`. Run `submit` from the directory that holds your `package.json`.
* **"Package archive is empty ..."** — Nothing under `src/` made it into the archive. Confirm `src/` actually contains your plugin directories.
* **"Archive upload failed (HTTP ...)"** — The registry accepted the request but the storage upload failed. Check your network and retry; the checksum-based dedup means a retry won't create a duplicate.
* **Submitting to the wrong environment** — Check the `GRAPH_SDK_ENV` value in your shell.

<InlineAlert variant="info" slots="text"/>

**Need help?** Reach out to the Graph team in the [#prj-graph-plugins](https://adobe.enterprise.slack.com/archives/C0ANK4FL49W) Slack channel.
