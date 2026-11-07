from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "library.db"
SCHEMA = ROOT / "portfolio-1-database-design" / "schema.sql"
SEED = ROOT / "portfolio-1-database-design" / "seed.sql"

def build(db_path=DB):
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists(): db_path.unlink()
    con = sqlite3.connect(db_path)
    try:
        con.execute("PRAGMA foreign_keys = ON")
        con.executescript(SCHEMA.read_text(encoding="utf-8"))
        con.executescript(SEED.read_text(encoding="utf-8"))
        fk = con.execute("PRAGMA foreign_key_check").fetchall()
        if fk: raise RuntimeError(f"Foreign-key violations: {fk}")
        counts = {t: con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                  for t in ["members","staff","authors","books","book_authors","book_copies","loans","loan_items"]}
        return counts
    finally:
        con.close()

if __name__ == "__main__":
    print("Database build: PASS")
    print(build())
