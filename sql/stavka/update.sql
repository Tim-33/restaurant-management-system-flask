UPDATE stavka
SET restoran_id = %s,
    recept_id = %s,
    naziv = %s,
    stavka_tip = %s,
    cijena = %s,
    opis = %s,
    slika = %s
WHERE id = %s
AND disabled = false;