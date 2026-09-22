# Reproducible build contract

Semantic build identity excludes wall-clock timestamps, temporary directory names, and absolute host paths. It includes source bytes, logical source name, target triple/profile, toolchain contract version, and normalized options.

A reproducibility check builds twice in independent directories and compares cryptographic hashes of the semantic artifact set.
