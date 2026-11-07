"""Atomic issue-book operation for the Community Library example."""
import sqlite3
from pathlib import Path


def issue_book(db_path, member_id, staff_id, copy_id, issued_on, due_on):
    conn = sqlite3.connect(str(db_path), timeout=10, isolation_level=None)
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        conn.execute("BEGIN IMMEDIATE")
        cur = conn.execute(
            "UPDATE book_copies SET copy_status='ON_LOAN' "
            "WHERE copy_id=? AND copy_status='AVAILABLE'", (copy_id,)
        )
        if cur.rowcount != 1:
            raise ValueError("Copy is not available for issue")
        cur = conn.execute(
            "INSERT INTO loans(member_id, staff_id, created_at) VALUES (?, ?, ?)",
            (member_id, staff_id, issued_on + "T00:00:00")
        )
        loan_id = cur.lastrowid
        conn.execute(
            "INSERT INTO loan_items(loan_id, copy_id, issued_on, due_on) VALUES (?, ?, ?, ?)",
            (loan_id, copy_id, issued_on, due_on)
        )
        conn.execute("COMMIT")
        return loan_id
    except Exception:
        if conn.in_transaction:
            conn.execute("ROLLBACK")
        raise
    finally:
        conn.close()
