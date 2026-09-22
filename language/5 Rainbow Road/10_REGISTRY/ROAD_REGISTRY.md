# Road Registry

A `RoadRegistry` stores immutable Road templates and source-bound Road plans by digest and optional stable alias.

Registry identity is not execution identity. Reusing a template against a different source creates a different Road plan/run while retaining the template's provenance.
