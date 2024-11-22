import sqlite3
import pandas as pd

# Specify your CSV file and SQLite database file
csv_file = "data/clients.csv"  # Replace with your CSV file
db_file = "clients.db"    # Replace with your desired SQLite database file name

# Load the CSV into a DataFrame
df = pd.read_csv(csv_file)

# Connect to SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Create a table based on the DataFrame's structure
columns = ", ".join([f"{col} TEXT" for col in df.columns])
create_table_query = f"CREATE TABLE IF NOT EXISTS clients ({columns})"
cursor.execute(create_table_query)

# Insert data into the table
df.to_sql("clients", conn, if_exists="replace", index=False)

# Commit and close the connection
conn.commit()
conn.close()

print(f"Data from {csv_file} has been imported into {db_file}")
