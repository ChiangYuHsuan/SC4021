import sqlite3
import csv


csv_file = 'clean_reddit_data.csv'   

conn = sqlite3.connect('reddit_data.db')
cursor = conn.cursor()


cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table in tables:
    table_name = table[0]
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()


    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        column_names = [description[0] for description in cursor.description]
        csv_writer.writerow(column_names)
        csv_writer.writerows(rows)

        print(f"Table {table_name} written to {csv_file}")


conn.close()