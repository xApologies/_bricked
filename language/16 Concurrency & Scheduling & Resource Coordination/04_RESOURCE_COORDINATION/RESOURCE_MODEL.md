# Resource coordination model

A resource has stable identity, kind, and positive integer capacity. A shared lease consumes one or more units. An exclusive lease consumes the entire resource capacity and is admitted only when no holder exists.

Waiters are ordered by deterministic wait sequence. Release may wake the earliest waiter whose requested claim is currently admissible. Resource state is included in the schedule receipt.

Resources can stand for fabric regions, Rainbow Bus capacity, accelerator queues, device channels, or other finite execution capabilities. Section 16 defines the coordination semantics, not the physical carrier.
