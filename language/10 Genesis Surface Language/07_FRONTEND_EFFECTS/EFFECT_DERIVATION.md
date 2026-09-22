# Frontend effect derivation

A source module does not self-declare its authority budget in v0.1. The compiler derives the exact effect set from lowered GIR operations using the Section 09 opcode/effect table.

This prevents source text from hiding an operation behind a weaker declared budget. Section 09 then checks that the derived budget matches the graph it receives.
