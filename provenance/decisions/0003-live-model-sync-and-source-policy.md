# 0003 — Live-model synchronization and external-source policy

Date: 2026-09-22
Status: working operational decision.

Accepted:
- Git is the last sealed project checkpoint, not necessarily the instantaneous live state during a ChatGPT work session.
- The active thread is the live model.
- A Diplomatic Pouch is the accepted delta between the verified Git baseline and the live model.
- Codex is the local Git integration/commit bridge.
- GitHub is the synchronization surface used for the normal return path to the thread.
- Pouches are generated at meaningful checkpoint boundaries, not necessarily after every conversation.
- Large donor/source archives may remain external to Git.
- Pouches should record materially used external sources even when those artifacts are not committed.
- External-library indexing is a future infrastructure task and does not block current `_bricked` architecture work.

No Genesis mathematical or runtime semantics are changed by this decision.
