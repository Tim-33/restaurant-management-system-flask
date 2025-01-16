SELECT  j.id id, j.created_at created_at, j.updated_at updated_at, j.deleted_at deleted_at, j.disabled disabled,
        r.naziv naziv_restoran, j.naziv naziv, j.jelovnik_tip jelovnik_tip
FROM jelovnik j
JOIN restoran r
ON j.restoran_id = r.id
WHERE j.disabled = false
AND j.id = %s;