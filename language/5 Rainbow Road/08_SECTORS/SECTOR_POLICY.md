# Sector Policy

Section 05 supports homogeneous Roads:

* `RainbowRoad<GENERIC>`
* `RainbowRoad<QFT>`
* `RainbowRoad<GR>`

Every waypoint address and every Corridor edge must admit the Road sector.

Cross-sector composition is rejected in this section. The QFT<->GR bridge is preserved as source mathematics and will be implemented through an explicit transduction/bridge object rather than by declaring sector equality.
