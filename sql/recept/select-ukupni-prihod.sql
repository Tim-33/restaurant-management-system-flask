SELECT
    r.naziv AS Recept,
    SUM(s.cijena * sr.kolicina) AS UkupniPrihod
FROM
    recept r
JOIN
    recept_sastojak rs ON r.id = rs.recept_id
JOIN
    sastojak s ON rs.sastojak_id = s.id
JOIN
    stavka_racun sr ON s.id = sr.stavka_id
GROUP BY
    r.naziv;