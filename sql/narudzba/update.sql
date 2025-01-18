UPDATE narudzba
SET skladiste_id = %s,
    naziv = %s
WHERE id = %s
AND disabled = false;