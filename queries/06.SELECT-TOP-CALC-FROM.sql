SELECT
	DATE_PART(
		'YEAR',
		AGE(
			NOW(),
			birthday
		)
	) AS AGE,
	birthday,
	nationality
FROM
	customers
LIMIT 10;