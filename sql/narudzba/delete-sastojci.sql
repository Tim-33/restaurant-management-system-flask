UPDATE sastojak_narudzba
SET disabled = true,
    deleted_at = now()
WHERE narudzba_id = %s
AND sastojak_id = %s
AND disabled = false;