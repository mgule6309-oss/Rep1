# Query analysis method

The benchmark script creates a deterministic synthetic workload of 1,000 books, 1,500 physical copies, 3,000 members, 8,000 loan headers and 12,000 loan-item history rows. It measures four representative access patterns before and after adding workload indexes. Each query is warmed up and timed over repeated runs; the script reports medians, not a single best-case result. `EXPLAIN QUERY PLAN` is captured before and after indexing.

The benchmark is a controlled local SQLite experiment, not a production workload. Timing depends on hardware, SQLite version, cache state and dataset distribution. Query-plan changes are more portable evidence than tiny millisecond differences. A real deployment should repeat the test with anonymised production-like distributions and concurrent workload.
