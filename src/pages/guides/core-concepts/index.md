---
title: Core Concepts - Firefly Graph
description: How the Project Graph plugin system is architected — datatypes, widgets, nodes, and utilities.
---

# Core Concepts

The Project Graph plugin system provides an extensible architecture for building custom nodes, datatypes, and UI components. Understanding the core concepts of how these plugins work together is essential for developing effective graph-based workflows.

Start here. This page gives you the mental model the rest of the guide assumes: how the four plugin types depend on each other, how a value moves from one node's output port into another's input, and what terms like port, binding, and resolution actually mean. Once it clicks, the implementation pages read as variations on one idea instead of ten separate APIs.

## The Plugin Ecosystem

The plugin system is built on four foundational types that work together:

### Datatypes

Datatypes define the shape and structure of data that flows through the graph. Examples include primitives like `number`, `string`, and `boolean`, as well as more complex types like `image`, `vector2`, `color`, and `mesh`.

Key characteristics:

* Define data structure and validation
* Do not have their own UI implementation
* Reference a default widget for visualization and editing
* Provide type safety for connections between nodes

### Widgets

Widgets are Lit web components that provide UI for viewing and editing datatype values. They are reactive components built on a signal-based system that automatically updates when data changes.

Key characteristics:

* Built as Lit web components
* Use a reactive signal system for automatic updates
* Can be bound to node ports (inputs or outputs)
* Come in two forms: port widgets (compact) and node widgets (larger, display-oriented)
* Do not perform computation — they only display and edit values

### Nodes

Nodes are computational units that define processing logic with typed input and output ports. Each node has a `process` function that receives input values and returns output values.

Key characteristics:

* Define typed input ports (left side) and output ports (right side)
* Implement a `process` function that performs the actual computation
* Bind widgets to their ports for user interaction
* Can be synchronous or asynchronous
* Support default values for inputs when no connection exists

### Utilities

Utility plugins are shared code libraries that other plugins import as dependencies. They have no runtime execution role — the platform never "runs" a utility plugin directly.

Key characteristics:

* Export reusable functions, constants, type guards, or web worker factories
* No runtime execution — pure code libraries with no lifecycle or process function
* Other plugins declare them as dependencies and import from them
* Can be multi-file: each `.ts` source file compiles to a separate bundle entry with its own `.d.ts` declarations

### The Relationship

These four plugin types work together, with utilities providing shared code imported by the other three:

```text
Utility ← (imported by) Widget | Node
Datatype ← Widget ← Node

• Utility exports shared code imported by other plugins
• Datatype defines the data shape
• Widget provides UI for that datatype
• Node uses datatypes for ports and binds widgets for interaction
```

<InlineAlert variant="info" slots="text"/>

**Example:** A `number` datatype might use a `number-input` widget by default. An `add` node would have two input ports and one output port, all of type `number`, and would bind the `number-input` widget to its input ports for inline editing.

## How Data Flows

Understanding data flow is fundamental to working with the graph system:

### Connection-Based Flow

Data flows through connections between node ports. The flow is always directional: **output → input**.

* An output port can connect to multiple input ports (one-to-many)
* An input port can only receive from one output port (one-to-one)
* Connections are type-safe — you can only connect ports of compatible types
* Data flows through the graph based on execution order determined by the runtime

### Port Type Safety

Each port is associated with exactly one datatype. The graph editor enforces type compatibility:

* **Direct connections:** Only ports of the same datatype can be directly connected
* **Automatic conversion:** The editor can auto-insert conversion nodes when connecting incompatible but convertible types
* **Type indicators:** Ports are color-coded by type for visual clarity

### The Process Function

Each node implements a `process` function that:

* Receives an object containing values from all connected input ports
* Performs computation, transformation, or other operations
* Returns an object containing values for all output ports
* Can be async for operations like API calls or ML inference

```typescript
process(inputs: { a: number; b: number }): { result: number } {
  return { result: inputs.a + inputs.b };
}
```

### Widget Role in Data Flow

Widgets provide UI but do not perform computation:

* They display current port values
* They allow users to edit values (which triggers re-execution)
* They react to changes in connected data
* They do not transform or process data themselves

<InlineAlert variant="info" slots="text"/>

**Key Principle:** Widgets are for interaction, nodes are for computation. This separation keeps the architecture clean and composable.

## Ports and Connections

### Port Anatomy

Every port has several key properties:

* **Direction:** Input (left side) or output (right side)
* **Datatype:** The type of data this port accepts or produces
* **Name:** A unique identifier within the node
* **Label:** Human-readable text displayed in the UI
* **Default value:** Value used when no connection exists (input ports only)

### Input Ports

Input ports appear on the left side of a node:

* Can have default values
* Can be optional (node can execute without a value)
* Can be hidden (used with widget bindings)
* Can have port widgets for inline editing
* Receive data from upstream output ports

### Output Ports

Output ports appear on the right side of a node:

* Produce values from the node's `process` function
* Can connect to multiple downstream input ports
* Can be hidden (used with widget bindings)
* Can be bound to node widgets for preview/display

### Type Compatibility

Connection rules based on type compatibility:

* **Same type:** Direct connection allowed
* **Convertible types:** Auto-insert conversion node offered
* **Incompatible types:** Connection not allowed

### Hidden Ports

Ports can be hidden from the visual display:

* Used when a widget provides the primary interaction method
* Still participate in data flow and execution
* Common in value nodes and control nodes
* Can be revealed for advanced use cases

### Optional Ports

Input ports can be marked as optional:

* Node can execute without a value on this port
* The `process` function receives `undefined` for missing optional values
* Useful for parameters with intelligent defaults or conditional behavior

## Widget Binding

Widget binding is how nodes connect UI components to their ports. There are two distinct binding mechanisms, each serving a different purpose:

### Port Widget Binding

Port widgets are small, compact UI elements rendered inline next to an input port. They are used for editing input values when no upstream connection exists.

**Characteristics:**

* Displayed adjacent to the port (typically to the right of input ports)
* Should be compact and space-efficient
* Only shown when the port has no incoming connection
* Automatically hidden when a connection is made
* Bound to a single input port
* Defined using `portWidgetBinding`

**Example use cases:**

* Number input field next to a numeric port
* Color swatch next to a color port
* Checkbox next to a boolean port
* Small dropdown for enum selection

```typescript
// Port widget binding example
portWidgetBinding: {
  portName: 'value',        // The input port to bind to
  widgetType: 'number-input' // The compact widget to display
}
```

### Node Widget Binding

Node widgets are larger UI elements rendered on the node body itself. They provide rich previews, large editing surfaces, or complex controls that need more space.

**Characteristics:**

* Displayed in the main body of the node
* Can be larger and more complex than port widgets
* Can bind to multiple ports (both inputs and outputs)
* Always visible (not hidden by connections)
* Can bind to output ports for preview/display
* Returns an array of bindings
* Defined using `nodeWidgetBinding`

**Example use cases:**

* Image preview for an image output port
* Multi-line text editor for a string input
* Graph visualization for data output
* Large color picker with advanced controls
* 3D mesh preview

```typescript
// Node widget binding example
nodeWidgetBinding: () => [
  {
    portName: 'output',          // Can bind to input OR output
    widgetType: 'image-preview'  // Larger preview widget
  },
  {
    portName: 'caption',
    widgetType: 'text-area'      // Multi-line editing
  }
]
```

### Key Differences

| Aspect | Port Widget | Node Widget |
|---|---|---|
| **Location** | Next to the port | On the node body |
| **Size** | Compact | Can be large |
| **Visibility** | Hidden when port is connected | Always visible |
| **Port Direction** | Input ports only | Input or output ports |
| **Binding Count** | One widget per port | Multiple ports per widget |
| **Primary Use** | Inline editing of inputs | Preview, display, complex editing |

<InlineAlert variant="info" slots="text"/>

**Design Guideline:** Use port widgets for simple, inline editing when no connection exists. Use node widgets for richer displays, previews, or when you need more space for interaction.

## Key Terminology

Essential terms for understanding the Project Graph plugin system:

| Term | Definition |
|---|---|
| **Utility Plugin** | A shared code library with no runtime execution role. Exports functions, constants, type guards, or web worker factories that other plugins (datatypes, widgets, nodes) import as dependencies. |
| **Node** | A unit of functionality implemented as a JavaScript/TypeScript function with typed inputs and outputs. Performs computation, transformation, or other operations. |
| **Graph** | A collection of nodes and connections that define a workflow. Has inputs and outputs defined by connections to the graph surface (background). |
| **Port** | A typed connection point on a node. Can be an input port (left side) or output port (right side). Each port has a specific datatype. |
| **Widget** | A Lit web component UI element bound to one or more port values. Provides visualization and editing capabilities but does not perform computation. |
| **Port Widget** | A compact widget displayed inline next to a port for viewing/editing a single value. Hidden when the port has an incoming connection. |
| **Node Widget** | A larger widget displayed on the node body. Can bind to multiple ports (inputs or outputs) and is always visible. Used for previews and complex editing. |
| **Connection** | A data link between an output port and an input port. Always flows in one direction: output → input. Enforces type compatibility. |
| **Datatype** | Defines the shape, structure, and validation rules for data that flows through the graph. Examples: number, string, image, vector2. |
| **Capsule** | A simplified, packaged view of a graph showing just inputs and outputs. The internal graph runs as a black box. The core product unit of Project Graph. |
| **Value Node** | A node with one input and one output that displays/edits a single value. Typically wraps a widget with minimal logic. |
| **Conversion Node** | A node that converts data from one datatype to another. Can be automatically inserted by the graph editor when connecting incompatible but convertible types. |
| **Process Function** | The core computation function of a node. Receives input values and returns output values. Can be synchronous or asynchronous. |
| **Default Value** | The value used for an input port when no connection exists. Displayed and editable via port widgets. |
| **Hidden Port** | A port that participates in data flow but is not displayed in the visual UI. Often used when a widget provides the primary interaction method. |
| **Optional Port** | An input port that can be undefined. The node can execute without a value on this port. The process function handles the undefined case. |

<InlineAlert variant="success" slots="text"/>

**Next:** [Creating Plugins](../creating-plugins/index.md) — Set up your first plugin project and build a working node.

<InlineAlert variant="info" slots="text"/>

**Need help?** Reach out to the Graph team.
