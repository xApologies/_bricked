# Portal / Road closure barriers

`PORTAL_OPEN -> PORTAL_TRANSPORT -> PORTAL_CLOSE` and `ROAD_BEGIN -> ROAD_APPEND* -> ROAD_CLOSE` are preserved as typed transaction histories. Section 11 does not fuse, elide, or reorder these operations.
