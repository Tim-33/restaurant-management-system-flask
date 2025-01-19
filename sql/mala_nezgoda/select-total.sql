SELECT 
    mn.restoran_id,
    r.naziv AS restoran_naziv,
    SUM(mn.ukupno) AS ukupno_mala_nezgoda
FROM 
    mala_nezgoda mn
JOIN 
    restoran r ON mn.restoran_id = r.id
GROUP BY 
    mn.restoran_id, r.naziv;