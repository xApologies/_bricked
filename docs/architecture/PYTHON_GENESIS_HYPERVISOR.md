# Python Genesis Hypervisor
Status: WORKING CANON; implementation not started.

The Python sandbox is the VM/hypervisor abstraction that boots and contains Genesis.

Responsibilities: boot/shutdown, containment, host monotonic clock, scheduling/execution budget, host I/O mediation, Horizon transduction, serialization/buffering, save/restore, replay support, resource accounting and fault handling.

Python does not decide Genesis semantics.

Analogy:
TABLE = native platform.
COIN = platform adapter.
DIE = Python Genesis Hypervisor.
INSIDE DIE = Genesis domain.

The Hypervisor owns the host timing source. Genesis may admit timing information and derive local S2 cycles without equating host time with Genesis time.
