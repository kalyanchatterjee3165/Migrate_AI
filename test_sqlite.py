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
