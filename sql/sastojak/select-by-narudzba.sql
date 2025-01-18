SELECT  sa.id id, sa.created_at created_at, sa.updated_at updated_at, sa.deleted_at deleted_at, sa.disabled disabled, 
        sa.naziv naziv, 
        sa.cijena cijena, 
        sa.kolicina_tip kolicina_tip, 
        sn.kolicina kolicina,
        sa.slika slika
FROM sastojak sa
JOIN sastojak_narudzba sn ON sa.id = sn.sastojak_id
WHERE sn.narudzba_id = %s
AND sa.disabled = false
AND sn.disabled = false;