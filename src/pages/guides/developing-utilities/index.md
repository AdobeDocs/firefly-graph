---
title: Developing Utilities - Firefly Graph
description: Build utility plugins that share reusable code across other plugins in Project Graph.
---

# Developing Utilities

## What is a Utility Plugin?

Utility plugins are shared code libraries for the Graph plugin ecosystem. Unlike datatypes, widgets, and nodes — which define data shapes, UI components, and computational units — utility plugins have **no runtime execution role**. They exist purely to export reusable TypeScript code (functions, constants, type guards, web worker factories) that other plugins import as dependencies.

Key characteristics:

* Export reusable functions, constants, type guards, or web worker factories
* No runtime execution — the platform never "runs" a utility plugin directly
* Other plugins declare them as dependencies and import from them at build time
* Can be multi-file: each `.ts` source file compiles to a separate bundle entry with its own `.d.ts` type declarations
* Created with `createUtilityPlugin()` from `@graph/platform-exports/v1/utility-plugin.js`

## When to Use a Utility Plugin

Create a utility plugin when:

* Two or more plugins share the same logic (math helpers, validation functions, formatting utilities)
* You want to define shared numeric constants or configuration values
* You need a reusable web worker factory that multiple nodes can instantiate
* You want clean type-safe abstractions that are tested independently of any specific node or widget

<InlineAlert variant="warning" slots="text"/>

**Avoid premature extraction.** If only a single plugin uses a piece of logic, keep it in that plugin. Utility plugins add an extra dependency and build artifact. Only extract to a utility plugin when the code is genuinely shared across multiple plugins.

## Project Structure

A utility plugin lives in its own directory under `src/`, following the same conventions as other plugin types:

```text
src/
└── utility-math/
    ├── manifest.json       ← declares type: "utility" and exported modules
    ├── plugin.ts           ← default export + re-exports of all public APIs
    ├── arithmetic.ts       ← one source file = one bundle entry
    └── constants.ts        ← another source file = another bundle entry
```

For a **single-file utility** (all code in `plugin.ts`), the manifest `assets.exported` can be an empty object. For **multi-file utilities**, each additional `.ts` file must be declared in `assets.exported`.

## The Manifest

A utility manifest differs from other plugin types in two ways: it must include `"type": "utility"` and an `"assets"` block that declares the exported modules.

### Single-file utility

```json
{
    "name": "@adobe/utility-math",
    "version": "1.0",
    "platformVersion": 1,
    "type": "utility",
    "assets": {
        "internal": {},
        "exported": {}
    },
    "dependencies": {}
}
```

### Multi-file utility

Each additional source file beyond `plugin.ts` must be listed in `assets.exported`. The key is the export name (used in import paths by consumers), and the value is the path to the compiled bundle:

```json
{
    "name": "@adobe/utility-math",
    "version": "1.0",
    "platformVersion": 1,
    "type": "utility",
    "assets": {
        "internal": {},
        "exported": {
            "arithmetic": "./arithmetic.js",
            "constants": "./constants.js"
        }
    },
    "dependencies": {}
}
```

Manifest field reference:

| Field | Required | Description |
|---|---|---|
| `type` | Yes | Must be `"utility"`. Identifies this as a utility plugin. |
| `assets.exported` | Yes | Maps export module names to their compiled `.js` bundle paths. Empty object `{}` for single-file utilities. |
| `assets.internal` | Yes | Internal assets not exported to consumers. Typically empty `{}` for utilities. |
| `dependencies` | Yes | Other plugins this utility depends on. Most utilities have no plugin dependencies. |

## Writing the Plugin

Every utility plugin must have a `plugin.ts` with a default export created by `createUtilityPlugin()`. This export provides the plugin metadata and signals to the CLI that this is a utility plugin.

```typescript
import { createUtilityPlugin } from "@graph/platform-exports/v1/utility-plugin.js";

// Named exports — these are the public API of your utility
export { clamp, lerp, remap } from "./arithmetic.js";
export { TAU, EPSILON } from "./constants.js";

// Default export — required for the CLI to recognize this as a utility plugin
export default createUtilityPlugin({
    displayName: "Math Utilities",
    description: "Shared math helpers and numeric constants for graph plugins",
    tags: ["math", "utility"]
});
```

The `createUtilityPlugin()` config accepts:

| Field | Required | Description |
|---|---|---|
| `displayName` | Yes | Human-readable name shown in the plugin registry |
| `description` | Yes | Short description of what this utility provides |
| `tags` | No | Tags for discoverability in the registry |

## Multi-file Utilities

For larger utilities, split code across multiple `.ts` files. Each file compiles to its own bundle entry with a separate `.d.ts` declaration file. This gives consumers fine-grained imports and keeps bundle sizes small.

The convention is to re-export all public APIs from `plugin.ts` so consumers can import from either the main entry or a specific module:

```typescript
// arithmetic.ts — a separate bundle entry
export function clamp(value: number, min: number, max: number): number {
    return Math.min(Math.max(value, min), max);
}

export function lerp(a: number, b: number, t: number): number {
    return a + (b - a) * t;
}
```

```typescript
// plugin.ts — main entry, re-exports everything for convenient top-level imports
import { createUtilityPlugin } from "@graph/platform-exports/v1/utility-plugin.js";

export { clamp, lerp } from "./arithmetic.js";
export { TAU, EPSILON } from "./constants.js";

export default createUtilityPlugin({
    displayName: "Math Utilities",
    description: "Shared math helpers",
    tags: ["math"]
});
```

<InlineAlert variant="info" slots="text"/>

**Always use `.js` extensions** in import paths even when referencing `.ts` source files. The TypeScript compiler and bundler resolve these correctly during the build.

## Using a Web Worker

Utility plugins can export web worker factories using the `new URL()` pattern. The bundler detects this pattern and emits the worker script as a separate chunk.

```typescript
// compute.ts — exported worker factory
export function createComputeWorker(): Worker {
    return new Worker(new URL("./worker.ts", import.meta.url), { type: "module" });
}
```

```typescript
// worker.ts — runs inside the Web Worker context
self.addEventListener("message", (event: MessageEvent<number>) => {
    const n = event.data;
    // ... perform computation ...
    self.postMessage(result);
});
self.postMessage("ready"); // signal that the worker is initialized
```

The worker factory pattern enables consuming nodes to spawn independent worker instances per invocation:

```typescript
// In a consuming node's process function:
import { createComputeWorker } from "@adobe/utility-compute/compute.js";

process: async (inputs) => {
    const worker = createComputeWorker();
    return new Promise((resolve) => {
        worker.addEventListener("message", (event) => {
            if (event.data === "ready") {
                worker.postMessage(inputs.value);
            } else {
                worker.terminate();
                resolve({ result: event.data });
            }
        });
    });
}
```

<InlineAlert variant="warning" slots="text"/>

**Declare the worker module in `assets.exported`.** The file containing the `new URL()` call (e.g. `compute.ts`) must be listed in `assets.exported`. The worker script itself (`worker.ts`) is automatically bundled as a dependency of that entry and does not need its own manifest declaration.

## Consuming a Utility Plugin

To use a utility plugin from another plugin:

**Step 1 — Declare the dependency in your manifest:**

```json
{
    "name": "@adobe/node-example",
    "version": "1.0",
    "platformVersion": 1,
    "dependencies": {
        "@adobe/datatype-number": { "majorVersion": 1 },
        "@adobe/utility-math": { "majorVersion": 1 }
    }
}
```

**Step 2 — Import from the utility in your plugin code:**

```typescript
// Import from the utility's main entry (plugin.ts re-exports everything)
import { clamp, lerp } from "@adobe/utility-math";

// Or import from a specific module entry declared in assets.exported
import { clamp } from "@adobe/utility-math/arithmetic.js";
import { TAU } from "@adobe/utility-math/constants.js";
```

After adding a new utility dependency, run `graph install` to link the dependency types so your editor and TypeScript can resolve them.

## Example: utility-helpers

The `@test/utility-helpers` plugin demonstrates a multi-file utility with three logical modules:

| File | Exports | Purpose |
|---|---|---|
| `plugin.ts` | Default export + re-exports all public APIs | Main entry point |
| `math.ts` | `clamp()`, `lerp()`, `remap()` | Numeric transformation functions |
| `validation.ts` | `isFiniteNumber()`, `isInRange()`, `assertRange()` | Type guards and range validation |
| `constants.ts` | `TAU`, `EPSILON`, `MAX_SAFE_VALUE` | Shared numeric constants |

```json
{
    "name": "@test/utility-helpers",
    "version": "1.0",
    "platformVersion": 1,
    "type": "utility",
    "assets": {
        "internal": {},
        "exported": {
            "math": "./math.js",
            "validation": "./validation.js",
            "constants": "./constants.js"
        }
    },
    "dependencies": {}
}
```

```typescript
// plugin.ts
import { createUtilityPlugin } from "@graph/platform-exports/v1/utility-plugin.js";

export { clamp, lerp, remap } from "./math.js";
export { isFiniteNumber, isInRange, assertRange } from "./validation.js";
export { TAU, EPSILON, MAX_SAFE_VALUE } from "./constants.js";

export default createUtilityPlugin({
    displayName: "Utility Helpers",
    description: "Shared math utilities, validation helpers, and numeric constants",
    tags: ["utility", "math", "helpers"]
});
```

## Example: utility-worker

The `@test/utility-worker` plugin demonstrates the web worker factory pattern. It exports a `createFactorialWorker()` function that spawns a worker to compute factorials off the main thread.

```json
{
    "name": "@test/utility-worker",
    "version": "1.0",
    "platformVersion": 1,
    "type": "utility",
    "assets": {
        "internal": {},
        "exported": {
            "compute": "./compute.js"
        }
    },
    "dependencies": {}
}
```

```typescript
// compute.ts
export function createFactorialWorker(): Worker {
    return new Worker(new URL("./worker.ts", import.meta.url), { type: "module" });
}
```

The consuming node (`node-factorial`) creates a worker per invocation, sends the input value, waits for the result, then terminates the worker.

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Missing `"type": "utility"` in manifest | Platform cannot identify plugin type; runtime error on load | Add `"type": "utility"` to `manifest.json` |
| Exported module not listed in `assets.exported` | Import from the module fails at runtime; module not bundled | Add an entry to `assets.exported` mapping the module name to its `.js` path |
| Stale dependency links after adding utility dependency | Editor cannot resolve imported types; TypeScript errors on import | Run `graph install` after adding or changing dependencies |
| Missing `.js` extension in import paths | Build failure or module resolution error | Always use `.js` extensions in TypeScript import paths (e.g. `./math.js`) |

<InlineAlert variant="success" slots="text"/>

**Next:** [CLI Reference](../cli-reference/index.md) — Complete reference for build, dev, and publish commands.

<InlineAlert variant="info" slots="text"/>

**Need help?** Reach out to the Graph team in the [#prj-graph-plugins](https://adobe.enterprise.slack.com/archives/C0ANK4FL49W) Slack channel.
