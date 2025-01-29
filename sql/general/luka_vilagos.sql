-- Tablice

/*
CREATE TABLE narudzba (
	id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    deleted_at DATETIME,
    disabled BOOLEAN DEFAULT FALSE NOT NULL,
    
    skladiste_id INT NOT NULL,
    naziv VARCHAR (31) NOT NULL,
    status_narudzbe ENUM ('ZAVRSENO', 'PONISTENO', 'NERIJESENO') DEFAULT 'NERIJESENO' NOT NULL,
    
    FOREIGN KEY (skladiste_id) REFERENCES skladiste (id)
);

CREATE TABLE sastojak_narudzba (
	id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    deleted_at DATETIME,
    disabled BOOLEAN DEFAULT FALSE NOT NULL,
	
    sastojak_id INT NOT NULL,
    narudzba_id INT NOT NULL,
    kolicina INT UNSIGNED NOT NULL,
    
    FOREIGN KEY (sastojak_id) REFERENCES sastojak (id),
    FOREIGN KEY (narudzba_id) REFERENCES narudzba (id)
);

CREATE TABLE transakcija_restoran (
	id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    deleted_at DATETIME,
    disabled BOOLEAN DEFAULT FALSE NOT NULL,
    
    restoran_racun_id INT NOT NULL,
    iznos DECIMAL (10, 2) DEFAULT 0 NOT NULL,
    naziv VARCHAR (256) DEFAULT 'Transakcija restoran' NOT NULL,
    
    FOREIGN KEY (restoran_racun_id) REFERENCES restoran_racun (id)
);

CREATE TABLE transakcija_zaposlenik (
	id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    deleted_at DATETIME,
    disabled BOOLEAN DEFAULT FALSE NOT NULL,
    
    zaposlenik_id INT NOT NULL,
    iznos DECIMAL (10, 2) DEFAULT 0 NOT NULL,
    naziv VARCHAR (256) DEFAULT 'Transakcija restoran' NOT NULL,
    
    FOREIGN KEY (zaposlenik_id) REFERENCES zaposlenik (id)
);
*/


-- Indeksi

CREATE INDEX idx_transakcija_zaposlenik ON transakcija_zaposlenik(zaposlenik_id);
CREATE INDEX idx_transakcija_restoran ON transakcija_restoran(restoran_racun_id);

-- Korisnik

DROP ROLE IF EXISTS vlasnik;
DROP USER IF EXISTS 'vlasnik'@'localhost';

CREATE ROLE vlasnik;

GRANT SELECT, INSERT, UPDATE, DELETE ON sustav_za_upravljanje_restoranom.restoran TO vlasnik;
GRANT SELECT, INSERT, UPDATE, DELETE ON sustav_za_upravljanje_restoranom.zaposlenik TO vlasnik;
GRANT SELECT, INSERT, UPDATE, DELETE ON sustav_za_upravljanje_restoranom.zaposlenik_placa TO vlasnik;
GRANT SELECT, INSERT, UPDATE, DELETE ON sustav_za_upravljanje_restoranom.skladiste TO vlasnik;
GRANT SELECT, INSERT, UPDATE, DELETE ON sustav_za_upravljanje_restoranom.restoran_racun TO vlasnik;
GRANT SELECT, INSERT, UPDATE, DELETE ON sustav_za_upravljanje_restoranom.trosak TO vlasnik;
GRANT SELECT, INSERT, UPDATE, DELETE ON sustav_za_upravljanje_restoranom.stol TO vlasnik;
GRANT SELECT, INSERT, UPDATE, DELETE ON sustav_za_upravljanje_restoranom.rezervacija TO vlasnik;
GRANT SELECT, INSERT, UPDATE, DELETE ON sustav_za_upravljanje_restoranom.racun TO vlasnik;
GRANT SELECT, INSERT, UPDATE, DELETE ON sustav_za_upravljanje_restoranom.recept TO vlasnik;
GRANT SELECT, INSERT, UPDATE, DELETE ON sustav_za_upravljanje_restoranom.stavka TO vlasnik;
GRANT SELECT, INSERT, UPDATE, DELETE ON sustav_za_upravljanje_restoranom.jelovnik TO vlasnik;
GRANT SELECT, INSERT, UPDATE, DELETE ON sustav_za_upravljanje_restoranom.jelovnik_stavka TO vlasnik;
GRANT SELECT, INSERT, UPDATE, DELETE ON sustav_za_upravljanje_restoranom.sastojak TO vlasnik;
GRANT SELECT, INSERT, UPDATE, DELETE ON sustav_za_upravljanje_restoranom.recept_sastojak TO vlasnik;

GRANT SELECT, INSERT ON sustav_za_upravljanje_restoranom.narudzba TO vlasnik;
GRANT SELECT, INSERT ON sustav_za_upravljanje_restoranom.sastojak_narudzba TO vlasnik;
GRANT SELECT, INSERT ON sustav_za_upravljanje_restoranom.mala_nezgoda TO vlasnik;
GRANT SELECT, INSERT ON sustav_za_upravljanje_restoranom.mala_nezgoda_sastojak TO vlasnik;
GRANT SELECT, INSERT ON sustav_za_upravljanje_restoranom.velika_nezgoda TO vlasnik;
GRANT SELECT, INSERT ON sustav_za_upravljanje_restoranom.velika_nezgoda_stavka TO vlasnik;
GRANT SELECT, INSERT ON sustav_za_upravljanje_restoranom.transakcija_restoran TO vlasnik;
GRANT SELECT, INSERT ON sustav_za_upravljanje_restoranom.transakcija_zaposlenik TO vlasnik;

CREATE USER 'vlasnik'@'localhost' IDENTIFIED BY 'password';
GRANT vlasnik TO 'vlasnik'@'localhost';
SET DEFAULT ROLE vlasnik TO 'vlasnik'@'localhost';

-- Funkcija za računanje ukupne cijene narudžbe

DROP FUNCTION IF EXISTS ukupna_cijena_narudzbe;

DELIMITER //

CREATE FUNCTION ukupna_cijena_narudzbe(narudzba_id INT) 
RETURNS DECIMAL(10, 2)
DETERMINISTIC
BEGIN
    DECLARE ukupna_cijena DECIMAL(10, 2) DEFAULT 0;
    
    SELECT SUM(s.cijena * sn.kolicina)
    INTO ukupna_cijena
    FROM sastojak_narudzba sn
    JOIN sastojak s ON sn.sastojak_id = s.id
    WHERE sn.narudzba_id = narudzba_id;

    RETURN ukupna_cijena;
END;
//

DELIMITER ;

-- Procedura za ažuriranje stanja narudžbe
DROP PROCEDURE IF EXISTS zavrsi_narudzbu;

DELIMITER //

CREATE PROCEDURE zavrsi_narudzbu(IN narudzba_id INT)
BEGIN
    UPDATE narudzba
    SET status_narudzbe = 'ZAVRSENO'
    WHERE id = narudzba_id;

    IF ROW_COUNT() = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No rows updated';
    END IF;
END;
//

DELIMITER ;

-- Okidač za ažuriranje iznosa sastojaka nakon male nezgode

DROP TRIGGER IF EXISTS after_mala_nezgoda_sastojak_insert;

DELIMITER //

CREATE TRIGGER after_mala_nezgoda_sastojak_insert
AFTER INSERT ON mala_nezgoda_sastojak
FOR EACH ROW
BEGIN
    UPDATE sastojak s
    JOIN mala_nezgoda_sastojak mns ON s.id = mns.sastojak_id
    SET s.trenutna_kolicina = s.trenutna_kolicina - NEW.kolicina
    WHERE mns.mala_nezgoda_id = NEW.mala_nezgoda_id AND mns.sastojak_id = NEW.sastojak_id;
END;
//

DELIMITER ;

-- Okidač za ažuriranje iznosa sastojaka nakon velike nezgode

DROP TRIGGER IF EXISTS after_velika_nezgoda_stavka_insert;

DELIMITER //
CREATE TRIGGER after_velika_nezgoda_stavka_insert
AFTER INSERT ON velika_nezgoda_stavka
FOR EACH ROW
BEGIN
    DECLARE v_done INT DEFAULT FALSE;
    DECLARE v_sastojak_id INT;
    DECLARE v_kolicina DECIMAL(10, 2);
    DECLARE v_recept_id INT;
    
    DECLARE cur CURSOR FOR
        SELECT 
            rs.sastojak_id,
            rs.kolicina * NEW.kolicina
        FROM recept_sastojak rs
        WHERE rs.recept_id = (SELECT recept_id FROM stavka WHERE id = NEW.stavka_id);
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_done = TRUE;
    
    SELECT recept_id INTO v_recept_id 
    FROM stavka 
    WHERE id = NEW.stavka_id;
    
    OPEN cur;
    
    read_loop: LOOP
        FETCH cur INTO v_sastojak_id, v_kolicina;
        
        IF v_done THEN
            LEAVE read_loop;
        END IF;
        
        UPDATE sastojak
        SET trenutna_kolicina = trenutna_kolicina - CEILING(v_kolicina)
        WHERE id = v_sastojak_id;
        
    END LOOP;
    
    CLOSE cur;
END;
//
DELIMITER ;

-- Okidač za ažuriranje stanja sastojaka nakon stvaranja računa

DROP TRIGGER IF EXISTS after_stavka_racun_insert;

DELIMITER //
CREATE TRIGGER after_stavka_racun_insert
AFTER INSERT ON stavka_racun
FOR EACH ROW
BEGIN
    DECLARE v_done INT DEFAULT FALSE;
    DECLARE v_sastojak_id INT;
    DECLARE v_kolicina DECIMAL(10, 2);
    DECLARE v_recept_id INT;
    
    DECLARE cur CURSOR FOR
        SELECT 
            rs.sastojak_id,
            rs.kolicina * NEW.kolicina
        FROM stavka s
        JOIN recept_sastojak rs ON rs.recept_id = s.recept_id
        WHERE s.id = NEW.stavka_id;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_done = TRUE;
    
    OPEN cur;
    
    read_loop: LOOP
        FETCH cur INTO v_sastojak_id, v_kolicina;
        
        IF v_done THEN
            LEAVE read_loop;
        END IF;
        
        UPDATE sastojak
        SET trenutna_kolicina = trenutna_kolicina - CEILING(v_kolicina)
        WHERE id = v_sastojak_id;
        
    END LOOP;
    
    CLOSE cur;
END;
//
DELIMITER ;

DROP PROCEDURE IF EXISTS process_financial_transaction;
DROP PROCEDURE IF EXISTS process_racun_transaction;
DROP PROCEDURE IF EXISTS process_trosak_transaction;
DROP PROCEDURE IF EXISTS process_narudzba_transaction;
DROP PROCEDURE IF EXISTS process_zaposlenik_placa_transaction;


DELIMITER //

-- Procedure to upisivanje transakcija restorana

CREATE PROCEDURE process_financial_transaction(
    IN p_restoran_id INT,
    IN p_iznos DECIMAL(10,2),
    IN p_naziv VARCHAR(256)
)
BEGIN
    UPDATE restoran_racun 
    SET stanje = stanje + p_iznos
    WHERE restoran_id = p_restoran_id;
    
    INSERT INTO transakcija_restoran (restoran_racun_id, iznos, naziv)
    SELECT id, p_iznos, p_naziv
    FROM restoran_racun
    WHERE restoran_id = p_restoran_id;
END;
//

-- Procedura za novi račun

CREATE PROCEDURE process_racun_transaction(
    IN p_racun_id INT
)
BEGIN
    DECLARE v_iznos DECIMAL(10,2);
    DECLARE v_restoran_id INT;
    DECLARE v_broj_racuna VARCHAR(31);
    
    SELECT iznos + napojnica, restoran_id, COALESCE(broj_racuna, 'N/A')
    INTO v_iznos, v_restoran_id, v_broj_racuna
    FROM racun
    WHERE id = p_racun_id;
    
    CALL process_financial_transaction(
        v_restoran_id,
        v_iznos,
        CONCAT('Račun: ', v_broj_racuna)
    );
END;
//

-- Procedura za novi trošak

CREATE PROCEDURE process_trosak_transaction(
    IN p_trosak_id INT
)
BEGIN
    DECLARE v_iznos DECIMAL(10,2);
    DECLARE v_restoran_id INT;
    DECLARE v_naziv VARCHAR(64);

    SELECT iznos, restoran_id, naziv
    INTO v_iznos, v_restoran_id, v_naziv
    FROM trosak
    WHERE id = p_trosak_id;
    
    CALL process_financial_transaction(
        v_restoran_id,
        -v_iznos,
        CONCAT('Trošak: ', v_naziv)
    );
END;
//

-- Procedura za završenu narudžbu

CREATE PROCEDURE process_narudzba_transaction(
    IN p_narudzba_id INT
)
BEGIN
    DECLARE v_total_cost DECIMAL(10,2);
    DECLARE v_restoran_id INT;
    DECLARE v_naziv VARCHAR(31);
    
    SELECT 
        n.naziv,
        SUM(sn.kolicina * s.cijena),
        sk.restoran_id
    INTO v_naziv, v_total_cost, v_restoran_id
    FROM narudzba n
    JOIN sastojak_narudzba sn ON sn.narudzba_id = n.id
    JOIN sastojak s ON s.id = sn.sastojak_id
    JOIN skladiste sk ON sk.id = n.skladiste_id
    WHERE n.id = p_narudzba_id
    GROUP BY n.naziv, sk.restoran_id;
    
    CALL process_financial_transaction(
        v_restoran_id,
        -v_total_cost,
        CONCAT('Narudžba: ', v_naziv)
    );
END;
//

-- Procedura za plaću korisnika

CREATE PROCEDURE process_zaposlenik_placa_transaction(
    IN p_zaposlenik_placa_id INT
)
BEGIN
    DECLARE v_iznos DECIMAL(10,2);
    DECLARE v_zaposlenik_id INT;
    DECLARE v_restoran_id INT;
    DECLARE v_mjesec DATE;
    DECLARE v_ime_prezime VARCHAR(63);
    
    SELECT zp.iznos, zp.zaposlenik_id, z.restoran_id, zp.mjesec, 
           CONCAT(z.ime, ' ', z.prezime)
    INTO v_iznos, v_zaposlenik_id, v_restoran_id, v_mjesec, v_ime_prezime
    FROM zaposlenik_placa zp
    JOIN zaposlenik z ON z.id = zp.zaposlenik_id
    WHERE zp.id = p_zaposlenik_placa_id;
    
    CALL process_financial_transaction(
        v_restoran_id,
        -v_iznos,
        CONCAT('Plaća zaposlenika: ', v_ime_prezime)
    );
    
    INSERT INTO transakcija_zaposlenik (zaposlenik_id, iznos, naziv)
    VALUES (v_zaposlenik_id, v_iznos, CONCAT('Plaća za: ', DATE_FORMAT(v_mjesec, '%Y-%m')));
END;
//

DELIMITER ;