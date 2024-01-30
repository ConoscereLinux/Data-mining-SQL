SELECT
	COUNT(id) AS "CONTEGGIO",
	MAX(
		DATE_PART(
			'YEAR',
			AGE(
				NOW(),
				birthday
			)
		)
	) AS "MAX_AGE",
	MIN(birthday) AS DATA_PRIMO_NATO,
	MIN(
		DATE_PART(
			'YEAR',
			AGE(
				NOW(),
				birthday
			)
		)
	) AS "MAX_AGE",
	MAX(birthday) AS DATA_ULTIMO_NATO
FROM
	customers;