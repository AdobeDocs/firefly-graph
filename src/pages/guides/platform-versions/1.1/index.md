---
title: Platform 1.1 Libraries - Firefly Graph
description: Libraries and import specifiers available to plugins targeting Graph platform version 1.1.
---

# Platform 1.1 — Available Libraries

This page lists every library a plugin can import when it targets Graph platform **1.1**. To target this release, set `platformVersion` to `{ "major": 1, "minor": 1 }` in the plugin's manifest. Each library below is provided by the platform at runtime, so you import it directly — there's no need to add it to your project's dependencies. Versions are the ranges guaranteed available in this release.

See [Platform Versioning](../../platform-versioning/index.md) for how targeting and runtime compatibility work, and the [reference index](../index.md) for the other platform versions.

## Libraries

### lit — `^3.2.0`

```text
lit
lit/decorators.js
lit/directives/async-append.js
lit/directives/async-replace.js
lit/directives/cache.js
lit/directives/choose.js
lit/directives/class-map.js
lit/directives/guard.js
lit/directives/if-defined.js
lit/directives/join.js
lit/directives/keyed.js
lit/directives/live.js
lit/directives/map.js
lit/directives/range.js
lit/directives/ref.js
lit/directives/repeat.js
lit/directives/style-map.js
lit/directives/template-content.js
lit/directives/unsafe-html.js
lit/directives/unsafe-svg.js
lit/directives/until.js
lit/directives/when.js
```

### @lit-labs/signals — `^0.1.3`

```text
@lit-labs/signals
```

### signal-utils — `^0.21.1`

```text
signal-utils
signal-utils/subtle/microtask-effect
signal-utils/subtle/reaction
```

### @lit/context — `^1.1.5`

```text
@lit/context
```

### @graph/resources — `^1.0.0`

```text
@graph/resources
```

### @graph/graph-icons — `^0.1.1`

```text
@graph/graph-icons/pg-icon-blend-mode.js
```

### @graph/platform-exports — `^1.0.0`

```text
@graph/platform-exports/node-plugin.js
@graph/platform-exports/widget-plugin.js
@graph/platform-exports/utility-plugin.js
@graph/platform-exports/datatype-plugin.js
@graph/platform-exports/events/widget-event-types.js
@graph/platform-exports/v1/node-plugin.js
@graph/platform-exports/v1/widget-plugin.js
@graph/platform-exports/v1/utility-plugin.js
@graph/platform-exports/v1/datatype-plugin.js
@graph/platform-exports/viewport-context.js
@graph/platform-exports/v1/viewport-context.js
```

### mediabunny — `^1.34.2`

```text
mediabunny
```

### @spectrum-web-components/action-button — `^1.7.0`

```text
@spectrum-web-components/action-button
@spectrum-web-components/action-button/sp-action-button.js
```

### @spectrum-web-components/action-menu — `^1.7.0`

```text
@spectrum-web-components/action-menu
@spectrum-web-components/action-menu/sp-action-menu.js
```

### @spectrum-web-components/button — `^1.7.0`

```text
@spectrum-web-components/button
@spectrum-web-components/button/sp-button.js
```

### @spectrum-web-components/dialog — `^1.7.0`

```text
@spectrum-web-components/dialog
@spectrum-web-components/dialog/sp-dialog.js
@spectrum-web-components/dialog/sp-dialog-wrapper.js
```

### @spectrum-web-components/field-label — `^1.7.0`

```text
@spectrum-web-components/field-label
@spectrum-web-components/field-label/sp-field-label.js
```

### @spectrum-web-components/icon — `^1.7.0`

```text
@spectrum-web-components/icon/sp-icon.js
```

### @spectrum-web-components/icons-workflow — `^1.7.0`

```text
@spectrum-web-components/icons-workflow/icons/sp-icon-image.js
@spectrum-web-components/icons-workflow/icons/sp-icon-add-content.js
@spectrum-web-components/icons-workflow/icons/sp-icon-revert.js
@spectrum-web-components/icons-workflow/icons/sp-icon-download.js
@spectrum-web-components/icons-workflow/icons/sp-icon-delete.js
@spectrum-web-components/icons-workflow/icons/sp-icon-visibility.js
@spectrum-web-components/icons-workflow/icons/sp-icon-visibility-off.js
@spectrum-web-components/icons-workflow/icons/sp-icon-align-left.js
@spectrum-web-components/icons-workflow/icons/sp-icon-align-center.js
@spectrum-web-components/icons-workflow/icons/sp-icon-align-right.js
@spectrum-web-components/icons-workflow/icons/sp-icon-align-top.js
@spectrum-web-components/icons-workflow/icons/sp-icon-align-middle.js
@spectrum-web-components/icons-workflow/icons/sp-icon-align-bottom.js
@spectrum-web-components/icons-workflow/icons/sp-icon-checkmark-circle.js
@spectrum-web-components/icons-workflow/icons/sp-icon-chevron-left.js
@spectrum-web-components/icons-workflow/icons/sp-icon-chevron-right.js
@spectrum-web-components/icons-workflow/icons/sp-icon-close-circle.js
@spectrum-web-components/icons-workflow/icons/sp-icon-flag.js
@spectrum-web-components/icons-workflow/icons/sp-icon-more.js
@spectrum-web-components/icons-workflow/icons/sp-icon-lock-open.js
@spectrum-web-components/icons-workflow/icons/sp-icon-lock-closed.js
@spectrum-web-components/icons-workflow/icons/sp-icon-rename.js
```

### @spectrum-web-components/menu — `^1.7.0`

```text
@spectrum-web-components/menu
@spectrum-web-components/menu/sp-menu.js
@spectrum-web-components/menu/sp-menu-item.js
@spectrum-web-components/menu/sp-menu-group.js
@spectrum-web-components/menu/sp-menu-divider.js
```

### @spectrum-web-components/number-field — `^1.7.0`

```text
@spectrum-web-components/number-field
@spectrum-web-components/number-field/sp-number-field.js
```

### @spectrum-web-components/picker — `^1.7.0`

```text
@spectrum-web-components/picker
@spectrum-web-components/picker/sp-picker.js
```

### @spectrum-web-components/radio — `^1.7.0`

```text
@spectrum-web-components/radio
@spectrum-web-components/radio/sp-radio.js
@spectrum-web-components/radio/sp-radio-group.js
```

### @spectrum-web-components/slider — `^1.7.0`

```text
@spectrum-web-components/slider
@spectrum-web-components/slider/sp-slider.js
```

### @spectrum-web-components/switch — `^1.7.0`

```text
@spectrum-web-components/switch
@spectrum-web-components/switch/sp-switch.js
```

### @spectrum-web-components/textfield — `^1.7.0`

```text
@spectrum-web-components/textfield
@spectrum-web-components/textfield/sp-textfield.js
```

### @spectrum-web-components/color-slider — `^1.7.0`

```text
@spectrum-web-components/color-slider
@spectrum-web-components/color-slider/sp-color-slider.js
```

### @spectrum-web-components/color-area — `^1.7.0`

```text
@spectrum-web-components/color-area
@spectrum-web-components/color-area/sp-color-area.js
```
