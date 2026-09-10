# Versioned-docs information architecture

Status: accepted — design input for the versioned-docs work under [GRAPH-645](https://jira.corp.adobe.com/browse/GRAPH-645).
Source decision: [GRAPH-3999](https://jira.corp.adobe.com/browse/GRAPH-3999) spike (Model A retention).
This document: [GRAPH-4217](https://jira.corp.adobe.com/browse/GRAPH-4217).

This is the maintainer-facing map of how the plugin developer documentation is organized
across content that changes on a different cadence than the docs site itself. It exists so
that anyone touching the docs — or building the firefly-graph publish workflow
([GRAPH-4216](https://jira.corp.adobe.com/browse/GRAPH-4216)) — knows which content class a
page belongs to, where its source of truth lives, who edits it, and when it is republished.

It does **not** implement the publish workflow, the CI gate, or the guide migration. Those
are separate stories (see [Related stories](#related-stories)).

## The three content classes

Plugin documentation splits into three classes by **how often it changes** and **what it is
pinned to**:

| Class | Pinned to | Source of truth | Who authors | Republished when |
|---|---|---|---|---|
| **(a) Concepts** — version-agnostic | nothing | firefly-graph (`src/pages/guides/`) | docs maintainers, by hand | any time; no version coupling |
| **(b) Plugin Development Guide** — the handwritten guide | platform **major** | monorepo, co-located with `@graph/platform-exports` | plugin-platform engineers, by hand | every platform **major** bump |
| **(c) Platform Library Reference** — available-modules list | platform **minor** | `platform-modules.json` in the versioned platform bundle | **auto-generated**, no human author | every platform **minor** bump |

The guiding principle from the [GRAPH-3999](https://jira.corp.adobe.com/browse/GRAPH-3999)
spike: separate the general principles/concepts (class a) from the per-platform-version
guide (class b), and generate the interface/module surface from the platform source rather
than hand-maintaining it (class c). There is intentionally **no** TypeDoc / auto-extracted
prose API reference — class (b) stays handwritten.

### (a) Version-agnostic concepts

Principles, philosophy, and process that hold regardless of which platform version a plugin
targets. These stay authored directly in firefly-graph and are edited on their own schedule.

Current pages in this class:

- [Core Concepts](../src/pages/guides/core-concepts/index.md) — how the plugin system is architected (datatype/widget/node relationships, load/resolve model, data lifecycle).
- [How to Think About Nodes](../src/pages/guides/how-to-think-about-nodes/index.md) — node design philosophy and anti-patterns.
- [Widget Design Guidelines](../src/pages/guides/widget-design-guidelines/index.md) — visual/interaction guidelines for widgets.
- [Plugin Versioning](../src/pages/guides/plugin-versioning/index.md) — how a plugin author versions their own plugin.
- [Platform Versioning](../src/pages/guides/platform-versioning/index.md) — how the platform is versioned and how plugins target a `major.minor`.
- [Submitting Plugins](../src/pages/guides/submitting-plugins/index.md) — the submission and review process.

### (b) The per-major handwritten guide

The hands-on Plugin Development Guide: how to build each plugin type against the interfaces
of the **current platform major**. Because these pages describe interface shapes that change
across majors, their source of truth moves to the monorepo, co-located with
`@graph/platform-exports`, so a single PR can carry a major bump and the guide rewrite
together and CI can gate on both ([GRAPH-4212](https://jira.corp.adobe.com/browse/GRAPH-4212),
[GRAPH-4213](https://jira.corp.adobe.com/browse/GRAPH-4213)). firefly-graph publishes the
snapshot for the current major.

Current pages in this class:

- [Creating Plugins](../src/pages/guides/creating-plugins/index.md)
- [Developing Datatypes](../src/pages/guides/developing-datatypes/index.md)
- [Developing Widgets](../src/pages/guides/developing-widgets/index.md)
- [Developing Nodes](../src/pages/guides/developing-nodes/index.md)
- [Developing Utilities](../src/pages/guides/developing-utilities/index.md)
- [CLI Reference](../src/pages/guides/cli-reference/index.md) — travels with the handwritten guide bundle (tracks the `graph` CLI, which resolves the per-major/minor platform bundle).

Until the migration in [GRAPH-4212](https://jira.corp.adobe.com/browse/GRAPH-4212) lands,
these pages still live in firefly-graph. This IA describes the **target** home; the
migration story moves the source and wires up publishing.

### (c) The per-minor auto-generated available-modules list

The [Platform Library Reference](../src/pages/guides/platform-versions/index.md): exactly
which libraries, versions, and import specifiers each platform release provides. One page per
`major.minor`, generated from the authoritative `platform-modules.json` inside each version's
`graph-platform-exports-*.tgz` bundle.

- Generator: [`scripts/gen-platform-pages.py`](../scripts/gen-platform-pages.py). It writes
  `src/pages/guides/platform-versions/<version>/index.md` for every version plus the section
  index, and marks the newest version `— latest`.
- Existing firefly pipeline (from GRAPH-3604): `sync-platform-versions.py` +
  `gen-platform-pages.py` + `check-platform-version.yml` keep this list current on every
  platform **minor** bump with no human doc work.
- **Do not hand-edit** the `platform-versions/` pages or their index — they are overwritten
  on every generator run. Change the generator, not the output.

## Retention — Model A

Per the [GRAPH-3999](https://jira.corp.adobe.com/browse/GRAPH-3999) decision:

- **One live guide.** The monorepo holds a single live (current-major) copy of the
  handwritten guide (class b). Previous majors are recovered from **git history** — there are
  no per-major duplicate directories in the monorepo source.
- **Published history in firefly-graph.** The versioned platform bundle snapshots the guide
  per major, and firefly-graph retains the published historical majors — the same way
  `platform-versions/<v>` pages are retained today for class (c). So a reader can still reach
  an older major's guide on the published site even though the monorepo keeps only the
  current one in-tree.
- **Minor bumps** only regenerate class (c). The guide (class b) is not required to change on
  a minor; editing it on a minor is allowed but not required. **Major bumps** rewrite the
  guide, and CI blocks the PR when the guide directory was not touched
  ([GRAPH-4213](https://jira.corp.adobe.com/browse/GRAPH-4213)).

## The "current" pointer

Each versioned class needs a stable entry point that always resolves to the newest published
release, so links and nav do not have to be re-pointed on every bump:

- **Class (b), the guide:** "current" = the guide snapshot for the **current published
  major**. The site navigation surfaces the guide as the current-major guide; older majors
  are reachable through the published history retained in firefly-graph (Model A). The
  firefly publish workflow ([GRAPH-4216](https://jira.corp.adobe.com/browse/GRAPH-4216))
  owns pointing "current" at the newest major snapshot as it pulls each new one.
- **Class (c), the library reference:** the generated index already marks the newest version
  `— latest` and is the stable "current" entry point for the reference. Recommended for
  GRAPH-4216: expose a stable alias (e.g. `platform-versions/current`) that redirects to the
  latest version page, so external links survive minor bumps. This IA reflects "current" as a
  nav label and index marker; the alias/redirect itself is publish-workflow scope, not
  hand-authored content (it must not become a stale checked-in page).

## How the site navigation reflects the split

`src/pages/config.md` (hand-maintained; not auto-generated) groups the left-sidebar entries
under the Plugin Developer Guide into the three classes, and `src/pages/guides/index.md`
introduces the guide with the same three-way split and a "current" note. The grouping makes
each page's class — and therefore its source of truth and update cadence — legible from the
nav alone:

- **Concepts (version-agnostic)** — class (a)
- **Plugin Development Guide (current major)** — class (b)
- **Platform Library Reference (per-minor, auto-generated)** — class (c), "Current release"
  entry points at the generated index that marks the latest version.

## Related stories

All under epic [GRAPH-645](https://jira.corp.adobe.com/browse/GRAPH-645):

- [GRAPH-4212](https://jira.corp.adobe.com/browse/GRAPH-4212) — migrate the handwritten guide source into the monorepo (co-located with platform-exports).
- [GRAPH-4213](https://jira.corp.adobe.com/browse/GRAPH-4213) — CI gate: block platform major bumps when the guide is not updated.
- [GRAPH-4214](https://jira.corp.adobe.com/browse/GRAPH-4214) — include the handwritten guide in the versioned platform bundle/closure.
- [GRAPH-4215](https://jira.corp.adobe.com/browse/GRAPH-4215) — provision the guide into `.platform-dependencies` on `graph install`.
- [GRAPH-4216](https://jira.corp.adobe.com/browse/GRAPH-4216) — firefly-graph: publish per-major guide snapshots and retain history (keep per-minor module auto-gen). **This IA is the design input for that story.**
- [GRAPH-4217](https://jira.corp.adobe.com/browse/GRAPH-4217) — this document.
