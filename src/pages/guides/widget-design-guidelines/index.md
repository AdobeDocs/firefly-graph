---
title: Widget Design Guidelines - Firefly Graph
description: Visual design guidelines for building widgets consistent with the Project Graph design system.
---

# Widget Design Guidelines

This section provides visual design guidelines for building widgets that are consistent with the Project Graph design system. Well-designed widgets enhance the user experience by providing familiar, intuitive interactions for data editing and visualization.

## Key Design Principles

**Compact by default**: Port widgets must be as small as possible since they share space with ports. Design for the minimum viable interaction surface.

**Two states**: Every widget must handle both read-only (connected) and editable (disconnected) states. The read-only state should clearly show the current value without affordances for editing.

**Spectrum consistency**: Use Spectrum Web Components and design tokens for visual consistency with the broader Adobe ecosystem.

**Accessible**: Widgets must be keyboard-navigable and meet WCAG 2.1 AA contrast requirements.

**Dark theme first**: The Graph Editor uses a dark theme. Design and test widgets in dark mode first.

## When to Create a New Widget

Before building a new widget, check whether an existing widget — or a composition of existing widgets — can meet your needs.

### Use an existing widget when:

* Your datatype is composed of primitive types (`datatype-number`, `datatype-string`, `datatype-boolean`). The platform auto-generates a composite widget by rendering each field using its registered default widget — no custom widget needed.
* An existing widget handles the interaction pattern you need (slider for ranges, color picker for colors, text area for long text).
* The difference between your needs and an existing widget is purely aesthetic. Prefer consistent UX over custom styling.

### Create a new widget when:

* No existing widget can adequately represent or edit your datatype's values (e.g., a canvas-based 2D point picker, an audio waveform display, an image thumbnail with crop handles).
* Your datatype's editing interactions are fundamentally different from any existing widget (e.g., drag-to-set rather than type-to-set).
* Your datatype is a resource type (image, video, audio) that requires asset loading and rendition management.

### Rule of thumb

Start with `defaultWidget` on your datatype. If the auto-generated composite widget is adequate, stop there. Only invest in a custom widget when the interaction quality matters enough to justify the ongoing maintenance cost.

## Port Widget Layout

Port widgets are rendered inline, next to a port label on the node's port row. Space is highly constrained.

### Sizing behavior

The port component uses CSS container queries to adapt widget visibility to available width:

| Container width | Behavior |
|---|---|
| ≥ 300px | Port pip + label + widget all visible |
| 200–299px | Port pip + truncated label + widget (may be tight) |
| < 200px | Port pip + truncated label only — widget is hidden |

Design your port widget assuming it may receive as little as 200px of horizontal space. At this size, only the most essential control should be visible.

### CSS guidelines for port widgets

Always set `:host { display: block; }` on your widget element. The port component controls available width — your widget fills its container with `flex: 1`. Never set a fixed width.

```css
:host {
    display: block;
    /* Do not set a fixed width — the port container controls your available space */
}

.container {
    min-width: 0; /* Allow content to shrink rather than overflow */
}
```

## Node Widget Layout

Node widgets are rendered in the node body, separate from any port row. They have significantly more space available but must still be responsive — users can resize nodes.

### CSS guidelines for node widgets

```css
:host {
    display: block;
    width: 100%;
    min-height: 120px; /* Establish a sensible default — avoid fixed height */
}
```

* Use `width: 100%` to fill the available node body width.
* Use `min-height` rather than `height` to allow the node to grow with its content.
* Use `overflow: hidden` or `overflow: auto` if content may exceed node dimensions.
* Test at multiple node sizes — your widget should degrade gracefully as the node is resized.

## Spectrum Design Tokens

Use Spectrum CSS custom properties for consistent theming. Never hardcode colors.

| Token | Use |
|---|---|
| `--spectrum-global-color-gray-50` … `gray-900` | Grays from near-white to near-black |
| `--spectrum-global-color-blue-400` | Primary action color |
| `--node-tilebackground` | Node background color |
| `--node-border-color` | Node border |
| `--pg-spacing-xs`, `--pg-spacing-sm`, `--pg-spacing-md`, `--pg-spacing-lg` | Standard spacing scale |

All standard Spectrum design tokens from `@spectrum-web-components/styles` are also available.

## Planned Sections

The following sections are still being developed:

* **Read-Only vs Editable States** — Visual language for connected (read-only) vs disconnected (editable) ports
* **Type Color Coding** — How data types map to port and connection colors
* **Figma Component Library** — Reusable design components for prototyping widgets

## Related Resources

* For implementation guidance, see [Developing Widgets](../developing-widgets/index.md)
* For Spectrum Web Components, visit the [Spectrum Web Components documentation](https://opensource.adobe.com/spectrum-web-components/)

<InlineAlert variant="success" slots="text"/>

**Next:** [Developing Nodes](../developing-nodes/index.md) — Build computational nodes with typed input and output ports, and bind your widgets for inline editing and preview.

<InlineAlert variant="info" slots="text"/>

**Need help?** Reach out to the Graph team in the [#prj-graph-plugins](https://adobe.enterprise.slack.com/archives/C0ANK4FL49W) Slack channel.
