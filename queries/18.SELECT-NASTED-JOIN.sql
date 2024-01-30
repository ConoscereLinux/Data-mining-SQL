SELECT
	total_price,
	calcolated_total_price
FROM
	invoices
	LEFT JOIN (
		SELECT
			SUM(books.price) AS calcolated_total_price,
			sold_books.invoice_id
		FROM
			sold_books
			LEFT JOIN books ON sold_books.book_id = books.id
		GROUP BY
			sold_books.invoice_id
	) AS sold_info ON invoices.id = sold_info.invoice_id
WHERE
	total_price <> calcolated_total_price;
