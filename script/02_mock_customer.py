import psycopg2
from faker import Faker

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="<host name>",
    database="<db name>",
    user="<user name>",
    password="<password>"
)

# Create a cursor object
cursor = conn.cursor()

# Generate mock data for multiple rows
fake = Faker('it_IT')
num_records = 1000000

mock_data = [
    (
        fake.first_name()[:50],
        fake.last_name()[:50],
        fake.address().replace('\n', ', ')[:100],
        fake.country()[:100],
        fake.date_of_birth(minimum_age=18, maximum_age=90),
        fake.job()[:50],
    )
    for _ in range(num_records)
]

# Insert the data into the table
insert_query = '''
    INSERT INTO customers (name, surname, address, nationality, birthday, job_title)
    VALUES (%s, %s, %s, %s, %s, %s)
'''
cursor.executemany(insert_query, mock_data)
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
