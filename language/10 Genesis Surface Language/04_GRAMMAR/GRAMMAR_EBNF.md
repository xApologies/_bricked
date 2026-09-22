# Executable grammar v0.1

```ebnf
file        = version, module ;
version     = "genesis", "0.1.0" ;
module      = "module", qname, "{", { item }, "}" ;
item        = use | export | statement ;

use         = "use", qname, "::", ident, "as", ident, ":", type ;
export      = "export", ident, ":", type ;

statement   = identity_stmt | relation_stmt | admit_stmt | transform_stmt
            | inherit_stmt | portal_stmt | transport_stmt | close_stmt
            | road_stmt | bridge_stmt | quantum_stmt | lift_stmt
            | seal_stmt | closure_assert | emit_stmt ;

identity_stmt = "en", ident, ":", type, "=",
                ( "mount", string
                | "alloc", ident, "cells", integer
                | "instantiate", ident, ident, "mmo", handle
                | "fork", ident ), [ attrs ] ;

relation_stmt = "rel", ident, "->", atom, "as", ident, [ attrs ] ;
admit_stmt    = "admit", ident, "as", ident, [ attrs ] ;
transform_stmt= "transform", ident, "with", ident, "as", ident, [ attrs ] ;
inherit_stmt  = "ar", ident, "as", ident, [ attrs ] ;
portal_stmt   = "portal", sector, ident, "with", ident, "as", ident,
                "corridor", string, [ "bridge", ident ], [ attrs ] ;
transport_stmt= "ve", ident, "through", ident, "->", atom, "as", ident, [ attrs ] ;
close_stmt    = "tor", ident, "with", ident, "as", ident, [ attrs ] ;
road_stmt     = "road", ( "begin", ident, "as", ident
                         | "append", ident, ident, "as", ident
                         | "close", ident, ident, "as", ident ), [ attrs ] ;
bridge_stmt   = "bridge", ident, sector, "->", sector, "as", ident, [ attrs ] ;
quantum_stmt  = "q", ( "prepare", ident, "as", ident
                      | "superpose", ident, "as", ident
                      | "entangle", ident, ident, "as", ident
                      | "channel", ident, "as", ident
                      | "measure", ident, "as", ident ), [ attrs ] ;
lift_stmt     = "lift", ident, "as", ident, [ attrs ] ;
seal_stmt     = "seal", ident, "as", ident, [ attrs ] ;
closure_assert= "assert", "closure", ident, "as", ident, [ attrs ] ;
emit_stmt     = "emit", "receipt", "as", ident, [ attrs ] ;

attrs       = "@", json_object ;
sector      = "GENERIC" | "QFT" | "GR" ;
```

This grammar is the canonical executable projection for Section 10 v0.1. It is intentionally smaller than the total conceptual Genesis vocabulary.
