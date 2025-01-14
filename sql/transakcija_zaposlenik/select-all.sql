SELECT  tz.id id, tz.created_at created_at, tz.updated_at updated_at, tz.deleted_at deleted_at, 
        tz.disabled disabled, CONCAT(z.ime, ' ', z.prezime) naziv_zaposlenik, tz.naziv naziv, tz.iznos iznos
FROM transakcija_zaposlenik tz
JOIN zaposlenik z ON tz.zaposlenik_id = z.id
WHERE tz.disabled = false;