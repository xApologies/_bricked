# Physical path normalization

No source-file contents or Genesis terms were rewritten. All domain labels retain the spelling supplied in this ZIP except Windows-forbidden colons in domain 17, replaced by hyphens. This archive already omits the pipe separators seen in an earlier ZIP.

ZIP containers are opened, not recreated as directories. Each selected package's single release-name wrapper is mounted at its existing domain. Inner numbered folders remain unchanged. Packages 16–18 and `_lang` have no common release wrapper. No case-insensitive path collisions were found.

| Source package | Removed packaging wrapper | Working domain |
| --- | --- | --- |
| `Genesis/1 Packages/GENESIS_CHIRALITY_MACHINE_SECTION_01_HARDWARE_ABI_v0.1.0_20260821_PART_A_CORE.zip` | `GENESIS_CHIRALITY_MACHINE_SECTION_01_HARDWARE_ABI_v0.1.0_20260821/` | `1 Packages/` |
| `Genesis/2 Instantiation & Memory/GENESIS_CHIRALITY_MACHINE_SECTION_02_GEOMETRIC_INSTANTIATION_v0.1.0_20260821_PART_A_CORE.zip` | `GENESIS_CHIRALITY_MACHINE_SECTION_02_GEOMETRIC_INSTANTIATION_v0.1.0_20260821/` | `2 Instantiation & Memory/` |
| `Genesis/3 Transformation Engine & Geometry Forking/GENESIS_CHIRALITY_MACHINE_SECTION_03_TRANSFORMATION_ENGINE_v0.1.0_20260821_PART_A_CORE.zip` | `GENESIS_CHIRALITY_MACHINE_SECTION_03_TRANSFORMATION_ENGINE_v0.1.0_20260821/` | `3 Transformation Engine & Geometry Forking/` |
| `Genesis/4 Portal Engine/GENESIS_CHIRALITY_MACHINE_SECTION_04_PORTAL_ENGINE_v0.1.0_20260821_PART_A_CORE.zip` | `GENESIS_CHIRALITY_MACHINE_SECTION_04_PORTAL_ENGINE_v0.1.0_20260821/` | `4 Portal Engine/` |
| `Genesis/5 Rainbow Road/GENESIS_CHIRALITY_MACHINE_SECTION_05_RAINBOW_ROAD_v0.1.0_20260821_PART_A_CORE.zip` | `GENESIS_CHIRALITY_MACHINE_SECTION_05_RAINBOW_ROAD_v0.1.0_20260821/` | `5 Rainbow Road/` |
| `Genesis/6 QFT + GR Bridge/GENESIS_CHIRALITY_MACHINE_SECTION_06_QFT_GR_TRANSDUCTION_v0.1.0_20260821_PART_A_CORE.zip` | `GENESIS_CHIRALITY_MACHINE_SECTION_06_QFT_GR_TRANSDUCTION_v0.1.0_20260821/` | `6 QFT + GR Bridge/` |
| `Genesis/7 QIS + Effect System/GENESIS_CHIRALITY_MACHINE_SECTION_07_QUANTUM_INFORMATION_EFFECTS_v0.1.0_20260821_PART_A_CORE.zip` | `GENESIS_CHIRALITY_MACHINE_SECTION_07_QUANTUM_INFORMATION_EFFECTS_v0.1.0_20260821/` | `7 QIS + Effect System/` |
| `Genesis/8 Genesis VM/GENESIS_CHIRALITY_MACHINE_SECTION_08_VM_IR_v0.1.0_20260821_PART_A_CORE.zip` | `GENESIS_CHIRALITY_MACHINE_SECTION_08_VM_IR_v0.1.0_20260821/` | `8 Genesis VM/` |
| `Genesis/9 Semantic Linker/GENESIS_CHIRALITY_MACHINE_SECTION_09_STATIC_SEMANTICS_LINKER_v0.1.0_20260821_PART_A_CORE.zip` | `GENESIS_CHIRALITY_MACHINE_SECTION_09_STATIC_SEMANTICS_LINKER_v0.1.0_20260821/` | `9 Semantic Linker/` |
| `Genesis/10 Genesis Surface Language/GENESIS_CHIRALITY_MACHINE_SECTION_10_GENESIS_FRONTEND_v0.1.0_20260821_PART_A_CORE.zip` | `GENESIS_CHIRALITY_MACHINE_SECTION_10_GENESIS_FRONTEND_v0.1.0_20260821/` | `10 Genesis Surface Language/` |
| `Genesis/11 Genesis Optimization & Backend/GENESIS_CHIRALITY_MACHINE_SECTION_11_OPTIMIZER_CODEGEN_v0.1.0_20260821_PART_A_CORE.zip` | `GENESIS_CHIRALITY_MACHINE_SECTION_11_OPTIMIZER_CODEGEN_v0.1.0_20260821/` | `11 Genesis Optimization & Backend/` |
| `Genesis/19 Genesis Bootstrap & Self-Hosting Path/GENESIS_CHIRALITY_MACHINE_SECTION_19_BOOTSTRAP_SELF_HOSTING_v0.1.0_20260821_PART_C_IMPLEMENTATION_LINEAGE.zip!/_section19_part_c/GENESIS_CHIRALITY_MACHINE_SECTION_12_STDLIB_PACKAGE_RUNTIME_v0.1.0_20260821_PART_A_CORE.zip` | `GENESIS_CHIRALITY_MACHINE_SECTION_12_STDLIB_PACKAGE_RUNTIME_v0.1.0_20260821/` | `12 Genesis Library/` |
| `Genesis/13 Callable Abstractions, Functions & Generics/GENESIS_CHIRALITY_MACHINE_SECTION_13_CALLABLES_GENERICS_v0.1.0_20260821_PART_A_CORE.zip` | `GENESIS_CHIRALITY_MACHINE_SECTION_13_CALLABLES_GENERICS_v0.1.0_20260821/` | `13 Callable Abstractions, Functions & Generics/` |
| `Genesis/14 Control Flow & Data Algebra/GENESIS_CHIRALITY_MACHINE_SECTION_14_CONTROL_FLOW_DATA_ALGEBRA_v0.1.0_20260821_PART_A_CORE.zip` | `GENESIS_CHIRALITY_MACHINE_SECTION_14_CONTROL_FLOW_DATA_ALGEBRA_v0.1.0_20260821/` | `14 Control Flow & Data Algebra/` |
| `Genesis/15 Recursion & Recursive Topology Execution/GENESIS_CHIRALITY_MACHINE_SECTION_15_RECURSIVE_TOPOLOGY_v0.1.0_20260821_PART_A_CORE.zip` | `GENESIS_CHIRALITY_MACHINE_SECTION_15_RECURSIVE_TOPOLOGY_v0.1.0_20260821/` | `15 Recursion & Recursive Topology Execution/` |
| `Genesis/16 Concurrency & Scheduling & Resource Coordination/GENESIS_CHIRALITY_MACHINE_SECTION_16_CONCURRENCY_SCHEDULING_v0.1.0_20260821_PART_A_CORE.zip` | `(none)` | `16 Concurrency & Scheduling & Resource Coordination/` |
| `Genesis/17 System I:O & BLACKGLASS:BRANE Interface/GENESIS_CHIRALITY_MACHINE_SECTION_17_SYSTEM_IO_BLACKGLASS_BRANE_v0.1.0_20260821_PART_A_CORE.zip` | `(none)` | `17 System I-O & BLACKGLASS-BRANE Interface/` |
| `Genesis/18 Compiler Toolchain & Diagnostics & Debugging/GENESIS_CHIRALITY_MACHINE_SECTION_18_TOOLCHAIN_DIAGNOSTICS_DEBUGGING_v0.1.0_20260821_PART_A_CORE.zip` | `(none)` | `18 Compiler Toolchain & Diagnostics & Debugging/` |
| `Genesis/19 Genesis Bootstrap & Self-Hosting Path/GENESIS_CHIRALITY_MACHINE_SECTION_19_BOOTSTRAP_SELF_HOSTING_v0.1.0_20260821_PART_A_CORE.zip` | `GENESIS_CHIRALITY_MACHINE_SECTION_19_BOOTSTRAP_SELF_HOSTING_v0.1.0_20260821/` | `19 Genesis Bootstrap & Self-Hosting Path/` |
| `Genesis/20 GENESIS/GENESIS_CHIRALITY_MACHINE_SECTION_20_V1_CONFORMANCE_FREEZE_v1.0.0_20260821_PART_A_CORE.zip` | `GENESIS_CHIRALITY_MACHINE_SECTION_20_V1_CONFORMANCE_FREEZE_v1.0.0_20260821/` | `20 GENESIS/` |
| `Genesis/_lang/GENESIS_LANGUAGE_SOURCESET_v0.1.zip` | `(none)` | `_lang/` |

`RECOVERED_FILES.json` gives the exact original and final path of every retained file. Historical absolute paths in original documents/manifests are kept as evidence; the new test launcher handles the one host-specific fixture lookup without modifying source.
