import sqlite3, os

current_dir = os.path.dirname(os.path.abspath(__file__))
SQL_FILE = os.path.join(current_dir, "db.SQL")
DB_FILE = os.path.join(current_dir, "MDPDatabase.sqlite")

def apply_sql():
    print("Applying SQL file")
    # Connect to the database (or create it if it doesn't exist)
    conn = sqlite3.connect(DB_FILE)

    # Open and read the SQL file
    with open(SQL_FILE, 'r') as f:
        sql = f.read()

    # Execute the SQL commands in the file
    conn.executescript(sql)

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()
    print("SQL file applied")

if __name__ == "__main__":
    apply_sql()