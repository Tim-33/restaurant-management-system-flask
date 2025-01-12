SELECT zp.id id, z.ime ime, z.prezime prezime, zp.iznos iznos, zp.mjesec mjesec
FROM zaposlenik_placa zp
JOIN zaposlenik z ON zp.zaposlenik_id = z.id
WHERE zp.mjesec = %s
AND zp.disabled = false;