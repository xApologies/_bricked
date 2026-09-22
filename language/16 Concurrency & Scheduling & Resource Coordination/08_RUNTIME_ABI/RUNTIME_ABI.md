# Runtime ABI

Required scheduler services:

`spawn(template, handle)`
`dispatch(task)`
`yield(task)`
`block(task, resource)`
`wake(task)`
`cancel(task)`
`acquire(task, resource, mode, units)`
`release(task, resource)`
`resume_recursion(continuation, budget)`
`detect_deadlock(wait_graph)`
`close_task(task)`
`close_schedule(scope)`

A native BLACKGLASS backend may implement these without Python provided receipts, state transitions, resource authority, and failure semantics remain compatible.
