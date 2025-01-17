UPDATE sastojak
SET skladiste_id = %s,
    naziv = %s,
    cijena = %s,
    kolicina_tip = %s,
    slika = %s,
    potrebna_kolicina = %s,
    trenutna_kolicina = %s
WHERE id = %s
AND disabled = false;