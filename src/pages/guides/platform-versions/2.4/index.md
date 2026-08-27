---
title: Platform 2.4 Libraries - Firefly Graph
description: Libraries and import specifiers available to plugins targeting Graph platform version 2.4.
---

# Platform 2.4 — Available Libraries

This page lists every library a plugin can import when it targets Graph platform **2.4**. To target this release, set `platformVersion` to `{ "major": 2, "minor": 4 }` in the plugin's manifest. Each library below is provided by the platform at runtime, so you import it directly — there's no need to add it to your project's dependencies. Versions are the ranges guaranteed available in this release.

See [Platform Versioning](../../platform-versioning/index.md) for how targeting and runtime compatibility work, and the [reference index](../index.md) for the other platform versions.

**On this page:**

* [lit](#lit)
* [@lit-labs/signals](#lit-labssignals)
* [signal-utils](#signal-utils)
* [@lit/context](#litcontext)
* [@graph/resources](#graphresources)
* [@graph/graph-icons](#graphgraph-icons)
* [@graph/platform-exports](#graphplatform-exports)
* [mediabunny](#mediabunny)
* [@spectrum-web-components/action-button](#spectrum-web-componentsaction-button)
* [@spectrum-web-components/action-menu](#spectrum-web-componentsaction-menu)
* [@spectrum-web-components/button](#spectrum-web-componentsbutton)
* [@spectrum-web-components/dialog](#spectrum-web-componentsdialog)
* [@spectrum-web-components/field-label](#spectrum-web-componentsfield-label)
* [@spectrum-web-components/icon](#spectrum-web-componentsicon)
* [@spectrum-web-components/icons-workflow](#spectrum-web-componentsicons-workflow)
* [@spectrum-web-components/menu](#spectrum-web-componentsmenu)
* [@spectrum-web-components/number-field](#spectrum-web-componentsnumber-field)
* [@spectrum-web-components/picker](#spectrum-web-componentspicker)
* [@spectrum-web-components/radio](#spectrum-web-componentsradio)
* [@spectrum-web-components/slider](#spectrum-web-componentsslider)
* [@spectrum-web-components/switch](#spectrum-web-componentsswitch)
* [@spectrum-web-components/textfield](#spectrum-web-componentstextfield)
* [@spectrum-web-components/color-slider](#spectrum-web-componentscolor-slider)
* [@spectrum-web-components/color-area](#spectrum-web-componentscolor-area)

## Libraries

### lit

**Version:** `^3.2.0`

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

### @lit-labs/signals

**Version:** `^0.1.3`

```text
@lit-labs/signals
```

### signal-utils

**Version:** `^0.21.1`

```text
signal-utils
signal-utils/subtle/microtask-effect
signal-utils/subtle/reaction
```

### @lit/context

**Version:** `^1.1.5`

```text
@lit/context
```

### @graph/resources

**Version:** `^1.0.0`

```text
@graph/resources
```

### @graph/graph-icons

**Version:** `^0.1.1`

```text
@graph/graph-icons/pg-icon-blend-mode.js
```

### @graph/platform-exports

**Version:** `^1.0.0`

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

### mediabunny

**Version:** `^1.34.2`

```text
mediabunny
```

### @spectrum-web-components/action-button

**Version:** `^1.7.0`

```text
@spectrum-web-components/action-button
@spectrum-web-components/action-button/sp-action-button.js
```

### @spectrum-web-components/action-menu

**Version:** `^1.7.0`

```text
@spectrum-web-components/action-menu
@spectrum-web-components/action-menu/sp-action-menu.js
```

### @spectrum-web-components/button

**Version:** `^1.7.0`

```text
@spectrum-web-components/button
@spectrum-web-components/button/sp-button.js
```

### @spectrum-web-components/dialog

**Version:** `^1.7.0`

```text
@spectrum-web-components/dialog
@spectrum-web-components/dialog/sp-dialog.js
@spectrum-web-components/dialog/sp-dialog-wrapper.js
```

### @spectrum-web-components/field-label

**Version:** `^1.7.0`

```text
@spectrum-web-components/field-label
@spectrum-web-components/field-label/sp-field-label.js
```

### @spectrum-web-components/icon

**Version:** `^1.7.0`

```text
@spectrum-web-components/icon/sp-icon.js
```

### @spectrum-web-components/icons-workflow

**Version:** `^1.7.0`

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
@spectrum-web-components/icons-workflow/icons/sp-icon-shuffle.js
```

### @spectrum-web-components/menu

**Version:** `^1.7.0`

```text
@spectrum-web-components/menu
@spectrum-web-components/menu/sp-menu.js
@spectrum-web-components/menu/sp-menu-item.js
@spectrum-web-components/menu/sp-menu-group.js
@spectrum-web-components/menu/sp-menu-divider.js
```

### @spectrum-web-components/number-field

**Version:** `^1.7.0`

```text
@spectrum-web-components/number-field
@spectrum-web-components/number-field/sp-number-field.js
```

### @spectrum-web-components/picker

**Version:** `^1.7.0`

```text
@spectrum-web-components/picker
@spectrum-web-components/picker/sp-picker.js
```

### @spectrum-web-components/radio

**Version:** `^1.7.0`

```text
@spectrum-web-components/radio
@spectrum-web-components/radio/sp-radio.js
@spectrum-web-components/radio/sp-radio-group.js
```

### @spectrum-web-components/slider

**Version:** `^1.7.0`

```text
@spectrum-web-components/slider
@spectrum-web-components/slider/sp-slider.js
```

### @spectrum-web-components/switch

**Version:** `^1.7.0`

```text
@spectrum-web-components/switch
@spectrum-web-components/switch/sp-switch.js
```

### @spectrum-web-components/textfield

**Version:** `^1.7.0`

```text
@spectrum-web-components/textfield
@spectrum-web-components/textfield/sp-textfield.js
```

### @spectrum-web-components/color-slider

**Version:** `^1.7.0`

```text
@spectrum-web-components/color-slider
@spectrum-web-components/color-slider/sp-color-slider.js
```

### @spectrum-web-components/color-area

**Version:** `^1.7.0`

```text
@spectrum-web-components/color-area
@spectrum-web-components/color-area/sp-color-area.js
```
