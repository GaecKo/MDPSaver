import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('MDPdatabase.sqlite')

# Open and read the SQL file
with open('db.SQL', 'r') as f:
    sql = f.read()

# Execute the SQL commands in the file
conn.executescript(sql)

# Commit the changes
conn.commit()

# Close the connection
conn.close()