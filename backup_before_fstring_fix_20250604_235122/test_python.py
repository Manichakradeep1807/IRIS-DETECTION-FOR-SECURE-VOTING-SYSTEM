print("Python is working")
print("Testing basic functionality")

import os
print("Current directory:", os.getcwd())

import sqlite3
print("SQLite3 imported successfully")

# Test database creation
conn = sqlite3.connect("test.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE test (id INTEGER)")
cursor.execute("INSERT INTO test VALUES (1)")
conn.commit()
conn.close()
print("Database test successful")

# Clean up
os.remove("test.db")
print("Test completed successfully")
