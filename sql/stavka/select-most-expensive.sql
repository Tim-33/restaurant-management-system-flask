SELECT restoran.naziv AS naziv_restorana,
       stavka.naziv AS najskuplja_stavka, 
       stavka.cijena AS najvisa_cijena
FROM stavka
	JOIN restoran ON stavka.restoran_id = restoran.id
WHERE (stavka.restoran_id, stavka.cijena) IN (
    SELECT restoran_id, MAX(cijena)
    FROM stavka
    GROUP BY restoran_id
)
ORDER BY najvisa_cijena DESC;