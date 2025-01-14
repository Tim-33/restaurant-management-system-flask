UPDATE trosak
SET restoran_id = %s,
    naziv = %s,
    iznos = %s,
    mjesecno = %s
WHERE id = %s
AND disabled = false;