SELECT *
FROM
	customers
WHERE
	nationality = 'Italia' AND job_title LIKE '%off%' AND id > 70000
LIMIT 10;