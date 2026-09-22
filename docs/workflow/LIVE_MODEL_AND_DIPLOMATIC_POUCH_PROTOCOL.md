# Live Model and Diplomatic Pouch Protocol

Status: WORKING PROJECT PROTOCOL.

## State model

The project has three ordinary synchronization states:

1. **SYNCED** — Git represents the latest sealed live-model checkpoint.
2. **THREAD AHEAD** — the active ChatGPT thread contains accepted work newer than Git.
3. **POUCH PENDING** — a sealed diplomatic pouch contains a delta that has not yet been integrated by Codex.

Git is the last sealed checkpoint. The active ChatGPT thread is the live working model. A Diplomatic Pouch serializes the accepted delta between them. Codex is the local integration/commit bridge.

## Session opening

When repository access is available:

1. read/audit GitHub;
2. record the verified repository HEAD;
3. identify any known pending pouch;
4. treat that state as the session baseline.

DP-002 baseline:

`ea6af06aa35015b26d62f1beca781bc870c90743`

## During work

Do not interrupt design merely to keep Git synchronized sentence by sentence. Accumulate accepted work in the live model.

Brainstorming is not automatically canon. The reconciliation step separates accepted decisions/specifications from exploratory discussion.

## Closing a meaningful checkpoint

At a meaningful thread/session boundary:

1. pull/read current Git;
2. compare Git with the accepted live model;
3. identify what the thread knows that Git does not;
4. package only that delta;
5. record the parent Git SHA;
6. record materially used external sources;
7. preserve OPEN questions;
8. include Codex integration instructions and an audit;
9. seal the pouch.

A chat thread does not require a pouch if it produced no meaningful accepted delta.

## Codex integration

Codex must inspect current local/remote Git before applying a pouch. A pouch baseline is not authorization to reset newer work.

Codex reconciles, validates, commits, and pushes. The resulting GitHub commit is then independently audited from the ChatGPT thread.

## Return path

Normal return path:

Codex -> Git commit -> GitHub -> ChatGPT audit.

A return ZIP is exceptional and is reserved for artifacts that should not reasonably live in Git.

## Governing shorthand

Git = sealed checkpoint.
Thread = live model.
Pouch = delta.
Codex = commit bridge.
GitHub = synchronization surface.
