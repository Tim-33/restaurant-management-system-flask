SELECT  vl.id id,
        vl.created_at created_at,
        vl.updated_at updated_at,
        vl.deleted_at deleted_at,
        vl.disabled disabled,
        r.naziv naziv_restoran,
        concat(z.ime, ' ', z.prezime) naziv_zaposlenik,
        vl.ukupno ukupno
FROM velika_nezgoda vl
JOIN restoran r ON vl.restoran_id = r.id
JOIN zaposlenik z ON vl.zaposlenik_id = z.id
WHERE vl.disabled = false;