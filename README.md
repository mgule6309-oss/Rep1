Community Library Management System

MIT 8103 – Advanced Database Systems Portfolio

Student: Sammani Sani Gule Muhammad
Student ID: 301926309
Case Study: Community Library Management System

Project Overview

This portfolio presents the database design and implementation concepts used to support a Community Library Management System. The proposed system manages library members, staff, books, authors, physical book copies, loans and returns.

The work demonstrates relational database design, normalisation, query optimisation, transaction management, NoSQL data modelling and distributed/cloud database architecture.

Portfolio Activities

1. Database Design and Normalisation

The relational database is designed around members, staff, books, authors, book copies, loans and loan items. Primary keys, foreign keys, constraints and an index for active loans help maintain data integrity.

See: portfolio-1-database-design/

2. Query Optimisation

SQL query patterns are examined using SQLite query plans and benchmark measurements before and after indexing. The recorded timings are illustrative of the supplied test dataset and environment, not guarantees of production performance.

See: portfolio-2-query-optimisation/ and evidence/

3. Transactions and Concurrency

The portfolio demonstrates an atomic book-issuing operation and transaction tests covering successful issue, unavailable copies and rollback after failure. The two-session concurrency discussion is a documented test plan, not a claim that a live concurrent test was performed.

See: portfolio-3-transactions-concurrency/

4. NoSQL Data Modelling

A sample loan document and MongoDB command examples demonstrate how a loan record could be represented in a document database. The MongoDB examples are illustrative and have not been presented as a live database deployment.

See: portfolio-4-nosql/

5. Distributed and Cloud Database Architecture

A proposed architecture discusses how the library system could be extended using distributed or cloud database services, including availability, backup and recovery considerations. It is a design proposal; no cloud infrastructure is claimed to have been deployed.

See: portfolio-5-distributed-cloud/

Repository Structure

* portfolio-1-database-design/ – relational schema, sample data and normalisation.
* portfolio-2-query-optimisation/ – query analysis and optimisation notes.
* portfolio-3-transactions-concurrency/ – transaction implementation and concurrency notes.
* portfolio-4-nosql/ – sample document and MongoDB examples.
* portfolio-5-distributed-cloud/ – distributed/cloud architecture proposal.
* scripts/ – Python scripts for database building, query analysis, transaction testing and running checks.
* evidence/ – benchmark outputs, validation records and test evidence.

Running the SQLite Scripts

Requirements: Python 3.10 or later. The SQLite implementation uses Python’s built-in sqlite3 module.

From the repository root, run:

python scripts/build_database.py
python scripts/run_query_analysis.py
python scripts/test_transactions.py

To run the checks in sequence:

python scripts/run_all_checks.py

Run these commands in a local Python environment. Review the output to confirm whether each check passes. The runner does not itself guarantee successful execution.

Scope and Limitations

The relational implementation and local SQLite checks are provided as code. Benchmark results depend on the test data and execution environment. MongoDB examples are illustrative; the concurrency scenario is a manual test plan; and the distributed/cloud architecture is a proposal rather than a deployed service.

Author

Sammani Sani Gule Muhammad
Student ID: 301926309
MIT 8103 – Advanced Database Systems
