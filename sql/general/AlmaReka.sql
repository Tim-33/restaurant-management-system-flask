-- 1 upit
SELECT
    r.naziv AS Recept,
    SUM(s.cijena * sr.kolicina) AS UkupniPrihod
FROM
    recept r
JOIN
    recept_sastojak rs ON r.id = rs.recept_id
JOIN
    sastojak s ON rs.sastojak_id = s.id
JOIN
    stavka_racun sr ON s.id = sr.stavka_id
GROUP BY
    r.naziv;
    
    
    
    
-- 2 upit
SELECT
    s.naziv AS Sastojak,
    SUM(rs.kolicina) AS UkupnaKolicina
FROM
    recept_sastojak rs
JOIN
    sastojak s ON rs.sastojak_id = s.id
GROUP BY
    s.naziv
ORDER BY
    UkupnaKolicina DESC;


-- 3 upit
SELECT
    r.naziv AS Recept,
    SUM(s.cijena * sr.kolicina) AS Prihod
FROM
    recept r
JOIN
    recept_sastojak rs ON r.id = rs.recept_id
JOIN
    sastojak s ON rs.sastojak_id = s.id
JOIN
    stavka_racun sr ON rs.sastojak_id = sr.stavka_id
WHERE
    sr.racun_id = 1
GROUP BY
    r.naziv;

-- 1 kompl view
DROP VIEW IF EXISTS RacunUkupnaVrijednost;
CREATE VIEW RacunUkupnaVrijednost AS
SELECT
    r.id AS RacunID,
    r.iznos + r.napojnica AS UkupnaVrijednost
FROM
    racun r;

-- 2 komp view
DROP VIEW IF EXISTS SastojciPoReceptu;
CREATE VIEW SastojciPoReceptu AS
SELECT
    rec.naziv AS Recept,
    sastojak.naziv AS Sastojak,
    rs.kolicina AS PotrebnaKolicina
FROM
    recept rec
JOIN
    recept_sastojak rs ON rec.id = rs.recept_id
JOIN
    sastojak ON rs.sastojak_id = sastojak.id;

-- 1 indeks
CREATE INDEX idx_racun_zaposlenik ON racun(zaposlenik_id);

-- korisnik glavni kuhar koji ima pravo na uvid u stavke, recepte, jelovnike, sastojke. moze mijenjati jelovnike i recepte
DROP USER IF EXISTS 'glavni_kuhar'@'localhost';

CREATE USER 'glavni_kuhar'@'localhost' IDENTIFIED BY 'password';
GRANT SELECT, INSERT, UPDATE ON sustav_za_upravljanje_restoranom.stavka TO 'glavni_kuhar'@'localhost';
GRANT SELECT, INSERT, UPDATE ON sustav_za_upravljanje_restoranom.recept TO 'glavni_kuhar'@'localhost';
GRANT SELECT, INSERT, UPDATE ON sustav_za_upravljanje_restoranom.jelovnik TO 'glavni_kuhar'@'localhost';
GRANT SELECT, INSERT, UPDATE ON sustav_za_upravljanje_restoranom.sastojak TO 'glavni_kuhar'@'localhost';

-- funkcija za racunanje ukupne vrijednosti ukljucujuci napojnicu koristi tablice racun, recept, recept_sastojak, stavka_racun
DROP FUNCTION IF EXISTS UkupnaVrijednostRacuna;

DELIMITER $$
CREATE FUNCTION UkupnaVrijednostRacuna(racunID INT)
RETURNS DECIMAL(10, 2)
DETERMINISTIC
BEGIN
    DECLARE ukupno DECIMAL(10, 2);
    SELECT iznos + napojnica INTO ukupno FROM racun WHERE id = racunID;
    RETURN ukupno;
END$$
DELIMITER ;

-- procedura za ispisivanje svih sastojaka potrebnih za recept ukljucujuci i njihove sastojke 
DROP PROCEDURE IF EXISTS SastojciZaRecept;

DELIMITER $$
CREATE PROCEDURE SastojciZaRecept(receptID INT)
BEGIN
    SELECT
		s.id AS ID,
        s.naziv AS Sastojak,
        rs.kolicina AS PotrebnaKolicina,
        s.kolicina_tip AS KolicinaTip,
        s.slika AS Slika
    FROM
        recept_sastojak rs
    JOIN
        sastojak s ON rs.sastojak_id = s.id
    WHERE
        rs.recept_id = receptID;
END$$
DELIMITER ;

-- okidac za validaciju racuna 

DROP TRIGGER IF EXISTS ValidacijaRacun;

DELIMITER $$
CREATE TRIGGER ValidacijaRacun BEFORE INSERT ON racun
FOR EACH ROW
BEGIN
    IF NEW.iznos < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Iznos racuna ne moze biti manji od nule';
    END IF;
END$$
DELIMITER ;
 
DROP PROCEDURE IF EXISTS NovaRacunTransakcija;

DELIMITER $$
CREATE PROCEDURE NovaRacunTransakcija (
    IN restoranID INT,
    IN zaposlenikID INT,
    IN napojnica DECIMAL(10, 2),
    IN stolID INT,
    IN stavke JSON
)
BEGIN
    DECLARE racunID INT;
    DECLARE stavkaID INT;
    DECLARE kolicina INT;
    DECLARE nova_cijena DECIMAL(10, 2);
    DECLARE ukupna_vrijednost DECIMAL(10, 2) DEFAULT 0;
    DECLARE iterator INT DEFAULT 0;
    DECLARE broj_racuna VARCHAR(31);

    START TRANSACTION;
    
	SELECT CONCAT(DATE_FORMAT(NOW(), '%Y%m%d'), '-', LPAD(IFNULL(MAX(id) + 1, 1), 6, '0'))
    INTO broj_racuna
    FROM racun;

    INSERT INTO racun (restoran_id, zaposlenik_id, napojnica, stol_id, broj_racuna, iznos)
    VALUES (restoranID, zaposlenikID, napojnica, stolID, broj_racuna, 0);

    SET racunID = LAST_INSERT_ID();

    WHILE iterator < JSON_LENGTH(stavke) DO
        SET stavkaID = JSON_UNQUOTE(JSON_EXTRACT(stavke, CONCAT('$[', iterator, '].stavka_id')));
        SET kolicina = JSON_UNQUOTE(JSON_EXTRACT(stavke, CONCAT('$[', iterator, '].kolicina')));

        SELECT cijena INTO nova_cijena FROM stavka WHERE id = stavkaID;
        
        INSERT INTO stavka_racun (racun_id, stavka_id, kolicina)
        VALUES (racunID, stavkaID, kolicina);

        SET ukupna_vrijednost = ukupna_vrijednost + (nova_cijena * CAST(kolicina AS DECIMAL(10, 2)));

        SET iterator = iterator + 1;
    END WHILE;

    UPDATE racun
    SET iznos = ukupna_vrijednost
    WHERE id = racunID;
    
    CALL process_racun_transaction(racunID);

    COMMIT;
END$$
DELIMITER ;
