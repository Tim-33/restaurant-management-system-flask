SELECT  sa.id id, sa.created_at created_at, sa.updated_at updated_at, sa.deleted_at deleted_at, sa.disabled disabled, 
        sa.naziv naziv, sa.cijena cijena, sa.kolicina_tip kolicina_tip, rs.kolicina kolicina, sa.slika slika
FROM sastojak sa
JOIN recept_sastojak rs ON sa.id = rs.sastojak_id
WHERE rs.recept_id = %s
AND sa.disabled = false
AND rs.disabled = false;