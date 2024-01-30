SELECT
	DATE_PART(
		'YEAR',
		AGE(
			NOW(),
			birthday
		)
	) AS AGE,
	COUNT(id) AS "NUMBER"
FROM
	customers
GROUP BY AGE
LIMIT 10;