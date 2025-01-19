SELECT naziv, SUM(trenutna_kolicina) AS ukupna_kolicina
	FROM sastojak
		GROUP BY naziv
			ORDER BY ukupna_kolicina DESC;