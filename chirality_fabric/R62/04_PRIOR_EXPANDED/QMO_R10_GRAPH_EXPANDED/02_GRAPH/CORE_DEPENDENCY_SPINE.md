# Time-Space → Consciousness Core Dependency Spine

Recovered from the strict recursive closure of the unified API. The spine is a selected readable path through the full edge registry; all source witnesses remain in the machine registries.

```text
@time_space
  --[EXPLICIT_ARROW | direct_source | high]-->
@genesis_field
  --[EXPLICIT_ARROW | direct_source | high]-->
@resolution
  --[EXPLICIT_ARROW | direct_source | high]-->
@bandwidth
  --[EXPLICIT_ARROW | direct_source | high]-->
@persistence
  --[EXPLICIT_ARROW | direct_source | high]-->
@chirality
  --[COMPOSED_DEPENDENCY | derived | high]-->
@helicon
  --[EXPLICIT_ARROW | direct_source | high]-->
@graviton
  --[EXPLICIT_ARROW | direct_source | high]-->
@time_shell
  --[COMPOSED_DEPENDENCY | derived | high]-->
@spacetime
  --[SUPPORTS | derived | high]-->
@black_hole
  --[BLACK_HOLE_MODEL_REACHES | derived | high]-->
@black_hole_cosmology
  --[DEPENDS_ON | recovered | high]-->
@cosmology
  --[EXPLICIT_ARROW | direct_source | high]-->
@consciousness
```

## Edge provenance

- `@time_space` → `@genesis_field` — **EXPLICIT_ARROW**; status `direct_source`; trust `TYPED_SOURCE_GRAPH`; provenance `"MK43_Ultra_API_CURRENT_CANONICAL.md:45141"`
- `@genesis_field` → `@resolution` — **EXPLICIT_ARROW**; status `direct_source`; trust `TYPED_SOURCE_GRAPH`; provenance `"MK43_Ultra_API_CURRENT_CANONICAL.md:45078"`
- `@resolution` → `@bandwidth` — **EXPLICIT_ARROW**; status `direct_source`; trust `TYPED_SOURCE_GRAPH`; provenance `"MK43_Ultra_API_CURRENT_CANONICAL.md:45130"`
- `@bandwidth` → `@persistence` — **EXPLICIT_ARROW**; status `direct_source`; trust `TYPED_SOURCE_GRAPH`; provenance `"MK43_Ultra_API_CURRENT_CANONICAL.md:45050"`
- `@persistence` → `@chirality` — **EXPLICIT_ARROW**; status `direct_source`; trust `TYPED_SOURCE_GRAPH`; provenance `"MK43_Ultra_API_CURRENT_CANONICAL.md:45110"`
- `@chirality` → `@helicon` — **COMPOSED_DEPENDENCY**; status `derived`; trust `TYPED_SOURCE_GRAPH`; provenance `"DERIVED:RP46_ADMISSIBLE_DEPENDENCY_COMPOSITION; path=@chirality -> @er_foam -> @helicon; relations=DEPENDS_TO + DEPENDS_TO; primitive_depth=2"`
- `@helicon` → `@graviton` — **EXPLICIT_ARROW**; status `direct_source`; trust `TYPED_SOURCE_GRAPH`; provenance `"MK43_Ultra_API_CURRENT_CANONICAL.md:45092"`
- `@graviton` → `@time_shell` — **EXPLICIT_ARROW**; status `direct_source`; trust `TYPED_SOURCE_GRAPH`; provenance `"MK43_Ultra_API_CURRENT_CANONICAL.md:45086"`
- `@time_shell` → `@spacetime` — **COMPOSED_DEPENDENCY**; status `derived`; trust `TYPED_SOURCE_GRAPH`; provenance `"DERIVED:RP46_ADMISSIBLE_DEPENDENCY_COMPOSITION; path=@time_shell -> @gravity -> @cosmology -> @general_relativity -> @spacetime; relations=DEPENDS_TO + DEPENDS_TO + DEPENDS_ON + DEPENDS_ON; primitive_depth=4"`
- `@spacetime` → `@black_hole` — **SUPPORTS**; status `derived`; trust `TYPED_SOURCE_GRAPH`; provenance `"DERIVED:RP46_INVERSE_RELATION; source_edge=(@black_hole DEPENDS_ON @spacetime); rule=DEPENDS_ON→SUPPORTS"`
- `@black_hole` → `@black_hole_cosmology` — **BLACK_HOLE_MODEL_REACHES**; status `derived`; trust `TYPED_SOURCE_GRAPH`; provenance `"DERIVED:RP51_BLACK_HOLE_FORWARD_CRAWL; witness=@black_hole-[DEPENDS_ON]->@spacetime | @spacetime-[SUPPORTS]->@black_hole_cosmology"`
- `@black_hole_cosmology` → `@cosmology` — **DEPENDS_ON**; status `recovered`; trust `TYPED_SOURCE_GRAPH`; provenance `"ACCEPTED_MATHEMATICS;GR_MODEL_EDGE:705"`
- `@cosmology` → `@consciousness` — **EXPLICIT_ARROW**; status `direct_source`; trust `TYPED_SOURCE_GRAPH`; provenance `"MK43_Ultra_API_CURRENT_CANONICAL.md:45071"`