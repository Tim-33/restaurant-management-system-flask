UPDATE restoran 
SET disabled = true,
    deleted_at = CURRENT_TIMESTAMP
WHERE id = %s;