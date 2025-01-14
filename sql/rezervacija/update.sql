UPDATE rezervacija
SET restoran_id = %s,
    stol_id = %s,
    ime = %s,
    vrijeme = %s,
    broj_osoba = %s
WHERE id = %s
AND disabled = false;