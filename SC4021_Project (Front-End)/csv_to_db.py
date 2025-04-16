import sqlite3
import csv

# Define the path to the CSV file
csv_file = 'electricvehicles_with_sentiment.csv'

# Connect to SQLite (or create the database if it doesn't exist)
conn = sqlite3.connect('reddit_data.db')
cursor = conn.cursor()

# Open the CSV file and read its contents
with open(csv_file, 'r', encoding='utf-8-sig', newline='') as f:
    reader = csv.reader(f)
    headers = next(reader)  # Skip the header row

    # Create the table with the column names from the header
    columns = ', '.join(headers)
    create_table_query = f"CREATE TABLE IF NOT EXISTS my_table ({columns})"
    cursor.execute(create_table_query)

    # Insert each row into the table
    for row in reader:
        placeholders = ', '.join(['?'] * len(row))  # Placeholder for values
        insert_query = f"INSERT INTO my_table ({columns}) VALUES ({placeholders})"
        cursor.execute(insert_query, row)

# Commit changes and close the connection
conn.commit()
conn.close()

print(f"CSV data has been successfully imported into SQLite database.")
