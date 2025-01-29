-- tablice

/*
CREATE TABLE mala_nezgoda (
	id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    deleted_at DATETIME,
    disabled BOOLEAN DEFAULT FALSE NOT NULL,
		
	restoran_id INT NOT NULL,
	zaposlenik_id INT NOT NULL,
    ukupno DECIMAL (10, 2) NOT NULL DEFAULT 0,
    
    FOREIGN KEY (restoran_id) REFERENCES restoran (id),
    FOREIGN KEY (zaposlenik_id) REFERENCES zaposlenik (id)
);

CREATE TABLE mala_nezgoda_sastojak (
	id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    deleted_at DATETIME,
    disabled BOOLEAN DEFAULT FALSE NOT NULL,
		
	mala_nezgoda_id INT NOT NULL,
    sastojak_id INT NOT NULL,
    kolicina INT UNSIGNED NOT NULL,
    
    
    FOREIGN KEY (mala_nezgoda_id) REFERENCES mala_nezgoda (id),
    FOREIGN KEY (sastojak_id) REFERENCES sastojak (id)
);

CREATE TABLE velika_nezgoda (
	id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    deleted_at DATETIME,
    disabled BOOLEAN DEFAULT FALSE NOT NULL,
		
	restoran_id INT NOT NULL,
	zaposlenik_id INT NOT NULL,
    ukupno DECIMAL (10, 2) NOT NULL DEFAULT 0,
    
    FOREIGN KEY (restoran_id) REFERENCES restoran (id),
    FOREIGN KEY (zaposlenik_id) REFERENCES zaposlenik (id)
);

CREATE TABLE velika_nezgoda_stavka (
	id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    deleted_at DATETIME,
    disabled BOOLEAN DEFAULT FALSE NOT NULL,
		
	velika_nezgoda_id INT NOT NULL,
    stavka_id INT NOT NULL,
    kolicina INT UNSIGNED NOT NULL,
    
    
    FOREIGN KEY (velika_nezgoda_id) REFERENCES velika_nezgoda (id),
    FOREIGN KEY (stavka_id) REFERENCES stavka (id)
);
*/

-- 1. UPIT: Prikaz ukupnog iznosa malih nezgoda po restoranu
SELECT 
    mn.restoran_id,
    r.naziv AS restoran_naziv,
    SUM(mn.ukupno) AS ukupno_mala_nezgoda
FROM 
    mala_nezgoda mn
JOIN 
    restoran r ON mn.restoran_id = r.id
GROUP BY 
    mn.restoran_id, r.naziv;
    
# male nezgode > Ukupni iznos malih nezgoda po restoranu
    
-- 2. UPIT: Popis sastojaka korištenih u "malim nezgodama" s ukupnim količinama

SELECT 
	s.naziv AS sastojak_naziv, 
	SUM(mns.kolicina) AS ukupna_kolicina, 
	SUM(mns.kolicina * s.cijena) AS ukupni_trosak 
FROM 
	mala_nezgoda mn 
JOIN 
	mala_nezgoda_sastojak mns ON mn.id = mns.mala_nezgoda_id 
JOIN 
	sastojak s ON mns.sastojak_id = s.id 
WHERE 
	mn.deleted_at IS NULL 
GROUP BY 
	s.id, s.naziv 
ORDER BY 
	ukupna_kolicina DESC, ukupni_trosak DESC; 
    
# male nezgoode > Sastojci malih nezgoda
        
-- 3. UPIT: Prikaz ukupne štete po restoranu za sve nezgode (male i velike)

SELECT 
    restoran_id,
    SUM(ukupno) AS ukupna_steta
FROM (
    SELECT restoran_id, ukupno FROM mala_nezgoda
    UNION ALL
    SELECT restoran_id, ukupno FROM velika_nezgoda
) AS sve_nezgode
GROUP BY restoran_id
ORDER BY ukupna_steta DESC;

# Restorani > Restorani s ukupnom štetom od nezgoda

-- 4. UPIT: Prikaz svih velikih nezgoda s detaljima o stavkama, uključujući količine i cijene stavki detaljno

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
    
# Velika nezgoda > Velike nezgode s detaljima

-- 5. POGLED: Pregled svih nezgoda po zaposleniku s ukupnim troškovima
DROP VIEW IF EXISTS pregled_nezgoda_po_zaposleniku;

CREATE VIEW pregled_nezgoda_po_zaposleniku AS
SELECT 
    z.id AS zaposlenik_id,
    z.ime AS zaposlenik_ime,
    z.prezime AS zaposlenik_prezime,
    COALESCE(SUM(mn.ukupno), 0) AS ukupno_mala_nezgoda,
    COALESCE(SUM(vn.ukupno), 0) AS ukupno_velika_nezgoda,
    COALESCE(SUM(mn.ukupno), 0) + COALESCE(SUM(vn.ukupno), 0) AS ukupno_trosak
FROM 
    zaposlenik z
LEFT JOIN 
    mala_nezgoda mn ON z.id = mn.zaposlenik_id
LEFT JOIN 
    velika_nezgoda vn ON z.id = vn.zaposlenik_id
GROUP BY 
    z.id, z.ime, z.prezime;
    
SELECT * FROM pregled_nezgoda_po_zaposleniku;

# Zaposlenici > Zaposlenici s podacima o nezgodama

-- 6. Procedura za dohvaćanje detalja male nezgode 
DROP PROCEDURE IF EXISTS detalji_male_nezgode;

DELIMITER //

CREATE PROCEDURE detalji_male_nezgode (IN p_nezgoda_id INT)
BEGIN
    SELECT restoran_id, zaposlenik_id, ukupno, created_at
    FROM mala_nezgoda
    WHERE id = p_nezgoda_id;

    SELECT s.naziv AS sastojak, mns.kolicina
    FROM mala_nezgoda_sastojak mns
    JOIN sastojak s ON mns.sastojak_id = s.id
    WHERE mns.mala_nezgoda_id = p_nezgoda_id;
END//

DELIMITER ;

# mala nezgoda > pregledaj > pregledaj / sakrij detalje

-- 7. Procedura za unos nove male nezgode
DROP PROCEDURE IF EXISTS unos_male_nezgode;

DELIMITER //

CREATE PROCEDURE unos_male_nezgode (
    IN p_restoran_id INT,
    IN p_zaposlenik_id INT,
    IN sastojci JSON
)
BEGIN
    DECLARE nezgoda_id INT;
    DECLARE i INT DEFAULT 0;
    DECLARE sastojak_id INT;
    DECLARE kolicina INT;
    DECLARE sastojci_count INT;

    INSERT INTO mala_nezgoda (restoran_id, zaposlenik_id)
    VALUES (p_restoran_id, p_zaposlenik_id);

    SET nezgoda_id = LAST_INSERT_ID();

    SET sastojci_count = JSON_LENGTH(sastojci);

    WHILE i < sastojci_count DO
        SET sastojak_id = CAST(JSON_UNQUOTE(JSON_EXTRACT(sastojci, CONCAT('$[', i, '].sastojak_id'))) AS UNSIGNED);
        SET kolicina = CAST(JSON_UNQUOTE(JSON_EXTRACT(sastojci, CONCAT('$[', i, '].kolicina'))) AS UNSIGNED);

        INSERT INTO mala_nezgoda_sastojak (mala_nezgoda_id, sastojak_id, kolicina)
        VALUES (nezgoda_id, sastojak_id, kolicina);

        SET i = i + 1;
    END WHILE;
    
    COMMIT;
END //

DELIMITER ;

# Male nezgode > Dodaj malu nezgodu

-- 8. Procedura za unos nove velike nezgode
DROP PROCEDURE IF EXISTS unos_velike_nezgode;

DELIMITER //

CREATE PROCEDURE unos_velike_nezgode (
    IN p_restoran_id INT,
    IN p_zaposlenik_id INT,
    IN stavke JSON
)
BEGIN
    DECLARE nezgoda_id INT;
    DECLARE i INT DEFAULT 0;
    DECLARE stavka_id INT;
    DECLARE kolicina INT;
    DECLARE stavke_count INT;
    DECLARE nova_cijena DECIMAL(10, 2);
    DECLARE ukupna_vrijednost DECIMAL(10, 2) DEFAULT 0;

    INSERT INTO velika_nezgoda (restoran_id, zaposlenik_id)
    VALUES (p_restoran_id, p_zaposlenik_id);

    SET nezgoda_id = LAST_INSERT_ID();

    SET stavke_count = JSON_LENGTH(stavke);

    WHILE i < stavke_count DO
        SET stavka_id = CAST(JSON_UNQUOTE(JSON_EXTRACT(stavke, CONCAT('$[', i, '].stavka_id'))) AS UNSIGNED);
        SET kolicina = CAST(JSON_UNQUOTE(JSON_EXTRACT(stavke, CONCAT('$[', i, '].kolicina'))) AS UNSIGNED);
        
        SELECT cijena INTO nova_cijena FROM stavka WHERE id = stavka_id;

        INSERT INTO velika_nezgoda_stavka (velika_nezgoda_id, stavka_id, kolicina)
        VALUES (nezgoda_id, stavka_id, kolicina);
        
        SET ukupna_vrijednost = ukupna_vrijednost + (nova_cijena * CAST(kolicina AS DECIMAL(10, 2)));

        SET i = i + 1;
    END WHILE;
    
    UPDATE velika_nezgoda
    SET ukupno = ukupna_vrijednost
    WHERE id = nezgoda_id;
    
    COMMIT;
END //

DELIMITER ;

# Velika nezgoda > Dodaj veliku nezgodu

-- 9. Funkcija za dohvaćanje broja sastojaka vezanih za malu nezgodu
DROP FUNCTION IF EXISTS broj_sastojaka_male_nezgode;

DELIMITER //

CREATE FUNCTION broj_sastojaka_male_nezgode (p_mala_nezgoda_id INT)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE broj_sastojaka INT;
    
    SELECT COUNT(*)
    INTO broj_sastojaka
    FROM mala_nezgoda_sastojak
    WHERE mala_nezgoda_id = p_mala_nezgoda_id;
    
    RETURN broj_sastojaka;
END//

DELIMITER ;

# Male nezgode > Tablica stupac Broj sastojaka

-- 10. okidač za automatsko ažuriranje ukupnog iznosa u tablici mala_nezgoda kada se dodaje novi sastojak
DROP TRIGGER IF EXISTS update_iznos_mala_nezgoda;

DELIMITER //

CREATE TRIGGER update_iznos_mala_nezgoda
AFTER INSERT ON mala_nezgoda_sastojak
FOR EACH ROW
BEGIN
    DECLARE sastojak_cijena DECIMAL(10, 2);
    
    SELECT cijena INTO sastojak_cijena
    FROM sastojak
    WHERE id = NEW.sastojak_id;
    
    UPDATE mala_nezgoda
    SET ukupno = ukupno + (sastojak_cijena * NEW.kolicina)
    WHERE id = NEW.mala_nezgoda_id;
END//

DELIMITER ;

-- 11. okidač za automatsko ažuriranje ukupnog iznosa u tablici velika_nezgoda kada se dodaje nova stavka
DROP TRIGGER IF EXISTS update_iznos_velika_nezgoda;

DELIMITER //

CREATE TRIGGER update_iznos_velika_nezgoda
AFTER INSERT ON velika_nezgoda_stavka
FOR EACH ROW
BEGIN
    DECLARE stavka_cijena DECIMAL(10, 2);
    
    SELECT cijena INTO stavka_cijena
    FROM stavka
    WHERE id = NEW.stavka_id;
    
    UPDATE velika_nezgoda
    SET ukupno = ukupno + (stavka_cijena * NEW.kolicina)
    WHERE id = NEW.velika_nezgoda_id;
END//

DELIMITER ;

-- 11. Korisnik: konobar
DROP ROLE IF EXISTS konobar;
DROP USER IF EXISTS 'Patricia_konobar'@'localhost';

CREATE ROLE konobar;
GRANT INSERT, UPDATE ON sustav_za_upravljanje_restoranom.mala_nezgoda TO konobar;
GRANT INSERT, UPDATE ON sustav_za_upravljanje_restoranom.velika_nezgoda TO konobar;
GRANT INSERT, UPDATE ON sustav_za_upravljanje_restoranom.mala_nezgoda_sastojak TO konobar;
GRANT INSERT, UPDATE ON sustav_za_upravljanje_restoranom.velika_nezgoda_stavka TO konobar;
CREATE USER 'Patricia_konobar'@'localhost' IDENTIFIED BY 'patricia12345';
GRANT konobar TO 'Patricia_konobar'@'localhost';
SET DEFAULT ROLE konobar TO 'Patricia_konobar'@'localhost';

-- 13. Indeks: Indeks na restoran_id i zaposlenik_id

CREATE INDEX idx_velika_nezgoda_restoran_zaposlenik ON velika_nezgoda (restoran_id, zaposlenik_id);
