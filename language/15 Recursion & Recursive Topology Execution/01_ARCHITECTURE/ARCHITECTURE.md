# Section 15 architecture

Execution chain:

`Genesis 0.4 source -> recursion AST -> recursive CFG -> recursion verifier -> frame bytecode -> Recursive VM -> closure/history receipt`

Section 15 extends the Section 08/14 machine model at the call-frame boundary. Ordinary scalar/data operations remain compatible with the prior GVM semantics. Recursive calls use frame-local registers so a function can invoke itself without aliasing or redefining its caller's SSA registers.

## Frame model

A recursive frame contains:

- function identity
- frame identity and parent frame identity
- local register file
- return PC and destination register in the parent
- recursion depth
- recursion contract state (metric, fuel, or visit history)
- local closure state
- inherited history-root seed

A return is admissible only after `RECURSION_CLOSE` has sealed the frame. The frame receipt is appended to the parent history root. This gives recursive execution a deterministic ancestry chain rather than a disposable host-language stack.
