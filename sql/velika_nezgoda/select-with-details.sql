SELECT 
    vn.id AS velika_nezgoda_id, 
    vn.restoran_id,
    vn.zaposlenik_id,
    vn.ukupno AS ukupna_steta, 
    vs.id AS stavka_id, 
    vs.naziv AS stavka_naziv, 
    vns.kolicina, 
    vs.cijena, 
    (vns.kolicina * vs.cijena) AS ukupna_cijena 
FROM 
    velika_nezgoda vn
JOIN 
    velika_nezgoda_stavka vns ON vn.id = vns.velika_nezgoda_id
JOIN 
    stavka vs ON vns.stavka_id = vs.id
ORDER BY 
    velika_nezgoda_id, stavka_id;