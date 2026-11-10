PRAGMA foreign_keys = ON;

CREATE TABLE members (
    member_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    joined_on TEXT NOT NULL
);

CREATE TABLE staff (
    staff_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE authors (
    author_id INTEGER PRIMARY KEY,
    author_name TEXT NOT NULL
);

CREATE TABLE books (
    book_id INTEGER PRIMARY KEY,
    isbn TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    publication_year INTEGER
        CHECK (publication_year IS NULL OR publication_year > 0)
);

CREATE TABLE book_authors (
    book_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);

CREATE TABLE book_copies (
    copy_id INTEGER PRIMARY KEY,
    book_id INTEGER NOT NULL,
    shelf_code TEXT NOT NULL UNIQUE,
    copy_status TEXT NOT NULL DEFAULT 'AVAILABLE'
        CHECK (copy_status IN (
            'AVAILABLE',
            'ON_LOAN',
            'MAINTENANCE',
            'LOST'
        )),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);

CREATE TABLE loans (
    loan_id INTEGER PRIMARY KEY,
    member_id INTEGER NOT NULL,
    staff_id INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
);

CREATE TABLE loan_items (
    loan_item_id INTEGER PRIMARY KEY,
    loan_id INTEGER NOT NULL,
    copy_id INTEGER NOT NULL,
    issued_on TEXT NOT NULL,
    due_on TEXT NOT NULL,
    returned_on TEXT,
    CHECK (due_on >= issued_on),
    CHECK (returned_on IS NULL OR returned_on >= issued_on),
    FOREIGN KEY (loan_id) REFERENCES loans(loan_id),
    FOREIGN KEY (copy_id) REFERENCES book_copies(copy_id)
);

CREATE UNIQUE INDEX uq_active_loan_per_copy
ON loan_items(copy_id)
WHERE returned_on IS NULL;
