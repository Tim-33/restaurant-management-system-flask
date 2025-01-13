SELECT  rr.id id, rr.created_at created_at, rr.updated_at updated_at, rr.deleted_at deleted_at, 
        rr.disabled disabled, r.naziv naziv, rr.stanje stanje, rr.valuta valuta
FROM restoran_racun rr
JOIN restoran r ON rr.restoran_id = r.id
WHERE rr.disabled = false;