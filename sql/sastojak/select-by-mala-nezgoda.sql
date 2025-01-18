SELECT  sa.id id, 
        sa.created_at created_at, 
        sa.updated_at updated_at, 
        sa.deleted_at deleted_at, 
        sa.disabled disabled, 
        sa.naziv naziv, 
        sa.cijena cijena, 
        sa.kolicina_tip kolicina_tip, 
        mns.kolicina kolicina,
        sa.slika slika
FROM sastojak sa
JOIN mala_nezgoda_sastojak mns ON sa.id = mns.sastojak_id
WHERE mns.mala_nezgoda_id = %s
AND sa.disabled = false
AND mns.disabled = false;