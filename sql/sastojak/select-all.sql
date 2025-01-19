SELECT  sa.id id,
        sa.created_at created_at, 
        sa.updated_at updated_at, 
        sa.deleted_at deleted_at, 
        sa.disabled disabled, 
        r.naziv naziv_restoran, 
        sa.skladiste_id skladiste_id, 
        sa.naziv naziv, 
        sa.cijena cijena, 
        sa.kolicina_tip kolicina_tip, 
        sa.slika slika, 
        sa.potrebna_kolicina potrebna_kolicina, 
        sa.trenutna_kolicina trenutna_kolicina,
        treba_naruciti(sa.id) treba_li_naruciti
FROM sastojak sa
JOIN skladiste sk ON sa.skladiste_id = sk.id
JOIN restoran r ON r.id = sk.restoran_id
WHERE sa.disabled = false;