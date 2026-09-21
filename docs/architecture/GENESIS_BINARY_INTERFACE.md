# Genesis Binary Interface
Status: DESIGN CANDIDATE.

GBI is the platform-neutral byte boundary downstream of Horizon transduction.

Genesis -> Horizon -> binary -> Python/GBI -> native adapter -> renderer. Input reverses the route.

GBI encodes authoritative exposed state; it does not generate platform-specific source code each frame.

Candidate message families: BOOT, SHUTDOWN, STATE_FRAME, OBJECT_STATE, RELATIONSHIP_STATE, PROJECTION_STATE, CHIRALITY_STATE, EVENT, INPUT, ACK, ERROR, SNAPSHOT, RESTORE, PROVENANCE.

Versioning, IDs, ordering, endianness, integrity, compatibility, replay and error semantics remain to be formalized.
