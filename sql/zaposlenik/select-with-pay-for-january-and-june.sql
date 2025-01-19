SELECT zaposlenik.ime, 
zaposlenik.prezime, 
zaposlenik_placa.iznos AS mjesecna_placa, 
zaposlenik_placa.mjesec
FROM zaposlenik
JOIN zaposlenik_placa ON zaposlenik.id = zaposlenik_placa.zaposlenik_id
WHERE MONTH(zaposlenik_placa.mjesec) IN (1, 6);