-- TABLICE

CREATE TABLE rezervacija (
	id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    deleted_at DATETIME,
    disabled BOOLEAN DEFAULT FALSE NOT NULL,
    
    restoran_id INT NOT NULL,
    stol_id INT NOT NULL,
    ime VARCHAR (31) NOT NULL,
    vrijeme DATETIME NOT NULL,
    broj_osoba TINYINT UNSIGNED NOT NULL		
);

CREATE TABLE stol (
	id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    deleted_at DATETIME,
    disabled BOOLEAN DEFAULT FALSE NOT NULL,
    
    restoran_id INT NOT NULL,
    broj TINYINT UNSIGNED NOT NULL,
    lokacija ENUM ('unutra', 'vani', 'vip') NOT NULL,
    broj_mjesta TINYINT UNSIGNED NOT NULL,
    
    FOREIGN KEY (restoran_id) REFERENCES restoran (id)
);

CREATE TABLE jelovnik (
	id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    deleted_at DATETIME,
    disabled BOOLEAN DEFAULT FALSE NOT NULL,
    
    restoran_id INT NOT NULL,
    naziv VARCHAR (31) NOT NULL,
    jelovnik_tip ENUM ('pica', 'jela', 'desert') NOT NULL,
    
    FOREIGN KEY (restoran_id) REFERENCES restoran (id)
);

CREATE TABLE jelovnik_stavka (
	id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    deleted_at DATETIME,
    disabled BOOLEAN DEFAULT FALSE NOT NULL,
    
    jelovnik_id INT NOT NULL,
    stavka_id INT NOT NULL,
    
    FOREIGN KEY (jelovnik_id) REFERENCES jelovnik (id),
    FOREIGN KEY (stavka_id) REFERENCES stavka (id)
);

-- UPITI

-- Dohvaćanje broja rezervacija po vrsti lokacije stola za svaki restoran
SELECT s.restoran_id, s.lokacija, COUNT(r.id) AS broj_rezervacija
FROM rezervacija r
JOIN stol s ON r.stol_id = s.id
GROUP BY s.restoran_id, s.lokacija
ORDER BY s.restoran_id, s.lokacija;

# Rezervacije > Rezervacije po lokaciji s brojem

-- Prikazivanje naziva svih jelovnika i broj stavki na svakom od njih
SELECT j.naziv AS naziv_jelovnika, COUNT(js.stavka_id) AS broj_stavki
FROM jelovnik j
LEFT JOIN jelovnik_stavka js ON j.id = js.jelovnik_id
GROUP BY j.id
ORDER BY broj_stavki DESC;

# Jelovnici > Jelovnici s brojem stavka

-- Dohvaćanje svih stavki koje su dodane na jelovnik i koje pripadaju kategoriji "jela"
SELECT st.naziv AS naziv_stavke, st.cijena AS cijena, j.naziv AS naziv_jelovnika
FROM stavka st
JOIN jelovnik_stavka js ON st.id = js.stavka_id
JOIN jelovnik j ON js.jelovnik_id = j.id
WHERE j.jelovnik_tip = 'jela'
ORDER BY st.cijena DESC;

# Jelovnici > Stavke s jelovnika po tipu jela

-- POGLEDI

-- Popis rezervacija s detaljima o stolu
DROP VIEW IF EXISTS pogled_rezervacije_stol;

CREATE VIEW pogled_rezervacije_stol AS
SELECT r.id AS rezervacija_id, r.ime AS ime_gosta, r.vrijeme AS vrijeme_rezervacije, s.broj AS broj_stola, s.lokacija AS lokacija_stola
FROM rezervacija r
JOIN stol s ON r.stol_id = s.id;

# Rezervacije > Rezervacije s podacima o stolu > Sve

-- Broj rezervacija po lokaciji stola
DROP VIEW IF EXISTS pogled_rezervacije_po_lokaciji;

CREATE VIEW pogled_rezervacije_po_lokaciji AS
SELECT s.lokacija AS lokacija_stola, COUNT(r.id) AS broj_rezervacija
FROM stol s
LEFT JOIN rezervacija r ON s.id = r.stol_id
GROUP BY s.lokacija;

SELECT * FROM pogled_rezervacije_po_lokaciji;

# Rezervacije > Broj rezervacija po lokaciji stola

-- Prikaz svih aktivnih rezervacija s informacijama o stolu
DROP VIEW IF EXISTS aktivne_rezervacije;

CREATE VIEW aktivne_rezervacije AS
SELECT r.id AS rezervacija_id, r.ime, r.vrijeme, s.broj AS broj_stola, s.lokacija
FROM rezervacija r
JOIN stol s ON r.stol_id = s.id
WHERE r.deleted_at IS NULL AND r.disabled = FALSE;

SELECT * FROM aktivne_rezervacije;

# Rezervacije > Rezervacije s podacima o stolu

-- INDEXI

-- Brže pretraživanje rezervacija prema vremenu
CREATE INDEX idx_rezervacija_vrijeme ON rezervacija (vrijeme);


-- Pretraživanje stolova prema lokaciji
CREATE INDEX idx_stol_lokacija ON stol (lokacija);


-- KORISNICI

-- tajnik (izdaje plače zaposlenicima, ima uvid u povijest transakcija, zapisuje troškove (mjesečne i jednokratne)
DROP USER IF EXISTS 'tajnik'@'localhost';
CREATE USER 'tajnik'@'localhost' IDENTIFIED BY 'tajnik_password';
GRANT SELECT, INSERT, UPDATE ON zaposlenik_placa TO 'tajnik'@'localhost';
GRANT SELECT, INSERT, UPDATE ON restoran TO 'tajnik'@'localhost';
GRANT SELECT, INSERT, UPDATE ON restoran_racun TO 'tajnik'@'localhost';


-- FUNKCIJE

-- Provjera dostupnosti stola u određenom vremenskom razdoblju
DROP FUNCTION IF EXISTS provjeri_dostupnost_stola;

DELIMITER //
CREATE FUNCTION provjeri_dostupnost_stola(p_stol_id INT, p_vrijeme DATETIME) 
RETURNS BOOLEAN
DETERMINISTIC
BEGIN
    DECLARE dostupno BOOLEAN;
    SELECT NOT EXISTS (
        SELECT 1
        FROM rezervacija
        WHERE stol_id = p_stol_id 
        AND vrijeme BETWEEN p_vrijeme AND DATE_ADD(p_vrijeme, INTERVAL 2 HOUR)
        AND deleted_at IS NULL 
        AND disabled = FALSE
    )
    INTO dostupno;
    RETURN dostupno;
END;
//
DELIMITER ;

# Kreiraj dvije rezervacije - jedna s itim vremenom - druga s različitim vremenom

-- Pronalazak prikladnog stola prema broju mjesta
DROP FUNCTION IF EXISTS pronadi_prikladan_stol;

DELIMITER //
CREATE FUNCTION pronadi_prikladan_stol(restoran_id INT, broj_mjesta INT, lokacija_preference ENUM('unutra', 'vani', 'vip'))
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE prikladan_stol INT;
    SELECT id
    INTO prikladan_stol
    FROM stol
    WHERE restoran_id = restoran_id AND broj_mjesta >= broj_mjesta AND lokacija = lokacija_preference AND deleted_at IS NULL AND disabled = FALSE
    LIMIT 1;
    RETURN prikladan_stol;
END;
//
DELIMITER ;

SELECT pronadi_prikladan_stol(1, 1, 'unutra') as stol;

-- OKIDAČI

-- Validacija dodjele stola i rezervacije
DROP TRIGGER IF EXISTS prije_rezervacije;

DELIMITER //
CREATE TRIGGER prije_rezervacije
BEFORE INSERT ON rezervacija
FOR EACH ROW
BEGIN
    IF NOT provjeri_dostupnost_stola(NEW.stol_id, NEW.vrijeme) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Stol nije dostupan za rezervaciju';
    END IF;
END;
//
DELIMITER ;

# Kreiraj dvije rezervacije - jedna s itim vremenom - druga s različitim vremenom