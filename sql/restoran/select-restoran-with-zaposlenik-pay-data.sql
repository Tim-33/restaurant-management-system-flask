SELECT restoran.naziv AS restoran, 
       COUNT(DISTINCT zaposlenik.id) AS broj_zaposlenika, 
       SUM(zaposlenik_placa.iznos) AS ukupne_place
FROM restoran
LEFT JOIN zaposlenik ON restoran.id = zaposlenik.restoran_id
LEFT JOIN zaposlenik_placa ON zaposlenik.id = zaposlenik_placa.zaposlenik_id
GROUP BY restoran.naziv;