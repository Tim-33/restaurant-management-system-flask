SELECT
    s.naziv AS Sastojak,
    SUM(rs.kolicina) AS UkupnaKolicina
FROM
    recept_sastojak rs
JOIN
    sastojak s ON rs.sastojak_id = s.id
GROUP BY
    s.naziv
ORDER BY
    UkupnaKolicina DESC;