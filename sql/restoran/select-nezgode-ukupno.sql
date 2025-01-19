SELECT 
    restoran_id,
    SUM(ukupno) AS ukupna_steta
FROM (
    SELECT restoran_id, ukupno FROM mala_nezgoda
    UNION ALL
    SELECT restoran_id, ukupno FROM velika_nezgoda
) AS sve_nezgode
GROUP BY restoran_id
ORDER BY ukupna_steta DESC;