# Section 08 architecture

## Two-stage execution language

Genesis needs a representation that preserves the project's native relationship/dependency semantics without forcing source programs to look like CPU assembly. It also needs a deterministic machine that can actually run those semantics on current hardware.

Therefore Section 08 separates:

### GIR — semantic graph

```text
Nodes      = typed semantic operations
Edges      = data dependency, relationship, effect ordering, closure obligation
Values     = SSA-like immutable references
Resources  = typed identity-bearing runtime resources
Blocks     = optional explicit control regions
```

GIR is the canonical compiler target for future Genesis syntax.

### GVM — execution machine

```text
Typed virtual registers
Resource table
Fabric mount table
Linear-resource ownership table
Frame/control stack
Append-only receipt ledger
Backend dispatch table
```

GVM is a deterministic lowering target and bytecode format. GVM instructions are not the ontology; they are an execution projection of GIR.

## Machine stack

```text
Genesis source (future)
        v
GIR graph
        v
Static verifier + type/effect checker
        v
Deterministic graph scheduler
        v
GVM instruction stream
        v
GVM verifier
        v
Reference VM
        v
Backend ABI
        v
Section stack 01..07
        v
BRANE / Trinity / BLACKGLASS
```

## Design law

**The program is the typed relationship graph. The instruction stream is a deterministic execution projection of that graph.**
