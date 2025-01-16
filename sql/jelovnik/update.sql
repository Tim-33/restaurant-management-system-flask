UPDATE jelovnik
SET restoran_id = %s,
    naziv = %s,
    jelovnik_tip = %s
WHERE id = %s
AND disabled = false;