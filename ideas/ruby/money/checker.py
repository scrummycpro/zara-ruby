import sqlite3

# Connect to the database
conn = sqlite3.connect("money.db")
c = conn.cursor()

# Execute a SELECT query
c.execute("SELECT * FROM projects")  # Replace "projects" with your table name
rows = c.fetchall()

# Print the results
for row in rows:
    print(row)

# Close the connection
conn.close()

