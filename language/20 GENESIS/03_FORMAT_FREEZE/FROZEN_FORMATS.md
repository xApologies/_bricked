# Frozen Format Policy

Genesis v1.0 freezes the interpretation of its public source, IR/bytecode, package, receipt, trace, and bootstrap-image formats. Compatible readers may accept newer optional fields, but v1.0-required fields cannot be silently reinterpreted. Content-addressed identities and provenance roots must remain stable for unchanged payloads.
