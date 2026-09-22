# GVM/GIR type universe v0.1

Scalar/structural:

`VOID BOOL INT FLOAT TEXT HASH SECTOR FABRIC_ADDR REGION`

Identity/resources:

`FABRIC MMO GEOMETRIC RELATION ADMISSION TRANSFORM PORTAL ROAD BRIDGE QSTATE QRESULT M5 RECEIPT`

A future frontend may expose richer parametric types such as:

`Portal<QFT>`, `Portal<GR>`, `MMO<closed>`, `QState<owned>`, `Road<partial>`.

GVM stores those refinements as verified attributes/typestates rather than flattening them into untyped strings.
