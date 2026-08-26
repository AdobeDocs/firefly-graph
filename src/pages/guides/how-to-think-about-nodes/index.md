---
title: How to Think About Nodes - Firefly Graph
description: Design philosophy for building nodes that compose well in Project Graph.
---

# How to Think About Nodes

This page hands you a way to think about node design before you commit to code. It's about judgment. You'll get a vocabulary for it: the behavioral classes a node can fall into, when a port should carry a stream, a list, or a single value, how wicked types let one port accept many datatypes, and the anti-patterns that quietly wreck composability. Come here once you've built a node or two and want the next ones to slot cleanly into the ecosystem instead of fighting it.

## Overview

Through years of research and iteration, the Project Graph team has developed a behavioral classification system that helps ensure nodes are consistent, composable, and intuitive. This guide explains how to think about nodes based on what they DO, not just what they process.

<InlineAlert variant="info" slots="text"/>

**Important Distinction:** This guide describes **BEHAVIORAL CLASSIFICATIONS**, not categories. Categories in Project Graph are tags applied to nodes for organization and discoverability (e.g., `category:math`, `category:image`, `category:ai`). Behavioral classifications describe the ROLE a node plays — what kind of behavior it exhibits in the graph. A node always fits into exactly **one behavioral class**, but may belong to **any number of categories** via tags.

## Why This Matters

When building node-based systems, it's easy to fall into common anti-patterns:

* **Uber-nodes:** Nodes that try to do too many things at once, making them hard to understand and difficult to compose with other nodes
* **Overly specialized nodes:** Nodes that only work with very specific data configurations, limiting reusability
* **Inconsistent patterns:** Nodes that don't follow the same interaction patterns as similar nodes, creating confusion
* **Poor composability:** Nodes that don't play well with the broader ecosystem because they use types or patterns differently

Behavioral classification helps you avoid these problems by providing clear mental models for different kinds of nodes. When you know what behavioral class you're designing for, you can:

* Keep nodes focused and single-purpose
* Ensure consistent user experience across similar nodes
* Make nodes that compose well with the ecosystem
* Avoid duplicating functionality
* Create intuitive, predictable workflows

<InlineAlert variant="success" slots="text"/>

Think of behavioral classifications as design patterns for nodes. They provide guardrails that keep your designs focused and consistent.

## Preview Nodes

Preview nodes strictly visualize data without performing any processing or transformation. They are the graph equivalent of `console.log()`, `print()`, or `printf()` in traditional programming.

### Characteristics

* **No processing:** Data passes through unchanged from input to output
* **One input, one output:** Simple passthrough architecture
* **Visualization focus:** Primary purpose is to display data in a meaningful way
* **Widget wrapper:** Wraps a preview widget to show the data
* **Non-interactive:** Users can view but typically not edit the data

### Examples

* **Image Preview:** Displays an image datatype
* **Number Display:** Shows a numeric value with formatting
* **String Viewer:** Renders text content
* **Mesh Viewer:** Shows a 3D mesh with basic rotation
* **Graph Visualizer:** Displays data as a chart or graph

### Design Guidelines

* Keep them purely visual — no editing, no computation
* Make the preview widget the star — the node is just a wrapper
* Support common visualization options (zoom, pan, rotation) via widget configuration
* Consider making the input port hidden since the widget is the primary interaction

```typescript
// Preview node pattern
{
  inputs: [{ name: 'value', datatype: 'image' }],
  outputs: [{ name: 'value', datatype: 'image' }],
  process: (inputs) => ({ value: inputs.value }), // Passthrough
  nodeWidgetBinding: () => [
    { portName: 'value', widgetType: 'image-preview' }
  ]
}
```

## Control Nodes

Control nodes give users direct control over data through interactive widgets. They are primarily widget wrappers with minimal or no processing logic. There are two main subtypes:

### Value Nodes (Simple Control)

Value nodes provide a 1:1 relationship with a single datatype. They have one input port and one output port, both of the same type.

**Characteristics:**

* One input, one output of the same datatype
* Minimal or no processing (usually just passthrough)
* Primary interaction through the default widget
* Input port often hidden (widget provides the interaction)
* Used to introduce values into the graph or edit values inline

**Examples:**

* **Number Input:** Users enter or adjust a numeric value
* **String Input:** Text entry field
* **Color Picker:** Color selection interface
* **Boolean Toggle:** Checkbox or switch for true/false
* **Dropdown:** Selection from predefined options

```typescript
// Value node pattern
{
  inputs: [{ name: 'value', datatype: 'number', defaultValue: 0 }],
  outputs: [{ name: 'value', datatype: 'number' }],
  process: (inputs) => ({ value: inputs.value }),
  portWidgetBinding: {
    portName: 'value',
    widgetType: 'number-input'
  }
}
```

### Dynamic Control Nodes

Dynamic control nodes expose widget configuration properties as additional input ports, allowing the widget's behavior to be controlled by data flowing through the graph.

**Characteristics:**

* Multiple input ports: value + configuration parameters
* Configuration ports control widget behavior
* Enable data-driven UI adaptation
* More flexible than simple value nodes

**Examples:**

* **Slider (Dynamic):** min, max, step, and value are all input ports, allowing other nodes to control the slider's range
* **Dropdown (Dynamic):** Options list is an input port, allowing the choices to be generated dynamically
* **Text Input (Constrained):** maxLength and pattern are input ports, controlling validation

```typescript
// Dynamic control node pattern
{
  inputs: [
    { name: 'value', datatype: 'number', defaultValue: 50 },
    { name: 'min', datatype: 'number', defaultValue: 0 },
    { name: 'max', datatype: 'number', defaultValue: 100 },
    { name: 'step', datatype: 'number', defaultValue: 1 }
  ],
  outputs: [{ name: 'value', datatype: 'number' }],
  process: (inputs) => {
    const clamped = Math.max(inputs.min, Math.min(inputs.max, inputs.value));
    return { value: clamped };
  }
}
```

### Design Guidelines for Control Nodes

* Keep processing minimal — focus on widget interaction
* Use simple value nodes for static, user-controlled inputs
* Use dynamic control nodes when widget behavior needs to adapt to data
* Don't combine control with complex operations — that's an operation node's job
* Consider hiding the value input port when the widget is the primary interaction

## Operation Nodes

Operation nodes perform the actual work in a graph — computation, transformation, inference, or other processing. They are the "verbs" of your workflow. Operation nodes can be further classified by the kind of operation they perform:

### Composition and Decomposition Nodes

These nodes create complex types from simple ones (composition) or break complex types into their constituent parts (decomposition). They are like constructors and introspection utilities.

**Composition Examples:**

* **Create Vector2:** Takes x and y numbers, outputs a vector2
* **Create Color (RGBA):** Takes red, green, blue, alpha numbers, outputs a color
* **Create Transform:** Takes position, rotation, scale, outputs a transform
* **Build Object:** Takes multiple typed inputs, outputs a structured object

**Decomposition Examples:**

* **Vector2 Components:** Takes vector2, outputs x and y numbers
* **Color Channels:** Takes color, outputs separate R, G, B, A values
* **Transform Parts:** Takes transform, outputs position, rotation, scale
* **Get Property:** Extracts a specific field from an object

```typescript
// Composition example
{
  inputs: [
    { name: 'x', datatype: 'number', defaultValue: 0 },
    { name: 'y', datatype: 'number', defaultValue: 0 }
  ],
  outputs: [{ name: 'vector', datatype: 'vector2' }],
  process: (inputs) => ({
    vector: { x: inputs.x, y: inputs.y }
  })
}

// Decomposition example
{
  inputs: [{ name: 'vector', datatype: 'vector2' }],
  outputs: [
    { name: 'x', datatype: 'number' },
    { name: 'y', datatype: 'number' }
  ],
  process: (inputs) => ({
    x: inputs.vector.x,
    y: inputs.vector.y
  })
}
```

### Conversion Nodes

Conversion nodes transform data from one datatype to another. They have a single input and a single output of different types. Think of them like type casting in traditional programming.

**Characteristics:**

* One input of type A, one output of type B
* Focused, single-purpose transformation
* Can be automatically inserted by the graph editor
* Should be lossless when possible, or clearly document loss
* Should be fast and deterministic

**Examples:**

* **Number to String:** Converts numeric value to text representation
* **String to Number:** Parses text to numeric value
* **Degrees to Radians:** Angle unit conversion
* **Color to Hex String:** Color to #RRGGBB format
* **Image to Texture:** Converts image data to GPU texture format

<InlineAlert variant="info" slots="text"/>

**Auto-Conversion:** When marked appropriately, conversion nodes can be automatically inserted by the graph editor when a user tries to connect incompatible port types. This creates a smooth, intelligent authoring experience.

```typescript
// Conversion node pattern
{
  inputs: [{ name: 'value', datatype: 'number' }],
  outputs: [{ name: 'result', datatype: 'string' }],
  process: (inputs) => ({
    result: inputs.value.toString()
  })
}
```

### Local/Domain-Specific Operation Nodes

These nodes perform operations within a specific domain. They typically run synchronously and execute client-side. They are the "workhorse" nodes that perform the bulk of processing in most graphs.

**Characteristics:**

* Focused on a specific domain (math, image processing, vector operations, etc.)
* Usually synchronous and fast
* Execute locally (client-side)
* Take multiple inputs, produce one or more outputs
* Deterministic — same inputs always produce same outputs

**Examples by Domain:**

**Math:**

* Add, Subtract, Multiply, Divide
* Sin, Cos, Tan, Sqrt, Pow
* Min, Max, Clamp, Lerp
* Random Number Generation

**Vector Math:**

* Vector Add, Subtract, Scale
* Dot Product, Cross Product
* Normalize, Length, Distance

**Image Processing:**

* Blur, Sharpen, Edge Detection
* Crop, Resize, Rotate
* Color Adjustment (brightness, contrast, saturation)
* Blend, Composite

**String Operations:**

* Concatenate, Split, Replace
* Uppercase, Lowercase, Trim
* Regular Expression Match

**3D/Geometry:**

* Mesh Operations (merge, boolean, subdivision)
* Transform (translate, rotate, scale)
* UV Mapping

```typescript
// Local operation node pattern
{
  inputs: [
    { name: 'a', datatype: 'number' },
    { name: 'b', datatype: 'number' }
  ],
  outputs: [{ name: 'result', datatype: 'number' }],
  process: (inputs) => ({
    result: inputs.a + inputs.b
  })
}
```

### Inference/Translation Operation Nodes

These nodes make asynchronous calls to machine learning models, external APIs, or cloud services. They often involve AI/ML inference, language translation, or other operations that require external compute.

**Characteristics:**

* Asynchronous execution (returns a Promise)
* May require network calls
* Can be time-consuming
* Non-deterministic (especially for generative AI)
* May require authentication or API keys
* Should handle errors gracefully
* Often show progress or loading states

**Examples:**

* **Firefly Text-to-Image:** Generates images from text prompts
* **Style Transfer:** Applies artistic style to images
* **Text Summarization:** Condenses long text to key points
* **Object Detection:** Identifies objects in images
* **Language Translation:** Translates text between languages
* **Sentiment Analysis:** Analyzes emotional tone of text
* **Speech-to-Text:** Transcribes audio to text

```typescript
// Inference operation node pattern
{
  inputs: [
    { name: 'prompt', datatype: 'string' },
    { name: 'style', datatype: 'string', defaultValue: 'photo' }
  ],
  outputs: [{ name: 'image', datatype: 'image' }],
  async process(inputs) {
    const response = await fireflyAPI.generateImage({
      prompt: inputs.prompt,
      style: inputs.style
    });
    return { image: response.imageData };
  }
}
```

<InlineAlert variant="warning" slots="text"/>

**Error Handling:** Inference nodes should always handle network failures, timeouts, rate limits, and API errors gracefully. Consider providing fallback values or clear error messages to users.

### Design Guidelines for Operation Nodes

* Keep operations focused on a single transformation or computation
* Use composition/decomposition for structural transformations
* Use conversion for type transformations
* Use local operations for synchronous, deterministic work
* Use inference operations for async, ML/API work
* Don't mix behavioral classes — split complex nodes into simpler, focused ones
* Make operations composable — outputs should be useful as inputs to other nodes

## Streams, Lists, and Values

Ports carry data in one of three **structures**. Choosing the right structure is one of the most important design decisions you will make, because it determines how data flows through the graph and when downstream nodes can start processing.

### Value (scalar)

A single, standalone data item. This is the default when no `structure` field is specified on a port.

* **Use when:** The port carries exactly one thing — one number, one string, one image.
* **Example:** The `result` output of a node that adds two numbers.

### List

A static, finite array of values. All items are available at once before any downstream processing begins.

* **Use when:** You know the number of items upfront, or you need random access to elements.
* **Declared with:** `structure: "list"` on the port definition.
* **Example:** A node that takes a list of prompts and returns a list of generated images.
* **Trade-off:** The entire list must be fully computed before any downstream node can start. Avoid lists for large or lazily-produced datasets.

### Stream

A lazy, push-based sequence of values delivered incrementally over time via `ReadableStream`. Items are produced and consumed one at a time.

* **Use when:** Data arrives progressively (generative AI tokens, video frames, large datasets), or you want pipeline parallelism — downstream nodes can begin processing early items while upstream nodes continue producing.
* **Declared with:** `structure: "stream"` on the port definition.
* **Example:** A text generation node that streams token chunks so a downstream display node updates in real time.
* **Trade-off:** Streams cannot be randomly accessed or measured in advance. Downstream nodes must handle incremental consumption.

<InlineAlert variant="success" slots="text"/>

**Rule of thumb:** Default to values for simple data, lists for bounded collections, and streams for generative or real-time data. Streams enable the best user experience for AI-powered nodes because the graph feels live and responsive.

The runtime handles stream consumption safely — if a stream output connects to two downstream nodes, the platform automatically TEEs it so each consumer receives its own independent stream.

## Wicked Types

A **wicked type** is a port whose datatype is resolved dynamically at runtime rather than being fixed at authoring time. This is how polymorphic nodes work.

### When to use wicked types

Use wicked types when your node should work with *any* datatype — for example:

* A passthrough node (`output = input`, regardless of type)
* A logging or debug node that can inspect any value
* A subgraph that exposes its internal node ports as configurable inputs and outputs

### How they work

In a node manifest, declare a `wickedTypes` map that names each polymorphic slot and lists the compatible types it can resolve to at runtime:

```json
{
  "wickedTypes": {
    "T": ["@adobe/datatype-number", "@adobe/datatype-string", "@adobe/datatype-image"]
  }
}
```

In the port definition, reference the wicked type identifier instead of a specific datatype. At runtime, the platform resolves `T` to the actual connected type.

### Wicked types in Capsule ports

Wicked types are also how **Capsule-level ports** work. When a Capsule exposes its own inputs and outputs, those graph-level ports are dynamically composed from the catalog definitions of the internal node ports they are bound to. The graph port type is "wicked" from whatever type the bound internal port carries — this is what makes Capsules recomposable without requiring changes to the graph manifest.

### Wicked types and widgets

Widgets can also declare wicked types to handle values of any compatible datatype. This is useful for generic preview or display widgets that need to render multiple types without specializing for each one.

## Categories and Tags

Tags with the `category:` prefix control which section a node appears in within the node picker. As noted in the Overview, categories describe *where to find* a node, while behavioral classes describe *what it does*.

| Category tag | Domain |
|---|---|
| `category:input` | Source nodes that provide user-editable values |
| `category:output` | Sink nodes that expose Capsule outputs |
| `category:preview` | Nodes that display data without modifying it |
| `category:math` | Arithmetic, algebra, geometry, vector math |
| `category:image` | Image manipulation, compositing, filtering |
| `category:color` | Color conversion, mixing, adjustment |
| `category:text` | String manipulation, formatting, parsing |
| `category:network` | External API calls, HTTP, data fetching |
| `category:conversion` | Type conversion between datatypes |
| `category:ai` | Generative AI, model inference |

**Guidance:**

* Use exactly one `category:` tag per node. Multiple category tags fragment discoverability.
* Add additional plain tags for searchability: operation verbs (`add`, `multiply`, `resize`), type names (`vector2`, `rgb`), domain keywords (`firefly`, `blend`).
* If no standard category fits, consider defining a new one consistently across all nodes in your plugin — but do not invent one-off categories for individual nodes.

## Port Naming

Port names become keys in the `inputs` and `outputs` objects of your `process` function, and appear in the graph UI via `displayName`.

* Use **camelCase** for the `name` field (`inputImage`, `blendAmount`, `outputColor`).
* Use **semantically meaningful names** that describe the data, not the position. `sourceImage` and `overlayImage` are better than `image1` and `image2`. Short symmetric names like `a` and `b` are fine for math nodes where the symmetry is the point.
* **Output port names** should describe the result, not the operation — `result`, `image`, `color` rather than `computed` or `processed`.
* **Hidden ports** used to store editable values on input/output nodes should match their corresponding visible output port name.

## Node Ideation Checklist

When designing a new node, ask yourself these questions to ensure you're following good patterns:

### 1. What are you trying to achieve?

* What problem does this node solve?
* What workflow will it enable?
* Who is the target user?

### 2. What are the underlying operations required?

* Break down the functionality into discrete steps
* Can it be expressed as a single operation or does it need to be split?
* Are there existing nodes that do part of this work?

### 3. Which behavioral class does each operation fit?

* Is this a preview (visualization only)?
* Is this a control (user input)?
* Is this an operation (processing)?
* If operation: composition/decomposition, conversion, local, or inference?

### 4. Does this node try to do too much?

* Can you describe it in one simple sentence?
* Does it mix behavioral classes (e.g., control + operation)?
* Would splitting it make the workflow clearer?
* Are you creating an "uber-node" that does everything?

### 5. Does it play well with existing nodes?

* Does it use standard datatypes consistently?
* Can its outputs connect naturally to other nodes' inputs?
* Does it follow the same patterns as similar nodes?
* Does it duplicate functionality that already exists?

### 6. Is it composable?

* Can it be combined with other nodes to create more complex workflows?
* Are the inputs and outputs granular enough to be useful individually?
* Does it force users into a specific workflow or allow flexibility?

### 7. Is it the right level of abstraction?

* Too low-level? (So granular it's tedious to use)
* Too high-level? (So specialized it only works for one use case)
* Just right? (Useful on its own, composable with others)

## Anti-Patterns to Avoid

Common mistakes when designing nodes:

### Uber-Nodes

**Problem:** A single node that tries to do too many things at once.

**Example:** An "Image Editor" node with 20 different operations, mode switching, and conditional logic.

**Solution:** Split into focused nodes: Blur, Crop, Adjust Brightness, etc. Let users compose them.

### Overly Specialized Nodes

**Problem:** Nodes that only work with very specific data configurations or workflows.

**Example:** A "Process Portrait Photo for Instagram" node that assumes specific aspect ratios, filters, and outputs.

**Solution:** Create general-purpose nodes (Resize, Apply Filter, Adjust Colors) that can be composed for many use cases.

### Duplicated Functionality

**Problem:** Creating a new node that does what existing nodes already do.

**Example:** Creating "Add Numbers" when "Add" already exists.

**Solution:** Search the node catalog first. Extend existing nodes if needed. Only create new nodes for truly new functionality.

### Inconsistent Type Usage

**Problem:** Using datatypes differently than the rest of the ecosystem.

**Example:** A node that expects a "color" as a hex string when the platform uses a structured color datatype.

**Solution:** Follow platform conventions. Use standard datatypes consistently. Create conversion nodes if needed.

### Mixed Behavioral Classes

**Problem:** Combining control and operation logic in a single node.

**Example:** A node that both lets users input a value AND performs complex processing on it.

**Solution:** Separate concerns. Create a control node for input and an operation node for processing.

### Poor Composability

**Problem:** Nodes with inputs/outputs that don't connect naturally to other nodes.

**Example:** A node that outputs a complex, proprietary data structure that no other node can consume.

**Solution:** Use standard datatypes. Provide decomposition nodes if needed. Think about the downstream workflow.

## Summary

Behavioral classifications provide a mental model for designing effective nodes:

* **Preview Nodes:** Visualize data (passthrough with display)
* **Control Nodes:** Give users control over data
  * Value Nodes: Simple 1:1 input/output
  * Dynamic Control Nodes: Widget configuration via ports
* **Operation Nodes:** Process data
  * Composition/Decomposition: Build or break apart complex types
  * Conversion: Type transformation
  * Local Operations: Synchronous, domain-specific processing
  * Inference Operations: Async ML/API calls

<InlineAlert variant="success" slots="text"/>

**Remember:** These behavioral classifications describe what a node DOES (its role). Categories like `category:math` or `category:image` are tags that help users FIND nodes. Every node has exactly one behavioral class but can have many category tags.

By keeping these patterns in mind, you'll create nodes that are:

* Focused and single-purpose
* Consistent with platform conventions
* Composable with other nodes
* Intuitive for users to understand and use
* Maintainable and extensible over time

<InlineAlert variant="success" slots="text"/>

**Next:** [CLI Reference](../cli-reference/index.md) — Complete reference for all `graph` commands: `dev`, `build`, `install`, `submit`, and more.

<InlineAlert variant="info" slots="text"/>

**Need help?** Reach out to the Graph team in the [#prj-graph-plugins](https://adobe.enterprise.slack.com/archives/C0ANK4FL49W) Slack channel.
