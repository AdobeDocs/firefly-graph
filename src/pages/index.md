---
title: Overview - Firefly Graph
description: Build plugins for Project Graph — datatypes, widgets, nodes, and utilities — with the Graph CLI.
contributors:
  - https://github.com/AdobeDocs
---

<Superhero slots="heading, text"/>

# Firefly Graph Plugin Developer Guide

Project Graph is a platform for visual, node-based creative workflows. Plugins are the building blocks that power everything in the graph — from the data types that define how information flows, to the widgets that let users interact with data, to the nodes that perform computation and connect to services.

<Resources slots="heading, links"/>

#### Resources

* [Plugin Developer Guide](guides/index.md)
* [CLI Reference](guides/cli-reference/index.md)
* [Firefly Graph on GitHub](https://github.com/AdobeDocs/firefly-graph)

## The Plugin Ecosystem at a Glance

Every plugin in Project Graph falls into one of four types:

| Plugin Type | What It Does | Example |
|---|---|---|
| **Datatype** | Defines a data shape (number, string, image, vector, etc.) | `datatype-number`, `datatype-image`, `datatype-vector2` |
| **Widget** | Provides a UI for viewing and editing a datatype value | `widget-slider`, `widget-color`, `widget-textarea` |
| **Node** | Defines computation with typed input/output ports | `node-add-n-n`, `node-input-number`, `node-firefly-generate` |
| **Utility** | Provides shared code (functions, constants, web workers) imported by other plugins | `utility-math`, `utility-constants` |

Datatypes are the foundation. Widgets build on datatypes. Nodes bring them together into workflows. Utilities provide shared code that any other plugin type can import.

## Discover

<DiscoverBlock width="100%" slots="heading, link, text"/>

### Get Started

[Plugin Developer Guide](guides/index.md)

Start here for a guided path from zero to a published plugin — core concepts, your first plugin, and where to go deeper for each plugin type.

<DiscoverBlock slots="heading, link, text"/>

### Guides

[Creating Plugins](guides/creating-plugins/index.md)

Set up a plugin project and build your first node, step by step.

<DiscoverBlock slots="link, text"/>

[Developing Nodes](guides/developing-nodes/index.md)

Build computational nodes with typed input and output ports, widget bindings, and persistent state.

<DiscoverBlock slots="link, text"/>

[Submitting Plugins](guides/submitting-plugins/index.md)

Package and submit your plugins for review and publication to the Graph Plugin Registry.

<DiscoverBlock width="100%" slots="heading, link, text"/>

### Reference

[Graph CLI Reference](guides/cli-reference/index.md)

Complete reference for every `graph` command: `login`, `install`, `build`, `lint`, `format`, `dev`, and `submit`.

## Before You Begin

Make sure you have the following before starting:

* **Node.js** v22 or later — check your version with `node --version`
* **A package manager** — npm (ships with Node.js), pnpm, or Yarn all work
* **TypeScript** fundamentals — plugins are written in TypeScript
* **Graph CLI** — the build, dev, and publish tool for plugins. Install globally with `npm install -g @adobe/graph-cli`
* **Adobe IMS credentials** — required for submitting plugins and accessing the plugin registry

<InlineAlert variant="info" slots="text"/>

Need help? Reach out to the Graph team in the [#prj-graph-plugins](https://adobe.enterprise.slack.com/archives/C0ANK4FL49W) Slack channel.
