SELECT  s.id id, s.created_at created_at, s.updated_at updated_at, s.deleted_at deleted_at, s.disabled disabled,
        res.naziv naziv_restoran, rec.naziv naziv_recept, s.naziv naziv, s.stavka_tip stavka_tip, s.cijena cijena, 
        s.opis opis, s.slika slika, sr.kolicina kolicina
FROM stavka s
JOIN restoran res ON s.restoran_id = res.id
JOIN recept rec ON s.recept_id = rec.id
JOIN stavka_racun sr ON s.id = sr.stavka_id
WHERE s.disabled = false
AND sr.racun_id = %s;
