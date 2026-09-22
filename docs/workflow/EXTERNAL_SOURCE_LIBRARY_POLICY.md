# External Source Library Policy

Status: WORKING PROJECT POLICY.

Large donor/source artifacts are not required to live in the `_bricked` Git repository.

Examples include large ZIP archives, research corpora, model archives, datasets, large PDFs/checkpoints, and source families such as Trinity, Chirality Fabric, Rainbow Road, PSSP, Time-Space/MK Ultra, Genesis Language, and related historical packages.

## Git stores derived project knowledge

Git should store appropriate project artifacts such as:

- specifications;
- architecture;
- algorithms;
- level definitions;
- provenance;
- decisions;
- source references;
- hashes/receipts;
- status;
- small derived documents.

## External storage retains heavyweight evidence

Heavyweight sources may remain in a local source library. Their absence from Git does not mean they are lost or superseded.

Future source registry work may assign stable source IDs, relative library paths, SHA-256 hashes, versions, relationships, and dependency records.

## Current lightweight rule

Until the library/indexer is implemented, each meaningful pouch should record the names of external artifacts that materially contributed to the accepted delta.

Do not claim a source was inspected if it was unavailable in that working context.

## Recovery principle

Derived project knowledge in Git and heavyweight source evidence are distinct layers. Git is the current project authority; external source checkpoints remain evidence/recovery material and may contain richer donor material than Git.
