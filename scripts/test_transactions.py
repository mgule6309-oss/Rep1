from pathlib import Path
import sqlite3, tempfile
from build_database import build
from issue_book import issue_book

ROOT = Path(__file__).resolve().parents[1]

def main():
    with tempfile.TemporaryDirectory() as td:
        db = Path(td) / "test.db"
        build(db)
        con = sqlite3.connect(db); con.execute("PRAGMA foreign_keys=ON")
        before_loans = con.execute("SELECT COUNT(*) FROM loans").fetchone()[0]
        con.close()

        # Successful commit.
        loan_id = issue_book(db, 1, 1, 5, "2026-11-01", "2026-11-15")
        con = sqlite3.connect(db)
        assert con.execute("SELECT copy_status FROM book_copies WHERE copy_id=5").fetchone()[0] == "ON_LOAN"
        assert con.execute("SELECT COUNT(*) FROM loan_items WHERE loan_id=? AND returned_on IS NULL", (loan_id,)).fetchone()[0] == 1
        assert con.execute("SELECT COUNT(*) FROM loans").fetchone()[0] == before_loans + 1
        con.close()
        print("PASS: successful issue committed copy status, loan header and loan item")

        # Reject a second issue of the same copy; no extra loan header may remain.
        try:
            issue_book(db, 2, 1, 5, "2026-11-02", "2026-11-16")
            raise AssertionError("Unavailable copy was incorrectly issued")
        except ValueError:
            pass
        con = sqlite3.connect(db)
        assert con.execute("SELECT COUNT(*) FROM loans").fetchone()[0] == before_loans + 1
        con.close()
        print("PASS: unavailable copy rejected without partial loan record")

        # Force a late CHECK failure after status update and loan-header insert.
        try:
            issue_book(db, 1, 1, 6, "2026-11-05", "2026-11-04")
            raise AssertionError("Invalid due date was incorrectly accepted")
        except sqlite3.IntegrityError:
            pass
        con = sqlite3.connect(db)
        assert con.execute("SELECT copy_status FROM book_copies WHERE copy_id=6").fetchone()[0] == "AVAILABLE"
        assert con.execute("SELECT COUNT(*) FROM loans").fetchone()[0] == before_loans + 1
        con.close()
        print("PASS: late CHECK failure rolled back status and loan header")

        # CHECK constraint rejects an invalid copy status.
        con = sqlite3.connect(db)
        try:
            con.execute("UPDATE book_copies SET copy_status='INVALID' WHERE copy_id=6")
            con.commit()
            raise AssertionError("Invalid copy status passed CHECK constraint")
        except sqlite3.IntegrityError:
            con.rollback()
        finally: con.close()
        print("PASS: invalid copy status rejected by CHECK constraint")

if __name__ == "__main__": main()
