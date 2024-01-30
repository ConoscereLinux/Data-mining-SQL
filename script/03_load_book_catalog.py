import chardet
import csv
import pathlib
import psycopg2
import random
import sys

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="<host name>",
    database="<db name>",
    user="<user name>",
    password="<password>"
)

# Create a cursor object
cursor = conn.cursor()

# Specify the path to the CSV file containing the books catalog
csv_file_path = pathlib.Path(sys.path[0], "Dataset", "books.csv")

# Specify the custom delimiter character
delimiter = ";"  # Replace with your desired separator character

# Determine the file encoding
with open(csv_file_path, 'rb') as file:
    result = chardet.detect(file.read())
encoding = result['encoding']

# Read the CSV file
with open(csv_file_path, "r", encoding=encoding) as file:
    reader = csv.DictReader(file, delimiter=delimiter)
    
    # Insert each row into the book table
    for index, row in enumerate(reader, start=1):
        title = row["Book-Title"][:200]
        author = row["Book-Author"][:100]
        price = round(random.uniform(0.90, 100.00), 2)
        publishing_house = row["Publisher"][:100]
        
        cursor.execute("INSERT INTO books (title, author, price, publishing_house) VALUES (%s, %s, %s, %s)",
                       (title, author, price, publishing_house))

        # Print the progress in the same line
        sys.stdout.write(f"\rProgress: {index}")
        sys.stdout.flush()        

# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()
