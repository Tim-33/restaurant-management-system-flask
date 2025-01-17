UPDATE recept_sastojak
SET disabled = true,
    deleted_at = now()
WHERE recept_id = %s
AND sastojak_id = %s
AND disabled = false;