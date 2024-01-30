SELECT
	COUNT(books.id) 
FROM
	books
RIGHT JOIN sold_books ON books.id = sold_books.book_id;