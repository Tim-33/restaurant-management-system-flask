UPDATE jelovnik_stavka
SET disabled = true,
    deleted_at = now()
WHERE jelovnik_id = %s
AND stavka_id = %s
AND disabled = false;