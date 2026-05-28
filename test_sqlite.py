import sqlite3

DB_PATH = "./output/migrate.db"

conn = sqlite3.connect(DB_PATH)
print(f"Connected to {DB_PATH}")
print("Type 'exit' to quit.\n")

while True:
    query = input("SQL> ").strip()
    if query.lower() == "exit":
        break
    if not query:
        continue
    try:
        rows = conn.execute(query).fetchall()
        for row in rows:
            print(row)
        print(f"({len(rows)} rows)\n")
    except Exception as e:
        print(f"Error: {e}\n")

conn.close()

'''
-- List all tables (like "show db")
SELECT name FROM sqlite_master WHERE type='table';

-- See table schema
PRAGMA table_info(Employee);

-- Select all rows
SELECT * FROM Employee;

-- Limit results
SELECT * FROM Employee LIMIT 10;

-- Filter
SELECT name, email, city FROM Employee WHERE country = 'USA';

-- Count rows
SELECT COUNT(*) FROM Employee;

-- Sort
SELECT name, city, country FROM Employee ORDER BY name ASC LIMIT 20;

-- Search
SELECT * FROM Employee WHERE name LIKE 'J%';

-- Group by
SELECT country, COUNT(*) as total FROM Employee GROUP BY country ORDER BY total DESC;
'''