---
title: Plugin Versioning - Firefly Graph
description: How plugin versions work — the major.minor format, what counts as a breaking change, and how versions are assigned during review.
---

# Plugin Versioning

This page explains how your plugins are versioned: the `major.minor` format, the line between a breaking change and a safe one, and how the version is actually assigned when you submit. The one idea to hold onto is simple — if a change *might* alter what an existing graph produces, it's major; if it *cannot*, it's minor. Everything below is that rule, spelled out. Platform versioning (which release of the Graph API your plugin targets) is separate, and lives in [Platform Versioning](../platform-versioning/index.md).

## Version Format

Plugin versions are **`major.minor`** — two numbers, no patch:

* **Major** — a change that *might* alter a graph's output or break a dependency contract another plugin relies on.
* **Minor** — a change that is guaranteed safe and cannot affect runtime output.

`1.0`, `1.4`, `2.0` are valid. `1.0.3` is not — there is no third number.

Datatypes are the exception: they aren't versioned at all (see [By Plugin Type](#by-plugin-type)).

## Versions Are Assigned at Review

You don't unilaterally set your published version number. You *propose* one, and a reviewer confirms or adjusts it:

1. You submit your source, your manifest, a changelog, and the `major.minor` bump you think the change warrants.
2. Automated checks run a structural diff, analyze port topology, and detect metadata-only changes.
3. A reviewer sets the final version — approving your proposed minor, or escalating to major if the change carries any behavior risk.
4. The version increments on publish.

Because the reviewer has the last word, propose honestly. Marking a behavior-changing edit as minor won't get it through; it'll come back as a major.

## What Counts as a Major Change

A change is major if it *may* produce different output in an existing graph, or break what developers depending on your plugin expect. Picture a node that draws a border on an image: if the border looks different after an update, every graph using that node now produces something else, so the change is breaking. If `2 + 2` started returning `5`, same story, just more obvious.

**Behavioral and output changes** — anything that could change what the plugin produces, even subtly:

* Logic or implementation changes
* Altered algorithmic defaults
* Bug fixes that change behavior (as opposed to fixing a crash)
* Behavioral differences in generative nodes

**Port changes:**

* Removing any port
* Adding a port whose default value alters output
* Adding a required port
* Changing how a port's value is interpreted
* Changing a port's type
* Changing a default value (unless the port is already connected in the graph, which overrides the default)

**Hidden cases** — often only caught in review:

* A dependency update that changes behavior
* A node's behavior shifting indirectly through a widget or resource it uses
* Anything a reviewer flags as behavior-impacting

**Security-critical** — a version found to contain harmful code (a crypto miner, say) is revoked, and that revocation cascades to anything depending on it.

## What Counts as a Minor Change

A change is minor if it can *never* change runtime output.

**Always minor:**

* Localization changes
* Reordering ports
* Non-port metadata — tags, description, display names
* Widget-only UI changes that don't affect port binding
* Performance improvements, as long as outputs stay the same
* Adding an optional port whose default doesn't affect output
* Adding a new output port, leaving existing outputs unchanged

**Minor only if a reviewer confirms no behavior impact:**

* Bug fixes that don't affect output
* Implementation changes proven to keep outputs identical
* Dependency updates that don't trigger behavior changes
* Default-value changes, but only when a graph already overrides that default

## The Bump Decision Table

| Change | Version |
|---|---|
| Localization change | Minor |
| Port reordering | Minor |
| Metadata change (not port schema) | Minor |
| Widget change (UI only) | Minor |
| New optional port (no behavior change) | Review required — minor if safe |
| Bug fix | Review required |
| Implementation change | Review required |
| Default value change | Major |
| Port removal | Major |

## By Plugin Type

The same principle applies everywhere, but the details differ by type:

* **Nodes** — always versioned. Nodes drive versioning for the whole ecosystem, and most changes land in reviewer judgment because behavior impact is hard to prove automatically.
* **Widgets** — versioned, because nodes bind to them explicitly. Major means breaking the node-to-widget binding contract; minor means UI-only or metadata changes. Widgets don't auto-upgrade.
* **Utilities and resources** — versioned, because node authors depend on them. Major means a breaking API change; minor means a change that's provably safe.
* **Datatypes** — not versioned. Datatypes are strictly additive and backward compatible, so there's no version to bump.

## Upgrade Semantics

A published graph only upgrades a plugin to a new version automatically when the change can't affect it — specifically when:

* Only metadata changed, or
* A default value changed but the port is already connected in the graph (so the default is moot), or
* An optional port was added and its default doesn't affect behavior.

Any change that could shift output — behavioral changes, or port changes beyond the trivial metadata-only cases — does not upgrade automatically. Consumers stay on their current version until they choose to move.

## How This Connects to Submission

You set your proposed `version` in each plugin's manifest, then run `graph submit` to send the whole project for review, where the final version is confirmed. The [channel](../submitting-plugins/index.md#channels-and-versioning) you submit to controls who receives the build. See [Submitting Plugins](../submitting-plugins/index.md) for the full flow.
