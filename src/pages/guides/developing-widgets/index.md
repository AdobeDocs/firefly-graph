---
title: Developing Widgets - Firefly Graph
description: Build Lit web components that view and edit datatype values in Project Graph.
---

# Developing Widgets

This page teaches you to build the UI layer of the graph: Lit web components that read a datatype value and write edits back through the reactive signal system. You'll start with a display-only widget, add editing, then handle multi-field and composite values. By the end you'll know when to reach for Spectrum Web Components, how port widgets differ from node body widgets, and which pitfalls trip people up first. Widgets don't compute anything. They render and edit, and that constraint shapes every decision here.

## 1. Introduction

Widgets are Lit web components that render UI for datatype values in Project Graph. They extend `WidgetElement<typeof data>` and use a reactive signal system for data binding. Widgets are what users interact with directly in the graph editor — from simple number inputs to complex image previews.

Unlike nodes, widgets don't perform computation. They exist solely to visualize and edit datatype values, providing an intuitive interface for users to interact with data flowing through the graph.

> Widgets are the user-facing layer of your datatypes. A well-designed widget makes complex data types accessible and easy to work with.

## 2. Widget Architecture

Widgets in Project Graph are built on a modern, reactive architecture:

* **Built with Lit** — A lightweight web component library from Google that provides reactive rendering and declarative templates
* **Extend WidgetElement** — The base class from `@graph/platform-exports/v1/widget-plugin.js` that provides the signal-based data binding system
* **Data definition** — The `data` object defines which datatype fields the widget operates on. This MUST use `as const` for proper TypeScript type inference
* **Reactive signals** — The platform manages state updates automatically. When data changes upstream, your widget re-renders automatically
* **Read and write only** — Widgets don't perform computation. They only read data from bound ports and write user edits back to those ports

> Think of widgets as "view controllers" for your datatypes. The graph runtime handles all the complex state management and data flow — you just focus on rendering and user interaction.

## 3. Display-Only Widget Pattern

The simplest widget pattern is display-only. This widget reads a value and displays it without allowing user edits.

```typescript
import { WidgetElement, createWidgetPlugin } from "@graph/platform-exports/v1/widget-plugin.js";
import { html, css, type TemplateResult, type CSSResultGroup } from "lit";

const data = {
    value: {
        type: "@adobe/datatype-number",
        displayName: "Value",
        description: "The numeric value to display"
    }
} as const;

class NumberDisplayWidget extends WidgetElement<typeof data> {
    public render(): TemplateResult {
        const value = this.widgetData.get("value").get();
        return html`<span>${value ?? 0}</span>`;
    }

    static styles: CSSResultGroup = css`
        :host { display: block; }
    `;
}

export default createWidgetPlugin({
    displayName: "Number Display",
    description: "A read-only widget that displays a numeric value",
    data,
    widget: NumberDisplayWidget
});
```

**Key points:**

* The `data` object uses `as const` — this is critical for TypeScript type inference
* `this.widgetData.get("value")` returns a signal, `.get()` reads its current value
* Use nullish coalescing (`??`) to provide defaults when values are undefined
* The widget automatically re-renders when the signal value changes

## 4. Editable Widget Pattern

Most widgets allow users to edit values. Use the `isSettable` check to disable editing when the port is connected to an upstream node.

```typescript
import { WidgetElement, createWidgetPlugin } from "@graph/platform-exports/v1/widget-plugin.js";
import { html, type TemplateResult } from "lit";

const data = {
    value: {
        type: "@adobe/datatype-string",
        displayName: "Value",
        description: "The value to display and edit"
    }
} as const;

class StringWidget extends WidgetElement<typeof data> {
    public render(): TemplateResult {
        const valueSignal = this.widgetData.get("value");
        const value = valueSignal.get();
        const isSettable = this.widgetData.isSettable("value").get();

        return html`
            <sp-textfield
                .value=${value ?? ""}
                ?disabled=${!isSettable}
                @input=${this._handleInput}
            ></sp-textfield>
        `;
    }

    private _handleInput(event: Event): void {
        const target = event.target as HTMLInputElement;
        this.widgetData.set("value", target.value);
    }
}

export default createWidgetPlugin({
    displayName: "String Input",
    description: "A widget for editing string values",
    data,
    widget: StringWidget
});
```

> **Understanding isSettable:** When a port is connected to an upstream node, data flows in from that connection. In this state, `isSettable` returns `false` because the value is being provided by another node — user editing should be disabled. When `true`, the port has no incoming connection and the user can edit the value directly.

**Key points:**

* Always check `isSettable` before allowing edits
* Use `?disabled=${!isSettable}` syntax to bind the disabled state
* Call `this.widgetData.set("field", value)` to update values
* Event handlers should be private methods (prefix with `_`)

## 5. Signal API Reference

The widget data API is built on reactive signals. Here's the complete reference for the `widgetData` interface. For background on how signals work in Lit, see the [Lit Signals documentation](https://lit.dev/docs/data/signals/).

| Method | Returns | Description |
|---|---|---|
| `this.widgetData.get("field")` | `ReadonlySignal<T>` | Get the reactive signal for a data field |
| `signal.get()` | `T` | Read the current value from a signal |
| `this.widgetData.isSettable("field")` | `ReadonlySignal<boolean>` | Whether the field is editable (no upstream connection) |
| `this.widgetData.set("field", value)` | `void` | Update the field value (only works when isSettable is true) |

> Signals are reactive. When you call `signal.get()` during rendering, Lit tracks this dependency and automatically re-renders your widget when that signal changes. You don't need to manually subscribe to updates.

## 6. Data Field Properties

Each field in the `data` object defines a connection to a datatype. Here are the available properties:

| Property | Type | Required | Description |
|---|---|---|---|
| `type` | `string` | Yes | Datatype reference (e.g., `"@adobe/datatype-number"`) |
| `displayName` | `string` | Yes | Human-readable label shown in the UI |
| `description` | `string` | Yes | Tooltip/help text describing the field's purpose |
| `defaultValue` | varies | No | Default value when no value is provided by a port binding |

> **Critical:** The `data` object MUST use `as const` for proper type inference with `WidgetElement<typeof data>`. Without it, TypeScript cannot infer the correct types for your widget data fields.

## 7. Multi-Field Widgets

Widgets can operate on multiple datatype fields simultaneously. This is useful for complex controls like sliders with min/max bounds:

```typescript
const data = {
    value: {
        type: "@adobe/datatype-number",
        displayName: "Value",
        description: "The numeric value"
    },
    min: {
        type: "@adobe/datatype-number",
        displayName: "Min",
        description: "Minimum slider value",
        defaultValue: 0
    },
    max: {
        type: "@adobe/datatype-number",
        displayName: "Max",
        description: "Maximum slider value",
        defaultValue: 1
    },
    step: {
        type: "@adobe/datatype-number",
        displayName: "Step",
        description: "Step increment",
        defaultValue: 0.001
    }
} as const;

class SliderWidget extends WidgetElement<typeof data> {
    public render(): TemplateResult {
        const value = this.widgetData.get("value").get() ?? 0;
        const min = this.widgetData.get("min").get() ?? 0;
        const max = this.widgetData.get("max").get() ?? 1;
        const step = this.widgetData.get("step").get() ?? 0.001;
        const isSettable = this.widgetData.isSettable("value").get();

        return html`
            <sp-slider
                .value=${value}
                .min=${min}
                .max=${max}
                .step=${step}
                ?disabled=${!isSettable}
                @input=${this._handleInput}
            ></sp-slider>
        `;
    }

    private _handleInput(event: Event): void {
        const target = event.target as HTMLInputElement;
        this.widgetData.set("value", parseFloat(target.value));
    }
}
```

**Key points:**

* Each field maps to a datatype and can be independently bound to a port
* Fields can have different settability states — check each individually if needed
* Default values ensure the widget always has sensible bounds
* Users can connect nodes to min/max/step to dynamically control the slider range

## 8. Updating Composite Values

When a datatype is an object (like vector2 or color), you must spread the existing value and override only the changed field:

```typescript
const data = {
    value: {
        type: "@adobe/datatype-vector2",
        displayName: "Position",
        description: "2D position vector"
    }
} as const;

class Vector2Widget extends WidgetElement<typeof data> {
    public render(): TemplateResult {
        const value = this.widgetData.get("value").get() ?? { x: 0, y: 0 };
        const isSettable = this.widgetData.isSettable("value").get();

        return html`
            <div class="vector-input">
                <sp-number-field
                    .value=${value.x}
                    ?disabled=${!isSettable}
                    @input=${this._handleInputX}
                ><label slot="label">X</label></sp-number-field>
                <sp-number-field
                    .value=${value.y}
                    ?disabled=${!isSettable}
                    @input=${this._handleInputY}
                ><label slot="label">Y</label></sp-number-field>
            </div>
        `;
    }

    private _handleInputX(event: Event): void {
        const target = event.target as HTMLInputElement;
        const numValue = parseFloat(target.value);
        if (!isNaN(numValue)) {
            this.widgetData.set("value", {
                ...this.widgetData.get("value").get(),
                x: numValue
            });
        }
    }

    private _handleInputY(event: Event): void {
        const target = event.target as HTMLInputElement;
        const numValue = parseFloat(target.value);
        if (!isNaN(numValue)) {
            this.widgetData.set("value", {
                ...this.widgetData.get("value").get(),
                y: numValue
            });
        }
    }
}
```

> **Important:** Always spread the existing value with `...this.widgetData.get("value").get()` when updating composite objects. If you don't, you'll overwrite the entire object and lose other field values.

## 9. Port Widgets vs Node Widgets

Widgets can be displayed in two locations, and your design should account for the space available:

### Port Widgets

* **Location:** Displayed inline next to a port on the node
* **Space:** Very limited horizontal space
* **Best for:** Simple, compact inputs that fit on a single line
* **Examples:** Number field, toggle switch, small text field, dropdown
* **Design tip:** Keep visual footprint minimal — users should be able to see multiple ports at once

### Node Widgets

* **Location:** Displayed in the node body (center area)
* **Space:** More space available, but still constrained by node size
* **Best for:** Previews, large editors, and multi-field controls
* **Examples:** Image thumbnails, color pickers with multiple channels, text areas, graphs/charts
* **Design tip:** Use responsive layouts that adapt to node resizing

> A good rule of thumb: if the widget needs more than ~200px width or has multiple rows of controls, it's probably better suited as a node widget. Port widgets should be compact enough that users can comfortably view 3-5 of them stacked vertically.

## 10. Spectrum Web Components

Project Graph uses Adobe Spectrum Web Components for consistent UI. Here are the most commonly used components:

| Component | Use Case | Event |
|---|---|---|
| `<sp-textfield>` | Text input (add `multiline` attribute for textarea) | `@input` |
| `<sp-number-field>` | Numeric input with increment/decrement buttons | `@input` |
| `<sp-slider>` | Range slider for continuous values | `@input` |
| `<sp-switch>` | Boolean toggle switch | `@change` |
| `<sp-picker>` | Dropdown menu for selecting from options | `@change` |
| `<sp-button>` | Buttons for actions | `@click` |

**Example usage:**

```typescript
// Multiline text field
html`
    <sp-textfield
        multiline
        .value=${value}
        ?disabled=${!isSettable}
        @input=${this._handleInput}
    ><label slot="label">Description</label></sp-textfield>`;

// Number field with constraints
html`
    <sp-number-field
        .value=${value}
        .min=${0}
        .max=${100}
        .step=${1}
        ?disabled=${!isSettable}
        @input=${this._handleInput}
    ><label slot="label">Opacity %</label></sp-number-field>`;

// Switch (boolean toggle)
html`
    <sp-switch
        ?checked=${value}
        ?disabled=${!isSettable}
        @change=${this._handleChange}
    >Enable Feature</sp-switch>`;
```

> For complete documentation on Spectrum Web Components, see the [official Spectrum Web Components documentation](https://opensource.adobe.com/spectrum-web-components/).

## 11. Styling

Widgets use Lit's scoped CSS system. Styles defined in your widget only apply to that widget's shadow DOM:

```typescript
import { css, type CSSResultGroup } from "lit";

class MyWidget extends WidgetElement<typeof data> {
    static styles: CSSResultGroup = css`
        :host {
            display: block;
            padding: 8px;
        }

        .container {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .label {
            font-size: 12px;
            color: var(--spectrum-global-color-gray-700);
        }
    `;

    public render(): TemplateResult {
        return html`
            <div class="container">
                <span class="label">My Widget</span>
            </div>
        `;
    }
}
```

### Available CSS Custom Properties

The platform provides CSS custom properties for consistent theming:

* `--spectrum-global-color-gray-*` — Spectrum color tokens (50, 100, 200, ..., 900)
* `--node-tilebackground` — Background color of node tiles
* `--node-border-color` — Border color for nodes
* All standard Spectrum design tokens from `@spectrum-web-components/styles`

> **Styling best practices:**
> - Always use `:host` to style the root element
> - Prefer Spectrum design tokens over hardcoded colors
> - Use flexbox or grid for layouts — avoid fixed dimensions when possible
> - Test your widget with different node sizes to ensure responsive behavior

## 12. Advanced Features

### Lifecycle Methods

Lit provides lifecycle methods for setup and teardown. Always call `super` when overriding:

```typescript
class MyWidget extends WidgetElement<typeof data> {
    // Called when element is added to the DOM
    public connectedCallback(): void {
        super.connectedCallback();
        // Initialize event listeners, subscriptions, etc.
    }

    // Called before each render
    protected willUpdate(changedProperties: Map<string, unknown>): void {
        super.willUpdate(changedProperties);
        // Perform any pre-render computations
    }

    // Called when element is removed from the DOM
    public disconnectedCallback(): void {
        // Clean up event listeners, subscriptions, etc.
        super.disconnectedCallback();
    }
}
```

### Local State

Use the `@state()` decorator for reactive local state (state not bound to datatype fields):

```typescript
import { state } from "lit/decorators.js";

class MyWidget extends WidgetElement<typeof data> {
    @state()
    private _expanded: boolean = false;

    public render(): TemplateResult {
        return html`
            <div>
                <sp-button @click=${this._toggleExpanded}>
                    ${this._expanded ? "Collapse" : "Expand"}
                </sp-button>
                ${this._expanded ? html`<div>Expanded content</div>` : null}
            </div>
        `;
    }

    private _toggleExpanded(): void {
        this._expanded = !this._expanded;
    }
}
```

### DOM Queries

Use the `@query()` decorator to get references to rendered elements:

```typescript
import { query } from "lit/decorators.js";

class MyWidget extends WidgetElement<typeof data> {
    @query("canvas")
    private _canvas!: HTMLCanvasElement;

    public firstUpdated(): void {
        // Called after first render — DOM elements are now available
        const ctx = this._canvas.getContext("2d");
        // Draw on canvas...
    }
}
```

### Resource Management

For widgets that work with images or videos, use the resource manager to handle renditions:

```typescript
class ImageWidget extends WidgetElement<typeof data> {
    @state()
    private _renditionUrl: string | undefined;

    private _rendition: Rendition | undefined;

    public async willUpdate(changedProperties: Map<string, unknown>): Promise<void> {
        super.willUpdate(changedProperties);

        const resource = this.widgetData.get("image").get();
        if (resource && resource !== this._currentResource) {
            this._rendition?.dispose();
            this._rendition = await this.resourceManager.createRendition(
                resource,
                { maxWidth: 200, maxHeight: 200 }
            );
            this._renditionUrl = this._rendition.url;
            this._currentResource = resource;
        }
    }

    public disconnectedCallback(): void {
        this._rendition?.dispose();
        super.disconnectedCallback();
    }

    public render(): TemplateResult {
        return html`
            ${this._renditionUrl ? html`<img src=${this._renditionUrl} />` : html`<span>No image</span>`}
        `;
    }
}
```

> **Memory management:** Always dispose renditions in `disconnectedCallback()`. Failing to do so will cause memory leaks as image data accumulates in memory.

## 13. File Structure

A widget plugin follows this standard file structure:

```text
src/widget-example/
├── manifest.json            # Plugin metadata and dependencies
├── plugin.ts                # Widget implementation
└── .plugin-dependencies/    # Managed by graph install
```

### manifest.json

```json
{
    "name": "@adobe/widget-example",
    "version": "1.0",
    "platformVersion": 1,
    "dependencies": {
        "@adobe/datatype-example": {
            "majorVersion": 1
        }
    }
}
```

**Key fields:**

* `name` — Unique plugin identifier (scoped to `@adobe`)
* `platformVersion` — Always `1` for current platform
* `dependencies` — Datatypes this widget depends on (must specify major version)

## 14. Naming Conventions

Widget plugins follow a consistent naming pattern across all files and identifiers:

| Item | Pattern | Example |
|---|---|---|
| Package name | `@adobe/widget-{name}` | `@adobe/widget-number` |
| Directory name | `widget-{name}` | `src/widget-number/` |
| Class name | `{Name}Widget` | `NumberWidget` |
| Display name | Human-readable, title case | `"Number Input"` |

**Examples of well-named widgets:**

* `@adobe/widget-slider` → `SliderWidget` → "Slider"
* `@adobe/widget-textarea` → `TextAreaWidget` → "Text Area"
* `@adobe/widget-color-picker` → `ColorPickerWidget` → "Color Picker"
* `@adobe/widget-image-preview` → `ImagePreviewWidget` → "Image Preview"

> **Naming tips:**
> - Use descriptive names that indicate the widget's purpose
> - Keep names concise — avoid redundant words like "input" or "control"
> - Use kebab-case for package/directory names, PascalCase for class names
> - Display names should be user-friendly and match common UI terminology

## 15. Common Pitfalls

### Canvas sizing: avoid ResizeObserver feedback loops

Do not use `ResizeObserver` to match the canvas bitmap dimensions to its container element. The resize → repaint → resize cycle creates a layout feedback loop that causes content to overflow or drift on every resize event.

**Instead:**

* Draw the bitmap once at a capped resolution (800px max dimension)
* Use CSS `object-fit: contain` so the browser scales it responsively
* Place the canvas inside a wrapper with `position: absolute; inset: 0`
* Style the canvas itself with `max-width: 100%; max-height: 100%; object-fit: contain`

```typescript
// Avoid — triggers layout feedback loop
const observer = new ResizeObserver(entries => {
    canvas.width = entries[0].contentRect.width;
    canvas.height = entries[0].contentRect.height;
    draw();
});
observer.observe(canvas);

// Correct — draw once at capped size, CSS handles display
const MAX_DIM = 800;
const scale = Math.min(1, MAX_DIM / Math.max(bitmap.width, bitmap.height));
canvas.width = Math.round(bitmap.width * scale);
canvas.height = Math.round(bitmap.height * scale);
ctx.drawImage(bitmap, 0, 0, canvas.width, canvas.height);
```

```typescript
static styles: CSSResultGroup = css`
    .wrapper {
        position: absolute;
        inset: 0;
    }
    canvas {
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
    }
`;

public render(): TemplateResult {
    return html`<div class="wrapper"><canvas></canvas></div>`;
}
```

## 16. Next Steps

Now that you understand widget development, here are some recommended next steps:

* **[Widget Design Guidelines](../widget-design-guidelines/index.md)** — Visual design patterns, sizing conventions, and when to create a new widget vs. reuse an existing one
* **[Developing Nodes](../developing-nodes/index.md)** — Learn how to bind your widgets to node ports for inline editing and preview
* **[Developing Datatypes](../developing-datatypes/index.md)** — Understanding datatypes is essential for effective widget design

<InlineAlert variant="info" slots="text"/>

**Need help?** Reach out to the Graph team in the [#prj-graph-plugins](https://adobe.enterprise.slack.com/archives/C0ANK4FL49W) Slack channel.
