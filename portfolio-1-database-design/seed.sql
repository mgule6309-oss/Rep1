PRAGMA foreign_keys = ON;

INSERT INTO members (member_id, full_name, email, joined_on) VALUES
(1, 'Amina Yusuf', 'amina@example.com', '2025-01-10'),
(2, 'Daniel Okafor', 'daniel@example.com', '2025-02-15'),
(3, 'Fatima Bello', 'fatima@example.com', '2025-03-20');

INSERT INTO staff (staff_id, full_name, email) VALUES
(1, 'Grace Adeyemi', 'grace.staff@example.com'),
(2, 'Peter James', 'peter.staff@example.com');

INSERT INTO authors (author_id, author_name) VALUES
(1, 'Chinua Achebe'),
(2, 'Chimamanda Ngozi Adichie'),
(3, 'Wole Soyinka'),
(4, 'Buchi Emecheta'),
(5, 'Ben Okri');

INSERT INTO books
(book_id, isbn, title, category, publication_year) VALUES
(1, '9780000000001', 'Things Fall Apart', 'Fiction', 1958),
(2, '9780000000002', 'Half of a Yellow Sun', 'Historical Fiction', 2006),
(3, '9780000000003', 'The Lion and the Jewel', 'Drama', 1959),
(4, '9780000000004', 'The Joys of Motherhood', 'Fiction', 1979),
(5, '9780000000005', 'The Famished Road', 'Fantasy', 1991);

INSERT INTO book_authors (book_id, author_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);

INSERT INTO book_copies
(copy_id, book_id, shelf_code, copy_status) VALUES
(1, 1, 'A1-001', 'ON_LOAN'),
(2, 2, 'A1-002', 'ON_LOAN'),
(3, 3, 'B1-001', 'AVAILABLE'),
(4, 4, 'B1-002', 'AVAILABLE'),
(5, 5, 'C1-001', 'AVAILABLE'),
(6, 1, 'A1-003', 'AVAILABLE'),
(7, 2, 'A1-004', 'MAINTENANCE');

INSERT INTO loans (loan_id, member_id, staff_id, created_at) VALUES
(1, 1, 1, '2025-10-01 09:00:00'),
(2, 2, 2, '2025-10-02 10:00:00'),
(3, 3, 1, '2025-10-03 11:00:00');

INSERT INTO loan_items
(loan_item_id, loan_id, copy_id, issued_on, due_on, returned_on) VALUES
(1, 1, 1, '2025-10-01', '2025-10-15', NULL),
(2, 2, 2, '2025-10-02', '2025-10-16', NULL),
(3, 3, 3, '2025-09-01', '2025-09-15', '2025-09-12'),
(4, 3, 4, '2025-09-01', '2025-09-15', '2025-09-14');
