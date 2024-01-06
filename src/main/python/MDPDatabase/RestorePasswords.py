import sqlite3

def restore_passwords():
    # Connect to the database (or create it if it doesn't exist)
    conn = sqlite3.connect('MDPDatabase.sqlite')

    # Execute the SQL command
    conn.executescript("DELETE FROM Password")


    # Commit the changes
    conn.commit()

    print("Passwords saved in MDPDatabase.sqlite have been deleted.")

    # Close the connection
    conn.close()

if __name__ == "__main__":
    restore_passwords()