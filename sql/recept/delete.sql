UPDATE recept
SET
    deleted_at = now(),
    disabled = true
WHERE id = %s;