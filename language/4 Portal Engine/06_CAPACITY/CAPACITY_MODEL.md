# Corridor Capacity Model

Each Corridor edge declares:

```text
bandwidth        organizational freedom threshold [0, 1]
capacity_units   reservable concurrent transport capacity
resolution       distinguishability support [0, 1]
```

`bandwidth` and `capacity_units` are deliberately different. Bandwidth follows the project meaning of available organizational freedom. Capacity units are an implementation scheduling resource used to prevent two software transactions from overcommitting the same edge.

A Portal request carries `capacity_units_required`. Capacity reservations are all-or-nothing across the selected path and are released after close/failure.
