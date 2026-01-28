import sqlite3, os, shutil

DB_PATH = "iris_system.db"
BACKUP = "iris_system_backup_before_users_migration.db"

def main():
    if os.path.exists(DB_PATH):
        shutil.copy2(DB_PATH, BACKUP)
        print("Backup created:", BACKUP)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA table_info(users)")
    cols = [r[1] for r in c.fetchall()]
    print("Current users columns:", cols)
    if "person_id" not in cols:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS users_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                display_name TEXT,
                role TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                totp_secret TEXT,
                person_id INTEGER,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        copyable = [
            col for col in cols
            if col in ("id","username","display_name","role","password_hash","totp_secret","is_active","created_at","updated_at")
        ]
        col_list = ",".join(copyable)
        if col_list:
            c.execute(f"INSERT INTO users_new ({col_list}) SELECT {col_list} FROM users")
        else:
            print("No columns to copy from legacy users table.")
        c.execute("DROP TABLE users")
        c.execute("ALTER TABLE users_new RENAME TO users")
        conn.commit()
        print("Migration applied. users table now includes person_id.")
    else:
        print("No migration needed. person_id already present.")
    conn.close()

if __name__ == "__main__":
    main()



















