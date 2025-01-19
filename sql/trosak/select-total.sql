SELECT restoran.naziv,
       SUM(CASE WHEN mjesecno = TRUE THEN iznos ELSE 0 END) AS mjesecni_trosak,
       SUM(CASE WHEN mjesecno = FALSE THEN iznos ELSE 0 END) AS nemjesecni_trosak,
       SUM(iznos) AS ukupni_trosak
FROM trosak join restoran on restoran_id=restoran.id
	GROUP BY restoran.naziv
		ORDER BY ukupni_trosak DESC;