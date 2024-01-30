import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="<host name>",
    database="<db name>",
    user="<user name>",
    password="<password>"
)

# Create a cursor object
cursor = conn.cursor()

# Create the customer table
cursor.execute("""
    CREATE TABLE customers (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        surname VARCHAR(50),
        address VARCHAR(100),
        nationality VARCHAR(50),
        birthday DATE,
        job_title VARCHAR(50)
    )
""")

# Create an index on the customer table for faster lookups by email
cursor.execute("CREATE INDEX idx_customer_nationality ON customers (nationality)")
cursor.execute("CREATE INDEX idx_customer_birthday ON customers (birthday)")
cursor.execute("CREATE INDEX idx_customer_job_title ON customers (job_title)")

# Create the invoice table
cursor.execute("""
    CREATE TABLE invoices (
        id SERIAL PRIMARY KEY,
        customer_id INT,
        invoice_number INT,
        invoice_date DATE,
        total_price NUMERIC(10, 2),
        FOREIGN KEY (customer_id) REFERENCES customers (id)
    )
""")

# Create an index on the invoice table for faster lookups by customer
cursor.execute("CREATE INDEX idx_invoice_customer_id ON invoices (customer_id)")

# Create the book table
cursor.execute("""
    CREATE TABLE books (
        id SERIAL PRIMARY KEY,
        title VARCHAR(200),
        author VARCHAR(100),
        price NUMERIC(10, 2),
        publishing_house VARCHAR(100)
    )
""")

# Create an index on the book table for faster lookups by title
cursor.execute("CREATE INDEX idx_book_title ON books (title)")

# Create the sold_books table
cursor.execute("""
    CREATE TABLE sold_books (
        id SERIAL PRIMARY KEY,
        invoice_id INT,
        book_id INT,
        FOREIGN KEY (invoice_id) REFERENCES invoices (id),
        FOREIGN KEY (book_id) REFERENCES books (id)
    )
""")

# Create an index on the sold_books table for faster lookups by invoice
cursor.execute("CREATE INDEX idx_sold_books_invoice_id ON sold_books (invoice_id)")

# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()
