UPDATE recept
SET
    restoran_id = %s,
    naziv = %s,
    upute = %s
WHERE id = %s;