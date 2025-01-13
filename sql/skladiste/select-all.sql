SELECT  s.id id, s.created_at created_at, s.updated_at updated_at, s.deleted_at deleted_at, 
        s.disabled disabled, r.naziv naziv, s.stanje stanje
FROM skladiste s
JOIN restoran r ON s.restoran_id = r.id
WHERE s.disabled = false;