---
title: Plugin Developer Guide - Firefly Graph
description: Build datatype, widget, node, and utility plugins for Project Graph.
---

# Plugin Developer Guide

Project Graph is a platform for visual, node-based creative workflows. **Plugins** are the building blocks that power everything in the graph — from the data types that define how information flows, to the widgets that let users interact with data, to the nodes that perform computation and connect to services.

## The Plugin Ecosystem at a Glance

Every plugin in Project Graph falls into one of four types:

| Plugin Type | What It Does | Example |
|---|---|---|
| **Datatype** | Defines a data shape (number, string, image, vector, etc.) | `datatype-number`, `datatype-image`, `datatype-vector2` |
| **Widget** | Provides a UI for viewing and editing a datatype value | `widget-slider`, `widget-color`, `widget-textarea` |
| **Node** | Defines computation with typed input/output ports | `node-add-n-n`, `node-input-number`, `node-firefly-generate` |
| **Utility** | Provides shared code (functions, constants, web workers) imported by other plugins | `utility-math`, `utility-constants` |

Datatypes are the foundation. Widgets build on datatypes. Nodes bring them together into workflows. Utilities provide shared code that any other plugin type can import.

## Before You Begin

Make sure you have the following before starting:

* **Node.js** v22 or later — check your version with `node --version`
* **A package manager** — npm (ships with Node.js), pnpm, or Yarn all work
* **TypeScript** fundamentals — plugins are written in TypeScript
* **Graph CLI** — the build, dev, and publish tool for plugins. Download it from the [Adobe Developer Console](https://developer.adobe.com/console) (see [Creating Plugins](creating-plugins/index.md) for setup)
* **Adobe IMS credentials** — required for submitting plugins and accessing the plugin registry

## Guide Contents

This guide is organized into three groups by how each page relates to a platform version. Knowing which group a page belongs to tells you how current it is and how often it changes:

* **Concepts** are version-agnostic — principles and process that hold no matter which platform version you target.
* The **Plugin Development Guide** is the hands-on guide for the **current platform major**. It reflects the interface shapes of the current major; the guides for older majors remain available in the published version history.
* The **Platform Library Reference** is generated per platform **minor** and always resolves to the current release.

New here? Start with [Core Concepts](core-concepts/index.md), then [Creating Plugins](creating-plugins/index.md), and follow the Plugin Development Guide in order.

### Concepts (version-agnostic)

* **[Core Concepts](core-concepts/index.md)** — how the plugin system is architected. Covers the relationship between datatypes, widgets, and nodes; how plugins are loaded and resolved at runtime; and the lifecycle of data flowing through a graph. Read this before diving into implementation to avoid surprises later.
* **[How to Think About Nodes](how-to-think-about-nodes/index.md)** — the design philosophy behind building nodes that compose well with the broader ecosystem. Covers behavioral classifications (preview, control, operation nodes), streams vs. lists vs. values and when to use each, wicked types for polymorphic ports, categories and tags, port naming conventions, and the anti-patterns to avoid.
* **[Widget Design Guidelines](widget-design-guidelines/index.md)** — how to design widgets that look and feel right in the graph editor. Covers when to create a new widget vs. reuse an existing one, port widget sizing and container query behavior (including when widgets are hidden at narrow widths), node widget layout, CSS self-sizing patterns, and Spectrum design tokens.
* **[Plugin Versioning](plugin-versioning/index.md)** — how to version your own plugins. Covers the `<major>.<minor>` version field (no patch), when to bump major versus minor, and how versions relate to submitting your project.
* **[Platform Versioning](platform-versioning/index.md)** — how the Graph platform API is versioned and how plugins target it. Covers the `platformVersion` manifest field, per-plugin version targeting, and how the CLI resolves a separate bundle for each `major.minor`.
* **[Submitting Plugins](submitting-plugins/index.md)** — how to submit your plugin project for review and publish it to the plugin registry. Covers the submission flow, review criteria, channels, and what happens after your submission is approved.

### Plugin Development Guide (current major)

The hands-on guide for building against the current platform major. Older majors' guides are retained in the published version history.

* **[Creating Plugins](creating-plugins/index.md)** — how to set up a plugin project and build your first plugin from scratch. Covers project structure, the manifest format, and a step-by-step tutorial for creating a node. Includes reference material on adding more plugins, manifest schemas, and common pitfalls.
* **[Developing Datatypes](developing-datatypes/index.md)** — how to define the data shapes that flow through your graph. Covers intrinsic types, resource types (images, video, audio), and composite types built from existing datatypes. Explains when to create a new datatype vs. reuse one, how to design types for maximum widget composability, and the tags and naming conventions that keep the ecosystem consistent.
* **[Developing Widgets](developing-widgets/index.md)** — how to build Lit web components that view and edit datatype values. Covers the reactive signal API, display-only vs. editable widget patterns, multi-field widgets, Spectrum Web Components, and the difference between port widgets and node body widgets.
* **[Developing Nodes](developing-nodes/index.md)** — how to build computational nodes with typed input and output ports. Covers the `process` function, port configuration, persistent node scope, error handling, widget binding (both port-level and node body), the common node patterns (input, preview, output, processing, conversion, composition), external API access with `fetchSources`, and file structure.
* **[Developing Utilities](developing-utilities/index.md)** — how to build utility plugins that share reusable code across plugins. Covers the `createUtilityPlugin()` factory, multi-file utility structure, the `assets.exported` manifest format, and the web worker factory pattern using `new URL()`.
* **[CLI Reference](cli-reference/index.md)** — complete reference for all `graph` commands: `login`, `install`, `build`, `lint`, `format`, `dev`, and `submit`. Use this when you need to look up a specific flag or understand what a command does.

### Platform Library Reference (per-minor, auto-generated)

* **[Platform Library Reference](platform-versions/index.md)** — exactly which libraries and versions each platform release provides — Lit, Spectrum Web Components, the `@graph/*` packages, and the import paths available from each. One page per platform version, generated automatically on each platform minor; the index always points at the current (latest) release.

<InlineAlert variant="info" slots="text"/>

Need help? Reach out to the Graph team.

[//]: # (TODO: establish an externally reachable Graph team contact mechanism and link it here, then apply the same link to every "Reach out to the Graph team." help footer across these guide pages. The internal Slack channel was removed because external developers cannot access it.)
