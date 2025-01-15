SELECT  rec.id id, rec.created_at created_at, rec.updated_at updated_at, rec.deleted_at deleted_at,
        rec.disabled disabled, res.naziv naziv_restoran, rec.naziv naziv, rec.upute upute
FROM recept rec
JOIN restoran res ON rec.restoran_id = res.id
WHERE rec.disabled = false;