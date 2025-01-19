SELECT 
	s.naziv AS sastojak_naziv, 
	SUM(mns.kolicina) AS ukupna_kolicina, 
	SUM(mns.kolicina * s.cijena) AS ukupni_trosak 
FROM 
	mala_nezgoda mn 
JOIN 
	mala_nezgoda_sastojak mns ON mn.id = mns.mala_nezgoda_id 
JOIN 
	sastojak s ON mns.sastojak_id = s.id 
WHERE 
	mn.deleted_at IS NULL 
GROUP BY 
	s.id, s.naziv 
ORDER BY 
	ukupna_kolicina DESC, ukupni_trosak DESC; 