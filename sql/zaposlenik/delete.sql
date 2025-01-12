UPDATE zaposlenik 
SET disabled = true
    deleted_at = now()
WHERE id = %s;