# Failure model

Representative failures:

- `RESOURCE_UNKNOWN`
- `RESOURCE_DOUBLE_ACQUIRE`
- `RESOURCE_RELEASE_STATIC`
- `RESOURCE_NOT_HELD`
- `TASK_RESOURCE_LEAK_STATIC`
- `TASK_RESOURCE_LEAK_RUNTIME`
- `TASK_PRIORITY`
- `TASK_QUANTUM`
- `JOIN_UNKNOWN_HANDLE`
- `RECURSION_CONTINUATION_INVALID`
- `SCHEDULER_TICK_BUDGET`
- `DEADLOCK`

Deadlock is represented as a terminal schedule status plus a concrete cycle witness in the schedule receipt.
