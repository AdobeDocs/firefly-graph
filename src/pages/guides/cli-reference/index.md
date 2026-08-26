---
title: CLI Reference - Firefly Graph
description: Complete reference for the Graph CLI — login, install, build, lint, format, dev, and submit.
---

# Graph CLI Reference

This is the lookup page for the `graph` CLI. Bookmark it. Every command is here: `login`, `install`, `build`, `lint`, `format`, `dev`, and `submit`, plus the global flags and how the CLI reads its environment config. Jump in when you need the exact flag or want to know what a command actually does.

## Introduction

The `graph` CLI is the primary tool for developing, building, testing, and publishing Graph plugins. It handles everything from local development with hot-reload to submitting your plugin project for review.

Whether you're creating nodes, widgets, datatypes, or utility plugins, `graph` provides a unified development experience with integrated build tooling, dependency management, and seamless integration with the Graph Plugin Registry.

## Installation

The Graph CLI is distributed through the [Adobe Developer Console](https://developer.adobe.com/console). Sign in with your Adobe ID, accept the Terms of Use, and download the CLI for your platform — it is not published to a public package registry.

Once the download is complete, verify the CLI is available on your `PATH`:

```bash
graph --version
```

The command it installs is `graph`. Before using registry commands such as `submit` and `install`, authenticate with Adobe IMS by running `graph login`.

## Global Options

These options apply to ALL `graph` commands and must appear BEFORE the subcommand:

| Option | Description |
|---|---|
| `-v, --verbose` | Enable verbose logging (debug level) |
| `--log-level <level>` | Set log level: `trace`, `debug`, `info` (default), `warning`, `error`, `fatal` |
| `--log-file <path>` | Write logs to a file (in addition to console output) |
| `-q, --quiet` | Suppress progress log output |

**Examples:**

```bash
graph --verbose build
graph --log-level debug submit --changelog "Fixed a bug"
graph --log-file ./graph-cli.log build
```

## Commands

### graph login

Authenticate with Adobe IMS and cache credentials. Required before using registry commands (`submit`, `install`).

Once authenticated, your credentials are cached locally and used automatically for subsequent commands until they expire.

| Option | Description |
|---|---|
| `-f, --force` | Force login even if existing credentials are still valid |

**Examples:**

```bash
graph login
graph login --force
```

### graph logout

Log out of Adobe IMS and clear cached credentials. Takes no options.

**Examples:**

```bash
graph logout
```

### graph plugins

List every plugin discovered in the current project (any directory under `src/` containing a `manifest.json`). For each plugin, prints its name, type, version, and platform version. Aliased as `graph plugin`. Takes no arguments or filtering options — it always lists the full project.

**Examples:**

```bash
graph plugins
graph plugin
```

### graph install

Install project plugins. Purges and recreates `.plugin-dependencies/` and `.platform-dependencies/` for the whole project, provisions the shared platform dependency bundle for each distinct `platformVersion` major.minor declared across your plugins, creates per-plugin symlinks to their declared dependencies, and writes each plugin's `tsconfig.json` and `eslint.config.mjs`. Always operates on every plugin in the project — there is no per-plugin filtering.

| Option | Description |
|---|---|
| `--bail` | Stop at the first plugin failure instead of continuing and reporting all failures |
| `--concurrency <number>` | Maximum number of plugins to process concurrently (default, and upper bound: number of CPUs minus 1) |
| `--graph-url <url>` | Base URL to download platform dependency bundles from (defaults to production) |

**Examples:**

```bash
graph install
graph install --bail
graph install --concurrency 4
graph install --graph-url https://stage.firefly.adobe.com
```

### graph build

Build project plugins. Scans `src/` for plugin directories, compiles TypeScript, generates `api-manifest.json`, and outputs to `dist/plugin-name/`. Always builds every plugin in the project — there is no per-plugin filtering.

| Option | Description |
|---|---|
| `--bail` | Stop at the first plugin failure instead of continuing and reporting all failures |
| `--concurrency <number>` | Maximum number of plugins to process concurrently (default, and upper bound: number of CPUs minus 1) |

**Examples:**

```bash
graph build
graph build --bail
graph build --concurrency 4
```

### graph lint

Lint plugins using the project's ESLint configuration. Always lints every plugin in the project — there is no per-plugin filtering.

<InlineAlert variant="warning" slots="text"/>

If your project has a custom `eslint.config.mjs`, you must add `eslint: 9.39.4` to `devDependencies` in your `package.json`. Without it, the command fails with: `ESlint v~9.39.0 required`.

| Option | Description |
|---|---|
| `--fix` | Automatically fix fixable lint errors |
| `--bail` | Stop at the first plugin failure instead of continuing and reporting all failures |
| `--concurrency <number>` | Maximum number of plugins to process concurrently (default, and upper bound: number of CPUs minus 1) |

**Examples:**

```bash
graph lint
graph lint --fix
graph lint --bail --concurrency 4
```

### graph format

Format project plugins with the project's formatter configuration. Always formats every plugin in the project — there is no per-plugin filtering.

| Option | Description |
|---|---|
| `--concurrency <number>` | Maximum number of plugins to process concurrently (default, and upper bound: number of CPUs minus 1) |

**Examples:**

```bash
graph format
graph format --concurrency 4
```

### graph dev

Start the development server with hot-reload. Watches source files, rebuilds changed plugins, and notifies connected clients via Server-Sent Events. This is the only build/serve command that accepts specific plugin names — the rest of the CLI always operates on the whole project.

The dev server provides a fast iteration cycle by automatically rebuilding plugins when you save changes and notifying the running Graph application to reload the updated plugins.

| Option | Description |
|---|---|
| `[plugins...]` | Plugin names to serve (builds and watches only these + their dependents). Omit to serve every local plugin. |
| `-p, --port <port>` | Dev server port (default: 3001) |
| `--graph-url <url>` | Base URL of the Graph application, used to generate the dev-mode link printed at startup (default: `http://localhost:5173`) |
| `--use-local` | Also serve and rebuild the named plugins' local dependencies, in addition to their dependents |

**Examples:**

```bash
# Start dev server for all plugins
graph dev

# Dev specific plugins only
graph dev @scope/node-add @scope/widget-slider

# Use a custom port
graph dev --port 4000

# Point the dev-mode banner at a different Graph app instance
graph dev --graph-url https://stage.firefly.adobe.com

# Also rebuild the named plugin's local dependencies
graph dev @scope/node-add --use-local
```

<InlineAlert variant="success" slots="text"/>

If you add new plugin directories while the dev server is running, you may need to restart it for the new plugins to be picked up.

### graph submit

Package the entire plugin project — everything under `src/`, excluding `.plugin-dependencies/` and `.platform-dependencies/` — into a single ZIP archive and submit it as one package to the Graph Plugin Registry. Unlike the older SDK, submission is **whole-project**, not per-plugin: your `package.json` `name` field (which must follow the `@scope/package-name` convention) identifies the package, and every plugin inside `src/` ships together as part of it.

| Option | Description |
|---|---|
| `-c, --channel <channel>` | Registry channel to submit to (default: `release`). 3–30 characters, lowercase letters, digits, and hyphens only. |
| `-l, --changelog <changelog>` | **Required.** Changelog describing what changed in this submission. Must be 10–500 characters. |

**Examples:**

```bash
graph submit --changelog "Fixed a bug with node evaluation order"
graph submit --channel beta --changelog "Fixed a bug with node evaluation order"
```

What happens during submission:

1. Validates the package name (from `package.json`), channel name, and changelog against the constraints above.
2. Archives `src/` into a ZIP file and computes its SHA-256 checksum.
3. Requests a pre-signed upload URL from the plugin service for that package + channel.
4. Uploads the archive to that URL (skipped if the server already has this exact archive content).
5. Finalizes the submission, transitioning the package to `ProcessingPlugins` for review.

<InlineAlert variant="info" slots="text"/>

This version of `submit` does not build your plugins first, does not prompt interactively for a major/minor change type, and has no `--status`, `--new-only`, `--force`, or `--skip-build` flags. Run `graph build` yourself beforehand to make sure `dist/` is current — the archive is built directly from `src/`, so a fresh build isn't required for `submit` to succeed, but your plugins should already be built and tested via `graph dev` before you submit.

## Environment Configuration

To target the **stage environment** instead of production, set the `GRAPH_SDK_ENV` environment variable:

```bash
# Per-command
GRAPH_SDK_ENV="stage" graph login
GRAPH_SDK_ENV="stage" graph submit --changelog "Testing on stage"

# Or export in your shell profile (.zshrc, .bashrc)
export GRAPH_SDK_ENV="stage"
```

<InlineAlert variant="info" slots="text"/>

The environment variable is still named `GRAPH_SDK_ENV` — it was not renamed as part of the CLI's rebrand to `graph`.

`GRAPH_SDK_ENV=stage` affects two things:

* **`graph login`** — authenticates against the stage IMS environment instead of production.
* **`graph submit`** — points the plugin registry client at the stage API instead of production.

The stage environment uses separate IMS credentials and a separate plugin service. Use it for testing submissions before publishing to production.

`graph install` and `graph dev` are configured independently, via the per-command `--graph-url` flag, rather than `GRAPH_SDK_ENV`:

* `graph install --graph-url <url>` — sets the base URL platform dependency bundles are downloaded from (defaults to the production Graph app).
* `graph dev --graph-url <url>` — sets the base URL used only to generate the dev-mode banner link printed at startup; it has no effect on where plugins are built or served from.

## Typical Development Workflow

Here's a typical workflow for developing and publishing Graph plugins:

1. **Install dependencies** — Run `pnpm install` to install project dependencies
2. **Authenticate** — Run `graph login` to authenticate with Adobe IMS (credentials are cached for future commands)
3. **Install plugin dependencies** — Run `graph install` to link plugin dependency types and provision platform bundles
4. **Start dev server** — Run `graph dev` to start the development server with hot-reload
5. **Develop and iterate** — Make changes to your plugins and see them automatically rebuilt and reloaded
6. **Final build** — Run `graph build` for a final production build
7. **Submit for review** — Run `graph submit --changelog "..."` to submit your plugin project for review

## Package Management

The `graph` CLI is designed to work alongside standard npm/pnpm package management workflows:

* Use `pnpm install` to install dependencies
* For running package scripts, use `pnpm run test`, `pnpm run lint`, etc.
* The `graph` CLI handles plugin-specific operations like installing, building, dev server, and submission

Your `package.json` can include scripts that delegate to `graph`:

```json
{
  "scripts": {
    "dev": "graph dev",
    "build": "graph build",
    "submit": "graph submit"
  }
}
```

<InlineAlert variant="success" slots="text"/>

**Next:** [Submitting Plugins](../submitting-plugins/index.md) — Build for production and submit your plugin project for review and publication.

<InlineAlert variant="info" slots="text"/>

**Need help?** Reach out to the Graph team in the [#prj-graph-plugins](https://adobe.enterprise.slack.com/archives/C0ANK4FL49W) Slack channel.
