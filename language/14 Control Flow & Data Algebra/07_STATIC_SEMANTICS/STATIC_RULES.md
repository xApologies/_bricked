# Static rules
Every `let` introduces a fresh immutable identity. Outer identities are readable in nested regions; nested identities are not visible after region exit. Record fields and variant payloads are type checked. `if` requires BOOL. Integer and boolean operators require matching operand types. `repeat` count is compile-time and <=4096.
