GENESIS CHIRALITY FABRIC — R62 SPLIT TRANSPORT VOLUMES
========================================================

Purpose
-------
These ZIP_A, ZIP_B, ... files are transport volumes for the exact original checkpoint:

  GENESIS_CHIRALITY_FABRIC_FULL_CHECKPOINT_R62_v1_0_20260829.zip

Original size:   1,838,368,113 bytes
Original SHA-256:f0c63cabf18ad856f10dc2ffd57669ae02106a561d2c9af06a5ecf83bf79d65e
Volumes:         21
Maximum payload: 90,000,000 bytes per volume

The volumes are not independent project checkpoints. Together they reconstruct the one exact
1,838,368,113-byte R62 checkpoint ZIP.

Easiest reassembly
------------------
1. Download every volume ZIP into one folder.
2. Download `reassemble_r62.py` into that same folder.
3. Run:

     python reassemble_r62.py

The script reads the binary part directly from each volume ZIP, verifies every part, writes the
original checkpoint ZIP, and verifies the final SHA-256.

No manual extraction is required.

Expected output
---------------
  GENESIS_CHIRALITY_FABRIC_FULL_CHECKPOINT_R62_v1_0_20260829.zip

Expected final SHA-256
---------------------
  f0c63cabf18ad856f10dc2ffd57669ae02106a561d2c9af06a5ecf83bf79d65e

Manual reassembly
-----------------
Extract the `.part_A.bin`, `.part_B.bin`, ... files from all volume ZIPs and concatenate them in
alphabetical order without changing a byte. The Python script is strongly preferred because it
performs verification automatically.
