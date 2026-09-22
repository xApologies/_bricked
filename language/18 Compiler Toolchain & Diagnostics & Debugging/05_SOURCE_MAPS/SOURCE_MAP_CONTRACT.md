# Source-map contract

Each executable instruction maps to the source statement that created it. The current Section 17 parser records `file:line`; Section 18 expands that into line/column spans and captures the exact source line. Source maps are derived artifacts and never replace the compiler's typed program representation.
