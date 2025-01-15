SELECT  rac.id id, rac.created_at created_at, rac.updated_at updated_at, rac.deleted_at deleted_at,
        rac.disabled disabled, s.broj broj_stola, res.naziv naziv_restoran, concat(zap.ime, ' ', zap.prezime) naziv_zaposlenik,
        rac.broj_racuna broj_racuna, rac.napojnica napojnica, rac.iznos iznos
FROM racun rac
JOIN restoran res ON rac.restoran_id = res.id
JOIN stol s ON rac.stol_id = s.id
JOIN zaposlenik zap ON rac.zaposlenik_id = zap.id
WHERE rac.disabled = false;