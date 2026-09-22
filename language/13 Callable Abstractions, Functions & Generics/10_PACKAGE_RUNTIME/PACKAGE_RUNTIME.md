# Callable-aware package runtime

`genesis_callable_packages.CallablePackageRuntime` extends the Section 12 package model.

It preserves:

- content-addressed package storage;
- semantic-version dependency resolution;
- frozen lockfiles;
- deterministic topological package order;
- effect budgets;
- package build receipts;
- Section 11 optimization and differential execution checks.

It adds:

- parsing of callable modules;
- callable visibility/import validation;
- recursion checks across all modules in the resolved package graph;
- direct-dependency enforcement for `usefn`;
- package effect accounting for exported function contracts and top-level calls;
- callable frontend receipts;
- call expansion ledgers;
- callable proof ledgers;
- expanded-source preservation in build artifacts.

A package build therefore records both the source-level callable architecture and the exact lower program that was ultimately executed.
