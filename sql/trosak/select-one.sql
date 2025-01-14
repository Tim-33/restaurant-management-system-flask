SELECT  t.id id, t.created_at created_at, t.updated_at updated_at, t.deleted_at deleted_at,
        t.disabled disabled, r.naziv naziv_restoran, t.naziv naziv, t.iznos iznos, t.mjesecno mjesecno
FROM trosak t
JOIN restoran r ON t.restoran_id = r.id
WHERE t.disabled = false
AND t.id = %s;