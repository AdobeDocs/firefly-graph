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
* **pnpm** package manager
* **TypeScript** fundamentals — plugins are written in TypeScript
* **Graph CLI** — the build, dev, and publish tool for plugins. Install globally with `npm install -g @adobe/graph-cli`
* **Adobe IMS credentials** — required for submitting plugins and accessing the plugin registry

## Guide Contents

The sections below are ordered for a first-time reader. Follow them in sequence for the smoothest path from zero to a published plugin.

### 1. [Core Concepts](core-concepts/index.md)

How the plugin system is architected. Covers the relationship between datatypes, widgets, and nodes; how plugins are loaded and resolved at runtime; and the lifecycle of data flowing through a graph. Read this before diving into implementation to avoid surprises later.

### 2. [Creating Plugins](creating-plugins/index.md)

How to set up a plugin project and build your first plugin from scratch. Covers project structure, the manifest format, and a step-by-step tutorial for creating a node. Includes reference material on adding more plugins, manifest schemas, and common pitfalls.

### 3. [Developing Datatypes](developing-datatypes/index.md)

How to define the data shapes that flow through your graph. Covers intrinsic types, resource types (images, video, audio), and composite types built from existing datatypes. Explains when to create a new datatype vs. reuse one, how to design types for maximum widget composability, and the tags and naming conventions that keep the ecosystem consistent.

### 4. [Developing Widgets](developing-widgets/index.md)

How to build Lit web components that view and edit datatype values. Covers the reactive signal API, display-only vs. editable widget patterns, multi-field widgets, Spectrum Web Components, and the difference between port widgets and node body widgets.

### 5. [Widget Design Guidelines](widget-design-guidelines/index.md)

How to design widgets that look and feel right in the graph editor. Covers when to create a new widget vs. reuse an existing one, port widget sizing and container query behavior (including when widgets are hidden at narrow widths), node widget layout, CSS self-sizing patterns, and Spectrum design tokens.

### 6. [Developing Nodes](developing-nodes/index.md)

How to build computational nodes with typed input and output ports. Covers the `process` function, port configuration, persistent node scope, error handling, widget binding (both port-level and node body), the common node patterns (input, preview, output, processing, conversion, composition), external API access with `fetchSources`, and file structure.

### 7. [How to Think About Nodes](how-to-think-about-nodes/index.md)

The design philosophy behind building nodes that compose well with the broader ecosystem. Covers behavioral classifications (preview, control, operation nodes), streams vs. lists vs. values and when to use each, wicked types for polymorphic ports, categories and tags, port naming conventions, and the anti-patterns to avoid.

### 8. [Developing Utilities](developing-utilities/index.md)

How to build utility plugins that share reusable code across plugins. Covers the `createUtilityPlugin()` factory, multi-file utility structure, the `assets.exported` manifest format, and the web worker factory pattern using `new URL()`.

### 9. [CLI Reference](cli-reference/index.md)

Complete reference for all `graph` commands: `login`, `install`, `build`, `lint`, `format`, `dev`, and `submit`. Use this when you need to look up a specific flag or understand what a command does.

### 10. [Submitting Plugins](submitting-plugins/index.md)

How to submit your plugin project for review and publish it to the plugin registry. Covers the submission flow, review criteria, channels, and what happens after your submission is approved.

<InlineAlert variant="info" slots="text"/>

Need help? Reach out to the Graph team in the [#prj-graph-plugins](https://adobe.enterprise.slack.com/archives/C0ANK4FL49W) Slack channel.
