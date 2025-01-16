SELECT  s.id id, s.created_at created_at, s.updated_at updated_at, s.deleted_at deleted_at, s.disabled disabled,
        res.naziv naziv_restoran, rec.naziv naziv_recept, s.naziv naziv, s.stavka_tip stavka_tip, s.cijena cijena, 
        s.opis opis, s.slika slika
FROM stavka s
JOIN restoran res ON s.restoran_id = res.id
JOIN recept rec ON s.recept_id = rec.id
JOIN jelovnik_stavka js ON s.id = js.stavka_id
WHERE s.disabled = false
AND js.disabled = false
AND js.jelovnik_id = %s;
