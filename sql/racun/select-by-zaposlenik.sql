SELECT  r.id id,
        r.created_at created_at,
        r.updated_at updated_at,
        r.deleted_at deleted_at,
        r.disabled disabled,
        s.broj broj_stola,
        r.broj_racuna broj_racuna,
        r.napojnica napojnica,
        r.iznos iznos
FROM racun r
JOIN stol s ON r.stol_id = s.id
WHERE r.zaposlenik_id = %s
AND r.disabled = false;