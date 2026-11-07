from pathlib import Path
import sqlite3, random, time, statistics, csv, json
ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "benchmark.sqlite"
EVID = ROOT / "evidence"

QUERIES = {
 "Q1_member_active_loans": ("""SELECT l.loan_id, m.full_name, b.title, li.due_on
 FROM loans l JOIN members m ON m.member_id=l.member_id
 JOIN loan_items li ON li.loan_id=l.loan_id
 JOIN book_copies bc ON bc.copy_id=li.copy_id
 JOIN books b ON b.book_id=bc.book_id
 WHERE l.member_id=? AND li.returned_on IS NULL ORDER BY li.due_on""", (42,)),
 "Q2_overdue_active": ("""SELECT li.loan_item_id, li.due_on, l.member_id
 FROM loan_items li JOIN loans l ON l.loan_id=li.loan_id
 WHERE li.returned_on IS NULL AND li.due_on < ? ORDER BY li.due_on""", ("2026-11-01",)),
 "Q3_popular_titles": ("""SELECT b.title, COUNT(*) AS borrow_count
 FROM loan_items li JOIN book_copies bc ON bc.copy_id=li.copy_id
 JOIN books b ON b.book_id=bc.book_id
 GROUP BY b.book_id,b.title ORDER BY borrow_count DESC LIMIT 10""", ()),
 "Q4_title_prefix": ("""SELECT book_id,title FROM books
 WHERE title COLLATE NOCASE >= 'data' AND title COLLATE NOCASE < 'datb'
 ORDER BY title COLLATE NOCASE LIMIT 50""", ())
}

SCHEMA = (ROOT/"portfolio-1-database-design/schema.sql").read_text()

def populate():
    if DB.exists(): DB.unlink()
    c=sqlite3.connect(DB); c.execute("PRAGMA foreign_keys=ON")
    c.executescript(SCHEMA)
    rng=random.Random(8103)
    c.executemany("INSERT INTO members VALUES(?,?,?,?)", [(i,f"Member {i}",f"member{i}@example.test","2025-01-01") for i in range(1,3001)])
    c.executemany("INSERT INTO staff VALUES(?,?,?)", [(i,f"Staff {i}",f"staff{i}@example.test") for i in range(1,11)])
    books=[]
    for i in range(1,1001):
        title = (f"Database Systems {i:04d}" if i % 4 == 0 else f"Community Reading {i:04d}")
        books.append((i,f"978000000{i:04d}",title,"Technology" if i%4==0 else "General",2000+(i%25)))
    c.executemany("INSERT INTO books VALUES(?,?,?,?,?)", books)
    c.executemany("INSERT INTO authors VALUES(?,?)", [(i,f"Author {i}") for i in range(1,501)])
    c.executemany("INSERT INTO book_authors VALUES(?,?)", [(i,((i-1)%500)+1) for i in range(1,1001)])
    c.executemany("INSERT INTO book_copies VALUES(?,?,?,?)", [(i,((i-1)%1000)+1,f"SHELF-{i:05d}","ON_LOAN") for i in range(1,1501)])
    c.executemany("INSERT INTO loans VALUES(?,?,?,?)", [(i,((i-1)%3000)+1,((i-1)%10)+1,"2026-01-01T09:00:00") for i in range(1,8001)])
    items=[]
    for i in range(1,12001):
        copy_id=((i-1)%1500)+1
        issued="2026-01-01"
        due="2026-10-15" if i % 10 == 0 else "2026-12-15"
        returned=None if i>10500 else "2026-10-20"
        loan_id=((i-1)%8000)+1
        items.append((i,loan_id,copy_id,issued,due,returned))
    c.executemany("INSERT INTO loan_items VALUES(?,?,?,?,?,?)", items)
    c.commit(); c.close()
    return {"books":1000,"copies":1500,"members":3000,"loans":8000,"loan_items":12000}

def explain(c, sql, params):
    return [" | ".join(str(v) for v in row) for row in c.execute("EXPLAIN QUERY PLAN "+sql, params).fetchall()]

def measure(c, sql, params, repeats=15):
    c.execute(sql,params).fetchall()
    vals=[]
    for _ in range(repeats):
        t=time.perf_counter_ns(); c.execute(sql,params).fetchall(); vals.append((time.perf_counter_ns()-t)/1_000_000)
    return round(statistics.median(vals),4), round(min(vals),4), round(max(vals),4)

def run():
    profile=populate(); c=sqlite3.connect(DB)
    before={}; after={}; plans={}
    for name,(sql,params) in QUERIES.items():
        before[name]=measure(c,sql,params)
        plans[name+" BEFORE"]=explain(c,sql,params)
    c.executescript("""
      CREATE INDEX idx_books_title_nocase ON books(title COLLATE NOCASE);
      CREATE INDEX idx_book_copies_book ON book_copies(book_id);
      CREATE INDEX idx_loan_items_copy ON loan_items(copy_id);
      CREATE INDEX idx_loan_items_active_due ON loan_items(due_on) WHERE returned_on IS NULL;
      CREATE INDEX idx_loan_items_active_loan ON loan_items(loan_id,due_on) WHERE returned_on IS NULL;
      CREATE INDEX idx_loans_member ON loans(member_id);
      ANALYZE;
    """)
    for name,(sql,params) in QUERIES.items():
        after[name]=measure(c,sql,params)
        plans[name+" AFTER"]=explain(c,sql,params)
    c.close()
    rows=[]
    for name in QUERIES:
        b=before[name][0]; a=after[name][0]
        rows.append({"query":name,"before_median_ms":b,"after_median_ms":a,
                     "change_percent":round(((a-b)/b*100),1) if b else None,
                     "before_min_ms":before[name][1],"before_max_ms":before[name][2],
                     "after_min_ms":after[name][1],"after_max_ms":after[name][2]})
    EVID.mkdir(exist_ok=True)
    with (EVID/"benchmark_summary.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    with (EVID/"query_plans_before_after.txt").open("w") as f:
        for name,lines in plans.items(): f.write(name+"\n"+"\n".join(lines)+"\n\n")
    (EVID/"benchmark_dataset_profile.json").write_text(json.dumps(profile,indent=2))
    (EVID/"benchmark_results.json").write_text(json.dumps(rows,indent=2))
    print("Synthetic benchmark rows:", profile)
    print("Query timing medians (milliseconds; 15 runs each):")
    for row in rows: print(row)
    print("Query plans written to evidence/query_plans_before_after.txt")

if __name__ == "__main__": run()
