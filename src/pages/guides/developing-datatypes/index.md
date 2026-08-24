---
title: Developing Datatypes - Firefly Graph
description: Define the data shapes that flow through a Project Graph workflow.
---

# Developing Datatypes

## 1. Introduction

Datatypes define the shape of data that flows through a Project Graph workflow. They are the foundation of the plugin ecosystem — every widget and node depends on datatypes. A datatype has no UI of its own; instead, it references a `defaultWidget` that the platform uses to display and edit values of that type.

When you create a datatype, you're establishing a contract for how data is structured and validated. The platform uses this contract to ensure type safety throughout the workflow, from node inputs and outputs to widget rendering and serialization.

## 2. Intrinsic Types

For data that can be directly serialized — numbers, strings, booleans, and simple objects — use `IntrinsicDataType`:

```typescript
import { type IntrinsicDataType, createDatatypePlugin } from "@graph/platform-exports/v1/datatype-plugin.js";

export default createDatatypePlugin<IntrinsicDataType<number>>({
    displayName: "Number",
    description: "A numeric value",
    tags: ["number", "primitive"],
    defaultWidget: "@adobe/widget-number"
});
```

Here are common intrinsic type patterns you can use as building blocks:

| Type Shape | Example Use |
|---|---|
| `IntrinsicDataType<number>` | Numbers, angles, percentages |
| `IntrinsicDataType<string>` | Text, prompts, code |
| `IntrinsicDataType<boolean>` | Toggles, switches |
| `IntrinsicDataType<{ x: number; y: number }>` | 2D vectors, positions, sizes |
| `IntrinsicDataType<{ r: number; g: number; b: number; a: number }>` | Colors |

## 3. Resource Types

For data backed by the platform's resource manager — binary assets like images, video, audio — use `ResourceType`:

```typescript
import { type ResourceType, createDatatypePlugin } from "@graph/platform-exports/v1/datatype-plugin.js";

export default createDatatypePlugin<ResourceType<"image">>({
    displayName: "Image",
    description: "An image resource",
    tags: ["category:image", "resource", "media"],
    defaultWidget: "@adobe/widget-image"
});
```

Resource types use the platform's resource manager for efficient handling of large binary data. The platform automatically handles caching, streaming, and lifecycle management. Instead of passing large binary blobs through the graph, resource types pass lightweight references that the runtime resolves as needed.

Common resource type categories include:

* `"image"` — Raster images (PNG, JPEG, WebP, etc.)
* `"video"` — Video files
* `"audio"` — Audio files
* `"model"` — 3D models and scenes
* `"document"` — Documents and rich text

## 4. Composite Types

For datatypes composed of other existing datatypes. This is a powerful pattern that enables significant reuse.

### 4.1 CompositeRecordType

Named fields referencing other datatypes (like a struct/object):

```typescript
import { type CompositeRecordType, createDatatypePlugin } from "@graph/platform-exports/v1/datatype-plugin.js";

export default createDatatypePlugin<CompositeRecordType<{
    name: "@adobe/datatype-string";
    age: "@adobe/datatype-number";
}>>({
    displayName: "Person",
    description: "A record with name and age fields",
    tags: ["composite", "record"],
    defaultWidget: "@adobe/widget-person"
});
```

Runtime values are plain objects: `{ name: "Alice", age: 30 }`

### 4.2 CompositeTupleType

Ordered elements referencing other datatypes (like a tuple/array):

```typescript
import { type CompositeTupleType, createDatatypePlugin } from "@graph/platform-exports/v1/datatype-plugin.js";

export default createDatatypePlugin<CompositeTupleType<[
    "@adobe/datatype-number",
    "@adobe/datatype-number"
]>>({
    displayName: "Number Pair",
    description: "An ordered pair of numbers",
    tags: ["composite", "tuple"],
    defaultWidget: "@adobe/widget-number-pair"
});
```

Runtime values are arrays: `[10, 20]`

### 4.3 Structured Fields

Both record and tuple types support structured fields for lists and streams:

```typescript
CompositeRecordType<{
    label: "@adobe/datatype-string";
    scores: { structure: "list"; type: "@adobe/datatype-number" };
}>
```

This creates a type with a `label` field (a single string) and a `scores` field (an array of numbers).

## 5. Why Reuse Existing Types

<InlineAlert variant="info" slots="text"/>

**Composing from existing datatypes is one of the most powerful patterns in the plugin ecosystem.**

When you compose a new datatype from existing datatypes, you gain several key advantages:

### Widget Reuse

Widgets already built for the constituent datatypes can be automatically reused. If you compose a record from `datatype-number` and `datatype-string`, the platform can render each field using the existing number and string widgets — no new widget needed. The platform automatically generates a composite widget that displays each field using its registered default widget.

### Consistency

Users see the same familiar widgets they already know, regardless of which composite type they're editing. A number field always looks and behaves like a number field, whether it's standalone or part of a larger composite type. This reduces cognitive load and creates a more predictable user experience.

### Interoperability

Nodes that work with the constituent types can work with decomposed fields of your composite type. For example, a node that takes a `datatype-number` input can accept the `age` field from a `Person` record type. The type system understands the relationships between composite and constituent types.

### Less Code

You don't need to build and maintain a custom widget for every new complex type. Each composite type you create can leverage the entire existing widget ecosystem, dramatically reducing development time and maintenance burden.

<InlineAlert variant="success" slots="text"/>

**Tip:** Before creating a new `IntrinsicDataType` for a complex object shape, consider whether a `CompositeRecordType` or `CompositeTupleType` would let you reuse existing widgets and infrastructure.

## 6. File Structure

Every datatype plugin requires two files:

### 6.1 manifest.json

Datatypes have no dependencies (they are leaf-level plugins in the dependency graph):

```json
{
    "name": "@adobe/datatype-example",
    "version": "1.0",
    "platformVersion": 1,
    "dependencies": {}
}
```

### 6.2 plugin.ts

The implementation exports a datatype configuration:

```typescript
import { type IntrinsicDataType, createDatatypePlugin } from "@graph/platform-exports/v1/datatype-plugin.js";

export default createDatatypePlugin<IntrinsicDataType<number>>({
    displayName: "Number",
    description: "A numeric value",
    tags: ["number", "primitive"],
    defaultWidget: "@adobe/widget-number"
});
```

## 7. Registration

<InlineAlert variant="info" slots="text"/>

Run `graph install` whenever you add a new plugin or change dependencies.

Run `graph install` to set up each plugin's TypeScript path configuration and link dependency types. It is automatically run as part of `graph build`.

## 8. Tags Convention

Tags help with discovery, categorization, and filtering in the platform. Follow these conventions:

* Use `"primitive"` for simple intrinsic types (number, string, boolean)
* Use `"category:xxx"` prefixed tags for categorization:
  * `"category:image"` — Image-related types
  * `"category:math"` — Mathematical types
  * `"category:geometry"` — Geometric types
  * `"category:color"` — Color-related types
  * `"category:media"` — Media types (video, audio)
* Use `"resource"` for all resource-backed types
* Use `"composite"` for composite record and tuple types
* Add descriptive tags for searchability (e.g., `"vector2"`, `"rgb"`, `"tuple"`, `"record"`)

Tags are case-insensitive and should use kebab-case for multi-word tags (e.g., `"multi-part-tag"`).

<InlineAlert variant="success" slots="text"/>

**Category tags are optional.** If `category:` tags are omitted from `manifest.json`, the CLI will prompt for a category on first submission. Categories are ultimately decided by the Project Graph team — treat your `category:` tags as a helpful suggestion to our curators.

## 9. Naming Conventions

Datatypes follow the pattern `datatype-{name}`:

* Primitives: `datatype-number`, `datatype-string`, `datatype-boolean`
* Math types: `datatype-vector2`, `datatype-vector3`, `datatype-matrix`
* Color types: `datatype-color`, `datatype-rgb`, `datatype-hsv`
* Media types: `datatype-image`, `datatype-video`, `datatype-audio`

All plugin names are scoped under `@adobe/` in manifests and references. Use lowercase with hyphens to separate words (kebab-case).

## 10. Best Practices

### Start Simple

Begin with the simplest type that meets your needs. You can always create more specialized types later. Most use cases can be covered by intrinsic types with primitive TypeScript types or composite types built from existing datatypes.

### Favor Composition

Before creating a new intrinsic type for a complex object, check if you can compose it from existing datatypes. This maximizes reuse and interoperability.

### Choose the Right Widget

The `defaultWidget` determines how users interact with values of your type. Choose a widget that provides the appropriate level of control and feedback. For composite types, the platform can auto-generate a widget if you don't specify one.

### Write Clear Descriptions

The `description` field appears in documentation and tooltips. Write clear, concise descriptions that help developers understand when to use your datatype.

### Test with Real Data

Create sample graphs that use your datatype with realistic values. This helps validate that your type definition matches actual usage patterns and that serialization/deserialization works correctly.

## 11. Next Steps

Now that you understand datatype development, explore related topics:

* **[Developing Widgets](../developing-widgets/index.md)** — Learn how to create UI components that view and edit your datatypes
* **[Widget Design Guidelines](../widget-design-guidelines/index.md)** — Visual design patterns and sizing conventions for widgets
* **[Developing Nodes](../developing-nodes/index.md)** — Build processing nodes that consume and produce your datatypes

<InlineAlert variant="info" slots="text"/>

**Need help?** Reach out to the Graph team in the [#prj-graph-plugins](https://adobe.enterprise.slack.com/archives/C0ANK4FL49W) Slack channel.
