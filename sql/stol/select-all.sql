SELECT  s.id id, s.created_at created_at, s.updated_at updated_at, s.deleted_at deleted_at,
        s.disabled disabled, r.naziv naziv_restoran, s.broj broj, s.lokacija lokacija, s.broj_mjesta broj_mjesta
FROM stol s
JOIN restoran r ON s.restoran_id = r.id
WHERE s.disabled = false;