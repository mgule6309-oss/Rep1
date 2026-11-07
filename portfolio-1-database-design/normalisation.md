# Database design and normalisation

## Case description
A simulated community library manages members, staff, a catalogue, authors, physical book copies, loans and returns. It needs to search titles, check copy availability, issue several books in one loan, identify overdue items and report popular titles. All sample people and `.test` email addresses are synthetic.

## Design decisions
- `books` stores bibliographic title/ISBN/category data; `book_copies` stores each physical copy and its shelf/status.
- `book_authors` resolves the many-to-many relationship between books and authors.
- `loans` stores the loan header (member, staff, timestamp); `loan_items` stores each physical copy and its issue/due/return dates. This supports multiple books per loan and item-level returns.
- Primary keys identify rows; foreign keys preserve relationships; UNIQUE constraints protect ISBN, email and shelf identifiers; CHECK constraints validate dates and copy status.
- A partial unique index on `loan_items(copy_id)` where `returned_on IS NULL` prevents two simultaneous active loans for one physical copy.

## Normalisation
- **1NF:** each field contains one value; multiple authors and loaned copies are represented in child/junction tables, not comma-separated lists.
- **2NF:** the junction table's composite key determines the complete relationship; descriptive author/book attributes remain in their own tables.
- **3NF:** member, staff, author, book and copy descriptions depend on their own keys rather than being repeated in loan rows. Loan-item dates belong to the individual copy-loan event.

The `copy_status` field is maintained by the issue/return transaction as an operational state. The transaction tests and application workflow must keep it aligned with active loan items; a production system could enforce this further with triggers or a single authoritative availability calculation.
