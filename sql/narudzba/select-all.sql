SELECT  n.id id,
        n.created_at created_at,
        n.updated_at updated_at,
        n.deleted_at deleted_at,
        n.disabled disabled,
        r.naziv naziv_restoran,
        s.id skladiste_id,
        n.naziv naziv,
        n.status_narudzbe status_narudzbe,
        ukupna_cijena_narudzbe(n.id) ukupna_cijena
FROM narudzba n
JOIN skladiste s ON n.skladiste_id = s.id
JOIN restoran r ON s.restoran_id = r.id
WHERE n.disabled = false;