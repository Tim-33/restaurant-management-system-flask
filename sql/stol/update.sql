UPDATE stol
SET restoran_id = %s,
    broj = %s,
    lokacija = %s,
    broj_mjesta = %s
WHERE id = %s
AND disabled = false;