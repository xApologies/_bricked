# Section 15 continuation integration

Section 15 established persistent recursion as bounded slices producing integrity-protected continuations. Section 16 treats such a continuation as a schedulable task state.

A recursion slice may return `SUSPENDED` and re-enter the ready set on a later logical turn, or return `CLOSED` and advance to task closure. The compatibility adapter preserves the Section 15 token fields: `task_id`, `state`, `delta`, `close_at`, `total_steps`, `history_root`, and `digest`.

The scheduler never relabels a suspended recursion as halted.
