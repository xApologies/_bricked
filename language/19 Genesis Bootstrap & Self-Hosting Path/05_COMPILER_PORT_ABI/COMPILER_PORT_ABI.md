# Compiler Port ABI

A compiler port is a normal BRANE M5 module contract with role `compiler` and capability `compile`.

Input: an immutable CAS reference containing UTF-8 Genesis source.

Output includes:
- source reference,
- emitted bytecode CAS reference,
- bytecode SHA-256,
- program id,
- verifier proof root,
- instruction count,
- compiler identity,
- an M6 realization in which BRANE alone assigns Z.

The reference adapter is bootstrap-only. A future Genesis-native compiler must satisfy the same ABI, allowing replacement without changing the bootstrap controller.
