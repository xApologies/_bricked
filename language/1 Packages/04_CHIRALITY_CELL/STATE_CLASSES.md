# State / Basin Classes

`state_class` is an 8-way hardware code. The ABI does not assign universal physical voltage to any class.

Suggested emulator labels:

- 0 `BLACK`
- 1 `BASIN_1`
- 2 `BASIN_2`
- 3 `BASIN_3`
- 4 `BASIN_4`
- 5 `BASIN_5`
- 6 `BASIN_6`
- 7 `WHITE`

This is an implementation encoding only. A physical backend supplies a calibration table. Chromatic source models may map the six interior basins to normalized targets such as `k/7`, but GCHI does not force a specific voltage standard.
