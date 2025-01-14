SELECT  tr.id id, tr.created_at created_at, tr.updated_at updated_at, tr.deleted_at deleted_at, 
        tr.disabled disabled, r.naziv naziv_restoran, tr.naziv naziv, tr.iznos iznos
FROM transakcija_restoran tr
JOIN restoran_racun rr ON tr.restoran_racun_id = rr.id
JOIN restoran r ON rr.restoran_id = r.id
WHERE tr.disabled = false
AND tr.id = %s;