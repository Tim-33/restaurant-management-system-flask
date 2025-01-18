SELECT
    r.naziv AS Recept,
    SUM(s.cijena * sr.kolicina) AS Prihod
FROM
    recept r
JOIN
    recept_sastojak rs ON r.id = rs.recept_id
JOIN
    sastojak s ON rs.sastojak_id = s.id
JOIN
    stavka_racun sr ON rs.sastojak_id = sr.stavka_id
WHERE
    sr.racun_id = 1
GROUP BY
    r.naziv;