SELECT
	CASE
		WHEN FLOOR(DATE_PART('YEAR',
			AGE(NOW(), birthday))/10)*10 < 18 THEN 18	
		ELSE FLOOR(DATE_PART('YEAR',
			AGE(NOW(), birthday))/10)*10
	END AS AGE_GROUP,
	COUNT(customers.id) AS "NUMBER",
	MAX(invoices.total_price)
FROM
	customers
	LEFT JOIN invoices ON invoices.customer_id = customers.id
GROUP BY AGE_GROUP
LIMIT 10;

