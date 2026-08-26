---
title: Developing Nodes - Firefly Graph
description: Build computational nodes with typed input and output ports in Project Graph.
---

# Developing Nodes

Nodes are where computation happens, and this is the deep dive. You'll build one from scratch, configure its input and output ports, and write the `process` function that turns inputs into outputs. From there it covers the harder parts: persistent per-node scope, error handling, binding widgets to ports, calling external APIs through `fetchSources`, and the handful of node patterns you'll reuse constantly. It's long. Keep it open while you work.

## 1. Introduction

Nodes are the computational building blocks of Project Graph workflows. Each node defines typed input and output ports, and a `process` function that transforms input data into output data. Nodes can also bind widgets to their ports for inline editing and display.

When you create a node plugin, you're defining:

* **Input ports** — what data the node receives
* **Output ports** — what data the node produces
* **Process function** — how the node transforms inputs into outputs
* **Widget bindings** (optional) — how the node displays and edits data in the UI
* **Lifecycle & state** (optional) — persistent per-node scope plus `init` / `shutdown` hooks for setup and teardown

## 2. Basic Node Example

Here's a complete working example of a simple node that adds two numbers together:

```typescript
import { createNodePlugin } from "@graph/platform-exports/node-plugin.js";

export default createNodePlugin({
    displayName: "Add Numbers",
    description: "Adds two numbers together",
    tags: ["category:math", "arithmetic", "add"],
    inputPorts: [
        { name: "a", type: "@adobe/datatype-number", displayName: "A", defaultValue: 0 },
        { name: "b", type: "@adobe/datatype-number", displayName: "B", defaultValue: 0 }
    ],
    outputPorts: [
        { name: "result", type: "@adobe/datatype-number", displayName: "Result" }
    ],
    process: async (inputs, _context) => {
        return { result: inputs.a + inputs.b };
    }
});
```

This node:

* Has two input ports (`a` and `b`) that accept numbers
* Has one output port (`result`) that produces a number
* Implements a `process` function that adds the two inputs together
* Uses the `@adobe/datatype-number` datatype for all ports

## 3. Port Configuration

Both input and output ports support the following configuration options:

| Property | Type | Required | Description |
|---|---|---|---|
| `name` | `string` | Yes | Internal identifier, used as key in inputs/outputs |
| `type` | `string` | Yes | Datatype reference (e.g., `"@adobe/datatype-number"`) |
| `displayName` | `string` | Yes | Human-readable label shown in the UI |
| `defaultValue` | varies | No | Default value when no connection is made |
| `description` | `string` | No | Tooltip/description text |
| `hidden` | `boolean` | No | Hide the port from the UI (used with nodeWidgetBinding) |
| `structure` | `("list" \| "stream")[]` | No | Declares the port carries a list or a stream instead of a single value (see [How to Think About Nodes](../how-to-think-about-nodes/index.md)) |
| `variadic` | `boolean` | No | Port accepts multiple connections, delivered as an array (see `PortError`'s `variadicIntegerIndex` in the Error Handling section) |
| `gateMode` | `"strict" \| "lenient" \| "optional"` | No | Runtime behavior for missing/undefined input values. Defaults to `"strict"`. `"optional"` allows execution even if the value is not set yet, `"lenient"` allows execution even if the value is dirty upstream on its connection. |
| `groupId` | `string` | No | Assigns the port to a port group defined in `portGroups` (see Port Groups below) |

<InlineAlert variant="info" slots="text"/>

Port names must be valid JavaScript identifiers. They become keys in the `inputs` and outputs objects, so use camelCase naming conventions.

### Port Groups

Related ports can be visually grouped in the UI. Declare the groups at the node level with `portGroups`, then reference a group's `id` from a port's `groupId`:

```typescript
export default createNodePlugin({
    displayName: "Adjust Color",
    description: "Adjusts brightness, contrast, and saturation of a color",
    tags: ["category:color", "adjust"],
    portGroups: [
        { id: "adjustments", displayName: "Adjustments", collapsed: true }
    ],
    inputPorts: [
        { name: "color", type: "@adobe/datatype-color", displayName: "Color" },
        { name: "brightness", type: "@adobe/datatype-number", displayName: "Brightness", defaultValue: 0, groupId: "adjustments" },
        { name: "contrast", type: "@adobe/datatype-number", displayName: "Contrast", defaultValue: 0, groupId: "adjustments" }
    ],
    outputPorts: [
        { name: "result", type: "@adobe/datatype-color", displayName: "Result" }
    ],
    process: async (inputs) => ({ result: adjustColor(inputs) })
});
```

A `PortGroupDefinition` has an `id`, a `displayName`, and an optional `collapsed` flag controlling whether the group starts collapsed in the UI. Ports without a `groupId` render ungrouped, as before.

### Breakpoints

Set `breakpoint: true` in the node config to mark it as a breakpoint for executions during graph authoring — the runtime pauses graph execution at this node so you can inspect its inputs and outputs before continuing. Use it sparingly, for nodes where mid-graph inspection genuinely helps debugging.

## 4. The Process Function

The `process` function is where your node's computational logic lives. It receives inputs and a context object, and returns outputs.

```typescript
process: async (inputs, context) => {
    // inputs: object with port names as keys, typed values
    // context provides, among others:
    //   context.scope - persistent per-node state (see Persistent Node Scope)
    //   context.abortSignal - fires when the runtime cancels this execution
    //   context.getToken(namespace, tokenName) - auth tokens (async — await it)
    //   context.resourceManager - resource CRUD operations
    //   context.reportProgress(0..1) - report execution progress
    return { outputPortName: computedValue };
}
```

### Inputs Object

The `inputs` parameter is an object where keys match your input port `name` values. For example, if you have input ports named `a` and `b`, you access them as `inputs.a` and `inputs.b`.

### Return Value

The return object keys must match your output port `name` values. The values must match the datatypes specified in your output port configurations.

### Async Operations

The function is async, so you can await API calls, resource operations, or any other asynchronous work.

### Context Object

The `context` parameter provides access to platform services:

* **context.scope** — Persistent per-node state that survives across executions (see the Persistent Node Scope section)
* **context.abortSignal** — An `AbortSignal` that fires when the runtime cancels this execution (pause or destroy); observe it in long-running loops and pass it to `fetch`
* **context.getToken(namespace, tokenName)** — Retrieve authentication tokens for external API calls (returns a `Promise` — `await` it)
* **context.resourceManager** — Create, read, update, and manage binary resources like images, files, etc.
* **context.reportProgress(progress)** — Report execution progress from `0.0` to `1.0` for the node's progress indicator

<InlineAlert variant="success" slots="text"/>

Keep your process function pure when possible — avoid side effects and make operations deterministic for better testing and caching. When a node genuinely needs to remember state between runs or reuse an expensive resource, use its **persistent scope** (see the Persistent Node Scope section) rather than module-level variables, which are disallowed in node plugin files because module state leaks across every invocation of the plugin.

### Reporting Token Cost

Nodes that call cost-bearing services (generative AI, paid APIs) can declare an optional `reportTokenCost` function alongside `process`:

```typescript
reportTokenCost: async (inputs, context) => {
    // context.signal is an AbortSignal — observe it to bail out of remote cost lookups
    const credits = await estimateCreditsFor(inputs.prompt, context.signal);
    return { firefly_credits: credits };
}
```

Key points:

* Runs **concurrently** with `process` — both must settle before the node's execution completes.
* For an iterating node, it fires once per iteration with that iteration's inputs.
* Receives a reduced context (`TokenCostContext`) with `nodeId`, `documentId`, `resourceManager`, `getToken`, and a `signal` — an `AbortSignal` that fires when the runtime no longer needs the cost result.
* Returns `TokenCostResults` — a small object of named cost fields, e.g. `{ firefly_credits: 5 }`.
* Providing `reportTokenCost` derives `tokenConsumer: true` on the published manifest; you never set that flag directly.

## 5. Persistent Node Scope

Every node has a persistent **scope** — a mutable, per-node object the runtime owns and hands to your node on *every* execution. Use it to keep state across runs (counters, caches) or to hold an expensive resource you build once and reuse (a 3D scene, a loaded model, a value generator).

Scope is established by an optional `init` method and torn down by an optional `shutdown` method. Inside `process`, you read and write it through `context.scope`. The value `init` returns both **creates** the scope and **defines its type**.

```typescript
import { createNodePlugin } from "@graph/platform-exports/node-plugin.js";

export default createNodePlugin({
    displayName: "Run Counter",
    description: "Counts how many times it has executed",
    tags: ["category:example", "stateful"],
    inputPorts: [
        { name: "trigger", type: "@adobe/datatype-number", displayName: "Trigger", defaultValue: 0 }
    ],
    outputPorts: [
        { name: "count", type: "@adobe/datatype-number", displayName: "Count" }
    ],
    // init runs ONCE, before the first process. Its return value both creates
    // the scope and defines its type as { runs: number }.
    init: () => ({ runs: 0 }),
    process: async (_inputs, context) => {
        context.scope.runs += 1; // typed as { runs: number } — no cast needed
        return { count: context.scope.runs };
    }
});
```

### Lifecycle Methods

| Method | When it runs | Receives | Returns | Use for |
|---|---|---|---|---|
| `init` | Once, when the node is added, before the first `process` | lifecycle context | the scope object (may be async) | Building reusable resources; defining the scope's type |
| `process` | Every execution | `inputs`, `context` (with `context.scope`) | output port values | Reading and mutating the scope |
| `shutdown` | Once, on true delete or runtime destroy | `scope`, lifecycle context | `void` (may be async) | Releasing what `init` / `process` allocated |

### Typing the Scope

Because the scope type is inferred from `init`'s return, `process` and `shutdown` see it fully typed with no cast. Three rules follow:

* A node that declares **no** `init` has no usable scope — touching `context.scope` is a compile error that directs you to add `init`. Nodes that never touch `context.scope` are unaffected.
* The scope shape is **closed** to `init`'s return: `process` cannot assign a wrong type or add undeclared fields. Declare every field in `init` — give values you populate later an initial `null` with an explicit return type.
* An `async` `init` is unwrapped — `process` sees the resolved scope, not a `Promise`.

### The Lifecycle Context

`init` and `shutdown` receive a *lifecycle* context, not the execution context. It carries node identity plus shared services (`resourceManager`, `getToken`, `canvasPool`) but **no** execution-scoped fields — there is no `abortSignal`, `reportProgress`, or `createMetadata`, because neither method is an execution.

### Lifecycle Guarantees

* Each node instance gets its **own independent** scope — even two nodes created from the same plugin.
* `init` runs exactly once and is awaited before the first `process`. If it rejects, the node surfaces an error and does not execute.
* Grouping a node into a subgraph (or ungrouping it) **preserves** the scope and its data — it is a re-parent, not a delete, so neither `init` nor `shutdown` runs.
* Only a true delete (or destroying the runtime) runs `shutdown` and drops the scope.
* Subgraph *container* nodes never receive the scope lifecycle.

<InlineAlert variant="warning" slots="text"/>

**Memoization skips unchanged runs.** If a node's inputs have not changed, the runtime may reuse the previous output and skip `process` entirely — so scope mutations (like a counter) happen only on runs that actually execute. Do not assume `process` runs once per graph run.

<InlineAlert variant="info" slots="text"/>

**Scope is in-memory only.** It is never serialized into the saved graph and does not survive a reload — an `init` / `shutdown` pair brackets a single runtime session. If a value must persist across reloads, store it in the document or an output port. Scope is also private to one node; it is not a channel for passing data between nodes.

## 6. Shuffling: Re-rolling Randomizable Ports

Some nodes have a *randomizable* input port — most commonly a `seed` — where the point of re-running the node is to draw a fresh value rather than reuse whatever is cached. The `shuffle` and `canShuffle` lifecycle methods define that re-roll behavior.

There is no separate "Shuffle" button in the UI. Instead, whenever `canShuffle` reports `true`, the runtime folds a "Run again" variant into the node's existing Run affordance; triggering it calls `shuffle` immediately before the next real execution.

<InlineAlert variant="warning" slots="text"/>

`shuffle` and `canShuffle` must be defined together. `createNodePlugin` throws at plugin-load time if only one of the two is provided.

### canShuffle — Is Shuffling Available?

`canShuffle` returns a reactive `ReadonlySignal<boolean>` indicating whether shuffling is currently available. It's commonly `false` when the randomizable port is wired to an upstream connection — there's nothing to re-roll because the value comes from elsewhere.

```typescript
canShuffle: inputPorts => computed(() => !inputPorts.seed.isConnected.get())
```

### shuffle — Re-rolling the Port

`shuffle` runs immediately before every real execution while `canShuffle` is `true`. Write a new value onto the port via `inputPorts.<name>.value.set(newValue)` — the write invalidates the runtime's output cache, making the node eligible to re-execute with the new value.

```typescript
shuffle: async inputPorts => {
    inputPorts.seed.value.set(Math.floor(Math.random() * 1_000_000));
}
```

### Shuffle Input Port Handles

Both methods receive typed handles for the node's input ports rather than raw values:

| Property | Type | Description |
|---|---|---|
| `value` | reactive signal (settable in `shuffle`) | Resolved value — connected upstream value or default override |
| `isConnected` | reactive boolean signal | True when an upstream connection drives this port |
| `isSettable` | reactive boolean signal | True when the port's default can be set — false if connected or bound elsewhere |

`canShuffle` receives read-only handles (no `.set()`); `shuffle` receives settable handles. Calling `.value.set()` on a port that isn't settable is a no-op.

### Shuffle Context

Both methods receive a lifecycle context — the same reduced context used by `init` and `shutdown`: node identity plus `resourceManager`, `getToken`, and `canvasPool`. There are no execution-scoped fields — no `abortSignal`, no `reportProgress` — because shuffling is a lightweight mutation, not a full execution.

### Reactive Signals

`signal`, `computed`, and the `ReadonlySignal` type used above are exported from the same module as `createNodePlugin`: `@graph/platform-exports/node-plugin.js`.

### Complete Example

```typescript
import { createNodePlugin, computed } from "@graph/platform-exports/node-plugin.js";

export default createNodePlugin({
    displayName: "Random Number",
    description: "Generates a random number from a re-rollable seed",
    tags: ["category:input", "number", "random"],
    inputPorts: [
        { name: "seed", type: "@adobe/datatype-number", displayName: "Seed", defaultValue: 0 }
    ],
    outputPorts: [
        { name: "value", type: "@adobe/datatype-number", displayName: "Value" }
    ],
    process: async inputs => ({ value: seededRandom(inputs.seed) }),
    // Re-roll the seed on every execution while it isn't driven by an upstream connection.
    shuffle: async inputPorts => {
        inputPorts.seed.value.set(Math.floor(Math.random() * 1_000_000));
    },
    canShuffle: inputPorts => computed(() => !inputPorts.seed.isConnected.get())
});
```

## 7. Error Handling

When your `process` function throws, the runtime catches the error and surfaces it in the graph editor. *How* you throw determines *where* the message appears and *what* text the user sees. Two typed error classes let you place a message precisely; both are imported from the same module as `createNodePlugin`.

```typescript
import { createNodePlugin, PortError, NodeError } from "@graph/platform-exports/node-plugin.js";
```

### Error Types at a Glance

| Throw | Where it appears | Message shown | When to use |
|---|---|---|---|
| `PortError` | On the named input port | Your message | The problem is attributable to a specific input |
| `NodeError` | On the node itself | Your message | A known error not tied to one port |
| `Error` (or any other throw) | On the node itself | `"An unexpected error has occurred"` — your text is hidden | Genuinely unexpected failures |

### PortError — Errors on a Specific Port

`PortError` attaches an error badge directly to an input port — the most helpful error for users because it points at exactly which input is wrong.

```typescript
process: async (inputs) => {
    if (inputs.prompt.trim() === "") {
        throw new PortError("prompt", "A non-empty prompt is required");
    }
    return { text: await generate(inputs.prompt) };
}
```

The constructor takes:

* **portName** — the `name` of the input port (must match one of your `inputPorts`).
* **message** — the human-readable text shown on the port.
* **variadicIntegerIndex** (optional) — for a variadic port, the array index of the offending element.

A variadic port delivers its values as an array. Pass the offending element's index as the third argument so the badge lands on that specific instance rather than the whole port:

```typescript
process: async (inputs) => {
    const numbers = inputs.numbers; // variadic → array of values
    for (let i = 0; i < numbers.length; i++) {
        if (numbers[i] < 0) {
            throw new PortError("numbers", "Negative values not allowed", i);
        }
    }
    return { result: numbers.reduce((a, b) => a + b, 0) };
}
```

### NodeError — Errors on the Node

`NodeError` puts a message on the node body rather than a port. Use it for known, describable problems that are not attributable to a single input — an invalid *combination* of inputs, an external service failure, or a configuration/state error. Its constructor takes a single **message** string.

```typescript
process: async (inputs) => {
    if (inputs.imageA.colorSpace !== inputs.imageB.colorSpace) {
        throw new NodeError("Cannot blend images with different color spaces");
    }
    return { result: blend(inputs.imageA, inputs.imageB) };
}
```

### Regular Errors — Unexpected Failures

Any other throw — a plain `Error` or a library exception — shows the generic `"An unexpected error has occurred"` on the node, and **your message is hidden**. This is intentional: it prevents leaking stack traces or internal details to users. Reserve plain throws for genuinely unexpected bugs; whenever you can describe the failure, use `PortError` or `NodeError` instead.

<InlineAlert variant="info" slots="text"/>

**Messages clear automatically.** The runtime clears port and node messages at the start of every execution attempt and when the node is removed — you never clear them manually. An errored node also holds up its downstream nodes until the cause is resolved (fixed inputs, a re-run, or removal), so throw only when the node genuinely cannot produce output.

## 8. Widget Binding

Widget binding is one of the most important concepts in node development. There are **two separate binding mechanisms**:

### portWidgetBinding — Inline Port Widgets

Renders a widget inline next to a specific input port. Used for editing input values when no upstream connection exists.

```typescript
portWidgetBinding: (inputs, _outputs) => {
    return {
        inputPorts: {
            a: {
                type: "@adobe/widget-number",
                data: { value: inputs.a }
            },
            b: {
                type: "@adobe/widget-number",
                data: { value: inputs.b }
            }
        }
    };
}
```

Key characteristics:

* Returns an object with `inputPorts` key
* Each key under `inputPorts` matches an input port name
* Widget only appears when the port has no incoming connection
* Used for inline value editing

### nodeWidgetBinding — Node Body Widgets

Renders a widget on the node body, separate from any port. Used for prominent displays like previews, large text areas, image thumbnails. Returns an **array** of widget bindings.

```typescript
nodeWidgetBinding: (inputs, _outputs) => {
    return [
        {
            type: "@adobe/widget-textarea",
            data: { value: inputs.value }
        }
    ];
}
```

Key characteristics:

* Returns an **array** of widget configurations
* Can bind to either `inputs` or `outputs`
* Always visible on the node body
* Used for prominent displays and previews

<InlineAlert variant="info" slots="text"/>

**Key distinction:** `portWidgetBinding` maps widgets to input ports for inline editing. `nodeWidgetBinding` displays widgets on the node body and can bind to either inputs or outputs.

## 9. Node Patterns

The following patterns cover the most common node use cases. Each pattern demonstrates a specific combination of ports, widgets, and processing logic.

### Input Node

An input node provides a constant or user-editable value to the graph. It has a hidden input port for storing the value, a node-level widget for editing, and an output port for downstream nodes.

```typescript
export default createNodePlugin({
    displayName: "Number Input",
    description: "Provides a number value to the graph",
    tags: ["category:input", "number"],
    inputPorts: [
        { name: "value", type: "@adobe/datatype-number", displayName: "Value", defaultValue: 0, hidden: true }
    ],
    outputPorts: [
        { name: "value", type: "@adobe/datatype-number", displayName: "Value" }
    ],
    nodeWidgetBinding: (inputs, _outputs) => [
        { type: "@adobe/widget-number", data: { value: inputs.value } }
    ],
    process: async (inputs) => ({ value: inputs.value })
});
```

Pattern characteristics:

* Hidden input port stores the editable value
* Node widget binds to the input for prominent editing
* Output port passes the value downstream
* Process function is a simple passthrough

### Preview Node

A preview node displays a value on the node body while passing it through unchanged to downstream nodes. The widget binds to the *output* to show the processed result.

```typescript
export default createNodePlugin({
    displayName: "Number Preview",
    description: "Displays a number value",
    tags: ["category:preview", "number"],
    inputPorts: [
        { name: "value", type: "@adobe/datatype-number", displayName: "Value" }
    ],
    outputPorts: [
        { name: "value", type: "@adobe/datatype-number", displayName: "Value" }
    ],
    nodeWidgetBinding: (_inputs, outputs) => [
        { type: "@adobe/widget-number", data: { value: outputs.value } }
    ],
    process: async (inputs) => ({ value: inputs.value })
});
```

Pattern characteristics:

* Input port receives the value to display
* Node widget binds to the **output** to show the result
* Output port passes the value downstream
* Process function is a simple passthrough

### Output Node

An output node provides both inline port editing and a prominent node body display. It uses both widget binding mechanisms and typically has a hidden output port since it's a terminal node.

```typescript
export default createNodePlugin({
    displayName: "Number Output",
    description: "Displays and outputs a number value",
    tags: ["category:output", "number"],
    inputPorts: [
        { name: "value", type: "@adobe/datatype-number", displayName: "Value", defaultValue: 0 }
    ],
    outputPorts: [
        { name: "value", type: "@adobe/datatype-number", displayName: "Value", hidden: true }
    ],
    portWidgetBinding: (inputs, _outputs) => ({
        inputPorts: {
            value: {
                type: "@adobe/widget-number",
                data: { value: inputs.value }
            }
        }
    }),
    nodeWidgetBinding: (inputs, _outputs) => [
        { type: "@adobe/widget-number", data: { value: inputs.value } }
    ],
    process: async (inputs) => ({ value: inputs.value })
});
```

Pattern characteristics:

* Both port widget and node widget bind to `inputs.value`
* Port widget provides inline editing when disconnected
* Node widget provides prominent display
* Output port is hidden since this is typically a terminal node

### Processing Node

A processing node performs computation on its inputs. Port widgets provide inline editing, and the process function contains the computational logic. The "Add Numbers" example from section 2 is a perfect example of this pattern.

```typescript
export default createNodePlugin({
    displayName: "Add Numbers",
    description: "Adds two numbers together",
    tags: ["category:math", "arithmetic", "add"],
    inputPorts: [
        { name: "a", type: "@adobe/datatype-number", displayName: "A", defaultValue: 0 },
        { name: "b", type: "@adobe/datatype-number", displayName: "B", defaultValue: 0 }
    ],
    outputPorts: [
        { name: "result", type: "@adobe/datatype-number", displayName: "Result" }
    ],
    portWidgetBinding: (inputs, _outputs) => ({
        inputPorts: {
            a: { type: "@adobe/widget-number", data: { value: inputs.a } },
            b: { type: "@adobe/widget-number", data: { value: inputs.b } }
        }
    }),
    process: async (inputs, _context) => {
        return { result: inputs.a + inputs.b };
    }
});
```

Pattern characteristics:

* Multiple input ports with port widgets for inline editing
* Process function contains computational logic
* Output port(s) expose computed results
* No node widget needed — the computation is the focus

### Conversion Node

A conversion node transforms data from one type to another. Input and output ports have different datatypes.

```typescript
export default createNodePlugin({
    displayName: "Number to String",
    description: "Converts a number to its string representation",
    tags: ["category:conversion", "number", "string"],
    inputPorts: [
        { name: "value", type: "@adobe/datatype-number", displayName: "Number" }
    ],
    outputPorts: [
        { name: "result", type: "@adobe/datatype-string", displayName: "String" }
    ],
    process: async (inputs) => ({ result: String(inputs.value) })
});
```

Pattern characteristics:

* Single input of one datatype
* Single output of a different datatype
* Process function performs type conversion
* Often tagged with `category:conversion`

### Composition Node

A composition node combines multiple simple inputs into a single complex output. This is useful for creating structured data from primitives.

```typescript
export default createNodePlugin({
    displayName: "Create Vector2",
    description: "Creates a 2D vector from X and Y components",
    tags: ["category:math", "vector2", "compose"],
    inputPorts: [
        { name: "x", type: "@adobe/datatype-number", displayName: "X", defaultValue: 0 },
        { name: "y", type: "@adobe/datatype-number", displayName: "Y", defaultValue: 0 }
    ],
    outputPorts: [
        { name: "vector", type: "@adobe/datatype-vector2", displayName: "Vector2" }
    ],
    portWidgetBinding: (inputs, _outputs) => ({
        inputPorts: {
            x: { type: "@adobe/widget-number", data: { value: inputs.x } },
            y: { type: "@adobe/widget-number", data: { value: inputs.y } }
        }
    }),
    process: async (inputs) => ({ vector: { x: inputs.x, y: inputs.y } })
});
```

Pattern characteristics:

* Multiple primitive input ports
* Single complex/structured output port
* Process function assembles the structure
* Often tagged with `compose`

### Decomposition Node

A decomposition node extracts multiple simple outputs from a single complex input. This is the inverse of a composition node.

```typescript
export default createNodePlugin({
    displayName: "Vector2 Properties",
    description: "Extracts X and Y components from a 2D vector",
    tags: ["category:math", "vector2", "decompose"],
    inputPorts: [
        { name: "vector", type: "@adobe/datatype-vector2", displayName: "Vector2" }
    ],
    outputPorts: [
        { name: "x", type: "@adobe/datatype-number", displayName: "X" },
        { name: "y", type: "@adobe/datatype-number", displayName: "Y" }
    ],
    process: async (inputs) => ({
        x: inputs.vector.x,
        y: inputs.vector.y
    })
});
```

Pattern characteristics:

* Single complex/structured input port
* Multiple primitive output ports
* Process function extracts properties
* Often tagged with `decompose`

### Stateful Node

A stateful node keeps a resource or accumulated state on its persistent scope across executions (see the Persistent Node Scope section). Build the resource once in `init`, reuse it in `process`, and release it in `shutdown`. Here `init` is `async` because the resource loads asynchronously.

```typescript
// SceneRenderer / createSceneRenderer are illustrative — substitute your own resource.
interface RenderScope {
    renderer: SceneRenderer;
    frames: number;
}

export default createNodePlugin({
    displayName: "Scene Renderer",
    description: "Renders a frame from a scene built once and reused",
    tags: ["category:3d", "render", "stateful"],
    inputPorts: [
        { name: "seed", type: "@adobe/datatype-number", displayName: "Seed", defaultValue: 0 }
    ],
    outputPorts: [
        { name: "image", type: "@adobe/datatype-image", displayName: "Image" }
    ],
    // Built once, before the first render. The return type defines RenderScope.
    init: async (): Promise<RenderScope> => {
        const renderer = await createSceneRenderer();
        return { renderer, frames: 0 };
    },
    process: async (inputs, context) => {
        context.scope.frames += 1;
        const image = await context.scope.renderer.render(inputs.seed);
        return { image };
    },
    // Release GPU / native resources on delete or runtime destroy.
    shutdown: (scope) => {
        scope.renderer.dispose();
    }
});
```

Pattern characteristics:

* Expensive resource built once in `init`, not rebuilt each execution
* State (the renderer and frame count) persists on `context.scope`
* `shutdown` releases the resource when the node is deleted
* Holds handles that must be disposed — GPU contexts, workers, connections

### Seeded / Randomizable Node

A seeded node exposes a randomizable input — typically a `seed` — paired with `shuffle` and `canShuffle` (see the Shuffling section) so a "Run again" draws a fresh value instead of reusing the cached output.

```typescript
export default createNodePlugin({
    displayName: "Random Number",
    description: "Generates a random number from a re-rollable seed",
    tags: ["category:input", "number", "random"],
    inputPorts: [
        { name: "seed", type: "@adobe/datatype-number", displayName: "Seed", defaultValue: 0 }
    ],
    outputPorts: [
        { name: "value", type: "@adobe/datatype-number", displayName: "Value" }
    ],
    process: async inputs => ({ value: seededRandom(inputs.seed) }),
    shuffle: async inputPorts => {
        inputPorts.seed.value.set(Math.floor(Math.random() * 1_000_000));
    },
    canShuffle: inputPorts => computed(() => !inputPorts.seed.isConnected.get())
});
```

Pattern characteristics:

* A randomizable input port (often named `seed`) drives non-deterministic output
* `shuffle` writes a fresh value onto that port before the next execution
* `canShuffle` is `false` once the port is wired to an upstream connection
* The "Run again" affordance triggers `shuffle` — there is no separate Shuffle button

## 10. External API Access

Nodes and widgets that reference a hardcoded network origin — in a `fetch()` call, a Lit template's `src` attribute, a GLSL `#include`, or any other embedded URL — must declare that origin in the plugin's `fetchSources` array. The `graph/no-undeclared-fetch-source` ESLint rule statically scans the plugin's source for hardcoded URLs and flags any whose origin isn't declared, so a missing declaration surfaces as a lint error instead of a runtime failure.

```typescript
export default createNodePlugin({
    displayName: "Fetch Data",
    description: "Fetches data from an external API",
    tags: ["category:network", "api", "fetch"],
    fetchSources: ["https://api.example.com"],
    inputPorts: [
        { name: "endpoint", type: "@adobe/datatype-string", displayName: "Endpoint" }
    ],
    outputPorts: [
        { name: "data", type: "@adobe/datatype-json", displayName: "Data" }
    ],
    process: async (inputs, context) => {
        const token = await context.getToken("example-provider", "API_TOKEN");
        const response = await fetch(`https://api.example.com/${inputs.endpoint}`, {
            headers: { Authorization: `Bearer ${token}` }
        });
        const data = await response.json();
        return { data };
    }
});
```

Only the origin (`https://api.example.com`) needs to be declared — `inputs.endpoint` just varies the path, which `fetchSources` does not restrict.

Key points:

* **Where it's declared** — the `fetchSources` array in the `create*Plugin({ ... })` config in `plugin.ts` is the single source of truth. The build merges it into `manifest.json`; don't edit `fetchSources` in the manifest directly.
* **Exact origin, no wildcards** — each entry must be a fully-qualified origin: scheme plus host, with no path and no wildcard patterns (`https://*.example.com` is not supported). A path on a declared entry is accepted but ignored during matching.
* **Every subdomain is a separate origin** — `https://api.example.com` and `https://cdn.example.com` are distinct origins and each must be declared individually.
* **Paths and query strings can vary freely** — once an origin is declared, any path or query string against it is allowed, e.g. `https://api.example.com/${id}?key=${key}` only requires `https://api.example.com` to be declared.
* **The host itself must be static** — a URL whose host is interpolated (e.g. `` `https://${host}/...` ``) can never be recorded in `fetchSources` and is always flagged; use a static, fully-qualified origin instead.
* **Scanning is usage-agnostic** — the lint rule flags every hardcoded URL in the file, not just ones passed to `fetch()`. A URL assigned to a constant, interpolated into a template, or used as a Lit `src` attribute is treated the same way, since any of these could eventually be requested.
* **Helper modules are scanned too** — any `.ts` file in the same folder as `plugin.ts` is checked, not just `plugin.ts` itself, since implementation is often split across adjacent files.
* **Two exemptions** — a URL used only as an XML/SVG namespace (`xmlns="http://www.w3.org/2000/svg"`), or one sitting inside a comment embedded in a string literal (e.g. a source-attribution comment in GLSL shader code), is not treated as a network request and doesn't need to be declared.
* **Retrieve auth tokens via context** — use `context.getToken(namespace, tokenName)` (it returns a `Promise`, so `await` it) rather than hardcoding credentials in the URL or headers.

### Static vs. Dynamic Origins

A declared origin must be fully static. Interpolating the *path* is fine; interpolating the *host* is not, because a dynamic host can never be matched against a fixed `fetchSources` entry:

```typescript
// Not allowed — the host is built dynamically and can never be declared in fetchSources
const response = await fetch(`https://${apiHost}/data`);

// Allowed — the origin is static; only the path varies
const response = await fetch(`https://api.example.com/${endpoint}`);
```

If a violation is found directly inside `plugin.ts`, `eslint --fix` can add the missing origin to `fetchSources` automatically. A violation found in a helper module can't be auto-fixed — the config lives in the sibling `plugin.ts`, so add the origin there by hand.

<InlineAlert variant="warning" slots="text"/>

Declare every origin your plugin's code touches — including each subdomain separately — in `fetchSources`. Undeclared fetch attempts are blocked by the platform at runtime, and the `graph/no-undeclared-fetch-source` ESLint rule catches undeclared or dynamically-constructed origins earlier, at lint time.

## 11. File Structure

Every node plugin requires `manifest.json` and `plugin.ts`.

### manifest.json

The manifest declares the plugin's metadata and dependencies. **You must list ALL datatype and widget dependencies**, including those used only in type annotations.

```json
{
    "name": "@adobe/node-example",
    "version": "1.0",
    "platformVersion": 1,
    "dependencies": {
        "@adobe/datatype-number": { "majorVersion": 1 },
        "@adobe/widget-number": { "majorVersion": 1 }
    }
}
```

Key fields:

* **name** — Unique plugin identifier, typically scoped (e.g., `@adobe/node-add`)
* **version** — Plugin version (major.minor format)
* **platformVersion** — Platform API version (currently 1)
* **dependencies** — All datatype and widget plugins used by this node

## 12. Naming Conventions

Consistent naming helps with discoverability and understanding a node's purpose at a glance. Follow these patterns:

| Pattern | Examples |
|---|---|
| `node-input-{type}` | `node-input-number`, `node-input-string`, `node-input-image` |
| `node-preview-{type}` | `node-preview-number`, `node-preview-image`, `node-preview-json` |
| `node-output-{type}` | `node-output-number`, `node-output-string`, `node-output-image` |
| `node-{operation}-{types}` | `node-add-n-n`, `node-multiply-3-n`, `node-concat-strings` |
| `node-convert-{from}-to-{to}` | `node-convert-number-to-vector2`, `node-convert-string-to-number` |
| `node-create-{type}` | `node-create-vector2`, `node-create-color`, `node-create-matrix` |
| `node-properties-{type}` | `node-properties-vector2`, `node-properties-color`, `node-properties-image` |

Additional naming guidelines:

* Use kebab-case for plugin names
* Use descriptive operation verbs (add, multiply, convert, create, extract, etc.)
* Include type hints in the name for complex operations
* Keep names concise but unambiguous

## 13. Best Practices

Follow these principles to create high-quality, maintainable node plugins:

### Single Responsibility

Keep nodes focused on one operation. A node that adds two numbers should not also multiply them. Create separate nodes for separate operations. This makes nodes more reusable and easier to test.

### Consistent Datatype Patterns

Use established datatype patterns consistently across related nodes. If you're working with 2D vectors, use `@adobe/datatype-vector2` throughout rather than creating custom structures. This ensures compatibility between different authors' nodes.

### Meaningful Default Values

Provide sensible defaults for input ports. A number input should default to `0`, not `undefined`. A string input might default to `""`. Defaults should allow the node to execute successfully without any connections.

### Descriptive Tags

Add meaningful tags for discoverability:

* Always include a `category:` tag (e.g., `category:math`, `category:image`)
* Add operation tags (add, subtract, filter, transform, etc.)
* Include datatype tags for type-specific operations
* Add domain-specific tags (color, geometry, network, etc.)

### Error Handling

Validate inputs and surface failures with the typed error classes — `PortError` for a bad input, `NodeError` for a node-level problem — so users get actionable, precisely-placed messages. See the Error Handling section for details.

### Performance Considerations

* Avoid expensive computations in widget binding functions — they run on every render
* Cache expensive operations across executions on the node's persistent scope (see the Persistent Node Scope section) — do not use module-level variables
* Use streaming APIs for large data transfers
* Consider memory implications for resource-heavy operations

<InlineAlert variant="info" slots="text"/>

For deeper conceptual understanding of node design patterns and graph thinking, see [How to Think About Nodes](../how-to-think-about-nodes/index.md).

## Next Steps

Now that you understand the fundamentals of node development, explore these related topics:

* **[How to Think About Nodes](../how-to-think-about-nodes/index.md)** — Design philosophy, behavioral classifications, streams vs. lists vs. values, wicked types, and anti-patterns to avoid
* **[CLI Reference](../cli-reference/index.md)** — Complete reference for build, dev, submit, and install commands
* **[Submitting Plugins](../submitting-plugins/index.md)** — How to submit your plugins for review and publish to the registry

<InlineAlert variant="info" slots="text"/>

**Need help?** Reach out to the Graph team in the [#prj-graph-plugins](https://adobe.enterprise.slack.com/archives/C0ANK4FL49W) Slack channel.
