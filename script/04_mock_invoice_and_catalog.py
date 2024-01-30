import psycopg2
from datetime import datetime
from faker import Faker
import random
from decimal import Decimal
import sys

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="<host name>",
    database="<db name>",
    user="<user name>",
    password="<password>"
)

# Instantiate the Faker object
fake = Faker()

# Specify the number of customers, invoices, and books to generate
max_invoices_per_customer = 10
max_books_per_invoice = 10
max_customer_for_task = 10

customer_cout = 0
invoice_count = 0
book_count = 0
last_customer_id = 0

continue_task = True

while continue_task:
    # Create a cursor object
    cursor = conn.cursor()

    # Retrieve customer IDs from the customers table
    cursor.execute(f"SELECT id FROM customers WHERE id > {last_customer_id}")
    customer_ids = cursor.fetchall()

    # Retrieve book IDs from the books table
    cursor.execute("SELECT id, price FROM books")
    book_data = cursor.fetchall()

    customer_task_count = 0
    # Generate mock data for customers
    for customer_id in customer_ids:
        # Generate a random number of invoices for each customer
        num_invoices = random.randint(1, max_invoices_per_customer)

        customer_cout += 1
        
        for i in range(1, num_invoices + 1):
            invoice_count += 1
            # Generate a random number of books for each invoice
            num_books = random.randint(1, max_books_per_invoice)

            start_date = datetime(2000, 1, 1)
            end_date = datetime(2024, 1, 16)
            invoice_date = fake.date_time_between(start_date=start_date, end_date=end_date)
            
            # Generate random book IDs from the book_ids list
            selected_books = random.sample(book_data, num_books)

            # Calculate the total price of the books in the invoice
            total_price = sum(price for _, price in selected_books)
            
            # Introduce occasional mistakes in the total calculation (10% chance of mistake)
            if random.random() < 0.1:
                total_price += Decimal(random.uniform(0.01, 100))

            # Generate an invoice serial based on the invoice date
            invoice_number = int(invoice_date.strftime("%m%d%H%M"))
            
            # Insert the invoice into the invoice table
            cursor.execute("INSERT INTO invoices (customer_id, invoice_number, invoice_date, total_price) "
                           "VALUES (%s, %s, %s, %s)  RETURNING id",
                           (customer_id, invoice_number, invoice_date, total_price))

            # Insert the books into the sold_books table
            invoice_id = cursor.fetchone()[0]  # Retrieve the last inserted invoice_id
            
            # Insert the books into the invoice_books table
            for book_id, _ in selected_books:
                book_count += 1
                cursor.execute("INSERT INTO sold_books (invoice_id, book_id) VALUES (%s, %s)",
                               (invoice_id, book_id))

            # Print the progress in the same line
            sys.stdout.write(f"\rCustomer {customer_cout:09d} Invoice {invoice_count:011d} Books {book_count:012d} (Last customer id: {customer_id})")
            sys.stdout.flush()

        customer_task_count += 1
        last_customer_id = customer_id[0]

        if customer_task_count >= max_customer_for_task:
            break

    else:
        continue_task = False
        
    # Commit the changes and close the cursor and connection
    conn.commit()
    cursor.close()

conn.close()

print("End")
