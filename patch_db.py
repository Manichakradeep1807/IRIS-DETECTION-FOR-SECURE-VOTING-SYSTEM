import sqlite3

db_path = "iris_system.db"

conn = sqlite3.connect(db_path)
c = conn.cursor()

# Check if person_id already exists
c.execute("PRAGMA table_info(users);")
columns = [row[1] for row in c.fetchall()]

if "person_id" not in columns:
    c.execute("ALTER TABLE users ADD COLUMN person_id INTEGER;")
    print("✅ Added person_id column to users table")
else:
    print("ℹ️ person_id column already exists")

conn.commit()
conn.close()
