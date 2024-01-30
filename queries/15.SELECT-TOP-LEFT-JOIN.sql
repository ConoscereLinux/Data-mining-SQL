SELECT
	books.id,
	title,
	author,
	publishing_house,
	price
FROM
	books
LEFT JOIN sold_books ON books.id = sold_books.book_id
WHERE invoice_id IS NULL
LIMIT 10;