SELECT restoran.naziv AS restoran,
restoran_racun.stanje AS iznos_na_racunu,
restoran_racun.valuta
FROM restoran
JOIN restoran_racun ON restoran.id = restoran_racun.restoran_id
ORDER BY restoran_racun.stanje ASC
LIMIT 1;
