# Transactions, isolation and concurrency

## Atomic issue workflow
`issue_book.py` uses `BEGIN IMMEDIATE`, conditionally changes a copy from `AVAILABLE` to `ON_LOAN`, inserts the loan header and loan item, then commits. If the copy is unavailable or a later constraint fails, the whole transaction rolls back. This avoids a committed stock-state change without its corresponding loan record.

## Concurrency consideration
SQLite permits multiple readers but serializes writers. `BEGIN IMMEDIATE` obtains the write reservation before checking and changing availability, reducing the chance that two writers both pass an availability check. The partial unique index on active loan items is an additional integrity guard.

## Manual two-session verification plan (not represented as executed)
1. Open two independent SQLite connections to the same database.
2. In session A, begin an immediate transaction and attempt to issue one available copy.
3. In session B, attempt to issue the same copy; it should wait up to the configured timeout or receive a busy/locked response.
4. Commit session A. Retry the operation in session B; the conditional update should affect zero rows and the application should reject the second issue.
5. Confirm one active loan item exists for the copy.

A production PostgreSQL deployment should explicitly select and test transaction isolation, lock timeouts, retry handling and deadlock behaviour for the expected workload. The two-session manual plan has not been run in this package-preparation environment.
