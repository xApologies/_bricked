# Transformation object model

## TransformRequest
A declarative request containing parent identity/root, capability profile, ordered operators, invariant contract, and semantic identity policy.

## TransformPlan
A canonicalized, admitted plan with deterministic `plan_id`, effect union, selected address sets, pre-state root, and expected semantic lineage action.

## TransformProgram
An ordered list of typed transformation operators. Composition is left-to-right over the staged child view.

## ChangeSet
A sparse address -> ChiralityCell mapping. It is the only material written to a `.gtd` delta.

## TransformationReceipt
The closure artifact containing parent/child identity, pre/post state roots, patch digest, effect analysis, invariant results and segment hashes.

## Child GeometricInstance
The realized post-transform state. It shares the canonical MMO identity unless the request explicitly declares another semantic identity policy.
