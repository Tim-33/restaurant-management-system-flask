SELECT  mn.id id,
        mn.created_at created_at,
        mn.updated_at updated_at,
        mn.deleted_at deleted_at,
        mn.disabled disabled,
        r.naziv naziv_restoran,
        concat(z.ime, ' ', z.prezime) naziv_zaposlenik,
        mn.ukupno ukupno,
        broj_sastojaka_male_nezgode(mn.id) broj_sastojaka
FROM mala_nezgoda mn
JOIN restoran r ON mn.restoran_id = r.id
JOIN zaposlenik z ON mn.zaposlenik_id = z.id
WHERE mn.disabled = false;