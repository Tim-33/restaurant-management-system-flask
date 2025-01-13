UPDATE skladiste
SET disabled = true,
    deleted_at = now()
WHERE id = %s AND disabled = false;