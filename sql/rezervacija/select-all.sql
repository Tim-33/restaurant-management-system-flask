SELECT  rez.id id, rez.created_at created_at, rez.updated_at updated_at, rez.deleted_at deleted_at,
        rez.disabled disabled, res.naziv naziv_restoran, s.broj broj_stola, s.broj_mjesta broj_mjesta_stola,
        rez.ime ime, rez.vrijeme vrijeme, rez.broj_osoba broj_osoba
FROM rezervacija rez
JOIN restoran res ON rez.restoran_id = res.id
JOIN stol s ON rez.stol_id = s.id
WHERE rez.disabled = false;