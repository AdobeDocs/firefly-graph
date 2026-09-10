# Contributing

Thanks for choosing to contribute!

The following are a set of guidelines to follow when contributing to this project.

## Source of Truth for the Plugin Development Guide

The handwritten **Plugin Development Guide** (the pages under `src/pages/guides/`,
excluding the auto-generated `platform-versions/` reference) is **no longer
authored in this repository**. Its authoritative source now lives in the Graph
monorepo, co-located with `@graph/platform-exports`:

> `packages/platform-exports/plugin-development-guide/` in
> [Adobe-CreativeCloud/graph](https://github.com/Adobe-CreativeCloud/graph)

Those pages here are published/synced from the monorepo and will be overwritten —
**do not hand-edit them in this repo**. To change the guide, open a PR against the
monorepo source instead.

What is still maintained here:

- The **Platform Library Reference** under `src/pages/guides/platform-versions/`,
  which is auto-generated per platform version by `scripts/gen-platform-pages.py`
  and `scripts/sync-platform-versions.py` (see `scripts/README.md`).
- Site scaffolding — the landing page, navigation config, and support pages.

## Code Of Conduct

This project adheres to the Adobe [code of conduct](../CODE_OF_CONDUCT.md). By participating,
you are expected to uphold this code. Please report unacceptable behavior to
[Grp-opensourceoffice@adobe.com](mailto:Grp-opensourceoffice@adobe.com).

## Have A Question?

Start by filing an issue. The existing committers on this project work to reach
consensus around project direction and issue solutions within issue threads
(when appropriate).

## Contributor License Agreement

All third-party contributions to this project must be accompanied by a signed contributor
license agreement. This gives Adobe permission to redistribute your contributions
as part of the project. [Sign our CLA](https://opensource.adobe.com/cla.html). You
only need to submit an Adobe CLA one time, so if you have submitted one previously,
you are good to go!

## Code Reviews

All submissions should come in the form of pull requests and need to be reviewed
by project committers. Read [GitHub's pull request documentation](https://help.github.com/articles/about-pull-requests/)
for more information on sending pull requests.

Lastly, please follow the [pull request template](PULL_REQUEST_TEMPLATE.md) when
submitting a pull request!

## From Contributor To Committer

We love contributions from our community! If you'd like to go a step beyond contributor
and become a committer with full write access and a say in the project, you must
be invited to the project. The existing committers employ an internal nomination
process that must reach lazy consensus (silence is approval) before invitations
are issued. If you feel you are qualified and want to get more deeply involved,
feel free to reach out to existing committers to have a conversation about that.

## Security Issues

Security issues shouldn't be reported on this issue tracker. Instead, [file an issue to our security experts](https://helpx.adobe.com/security/alertus.html).
