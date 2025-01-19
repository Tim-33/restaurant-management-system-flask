SELECT
    s.id AS ID,
    s.naziv AS Sastojak,
    rs.kolicina AS PotrebnaKolicina,
    s.kolicina_tip AS KolicinaTip,
    s.slika AS Slika
FROM
    recept_sastojak rs
JOIN
    sastojak s ON rs.sastojak_id = s.id
WHERE
    rs.recept_id = %s;