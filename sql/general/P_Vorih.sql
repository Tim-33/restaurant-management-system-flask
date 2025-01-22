-- Tablice

CREATE TABLE zaposlenik(
	id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    deleted_at DATETIME,
    disabled BOOLEAN DEFAULT FALSE NOT NULL,
    
    restoran_id INT NOT NULL,
	zaposlenik_tip ENUM('vlasnik', 'kuhar', 'glavni_konobar', 'konobar', 'cistac') DEFAULT 'kuhar' NOT NULL,
    ime VARCHAR (31) NOT NULL,
    prezime VARCHAR (31) NOT NULL,
    email VARCHAR (255) NOT NULL,
    datum_rodenja DATE NOT NULL,
    iznos_place DECIMAL (10, 2) NOT NULL,
    slika BLOB,
    
    FOREIGN KEY (restoran_id) REFERENCES restoran (id)
);

CREATE TABLE zaposlenik_placa (
	id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    deleted_at DATETIME,
    disabled BOOLEAN DEFAULT FALSE NOT NULL,

	zaposlenik_id INT NOT NULL,
    iznos DECIMAL (10, 2) NOT NULL,
    mjesec DATE DEFAULT (CURRENT_DATE()) NOT NULL,
    
    FOREIGN KEY (zaposlenik_id) REFERENCES zaposlenik (id)
);

CREATE TABLE restoran (
	id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    deleted_at DATETIME,
    disabled BOOLEAN DEFAULT FALSE NOT NULL,
    
    naziv VARCHAR (255) NOT NULL,
    adresa VARCHAR (255) NOT NULL,
    broj_telefona VARCHAR (20) UNIQUE NOT NULL,
    slika BLOB
);

CREATE TABLE restoran_racun (
	id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    deleted_at DATETIME,
    disabled BOOLEAN DEFAULT FALSE NOT NULL,
    
    restoran_id INT NOT NULL,
    stanje DECIMAL (10, 2) DEFAULT 0 NOT NULL,
    valuta ENUM ('EUR', 'USD', 'CAD', 'GBP', 'AUD', 'JPY', 'CNY', 'CHF', 'SEK', 'NZD'),
    
    FOREIGN KEY (restoran_id) REFERENCES restoran (id)
);

-- Upiti
-- 1. Prikaz svih zaposlenika s iznosom njihovih mjesečnih plaća u 1. i 6. mjesecu
SELECT zaposlenik.ime, 
zaposlenik.prezime, 
zaposlenik_placa.iznos AS mjesecna_placa, 
zaposlenik_placa.mjesec
FROM zaposlenik
JOIN zaposlenik_placa ON zaposlenik.id = zaposlenik_placa.zaposlenik_id
WHERE MONTH(zaposlenik_placa.mjesec) IN (1, 6);

-- Zaposlenici > Prikaz svih zaposlenika s iznosom njihovih mjesečnih plaća u 1. i 6. mjesecu

-- 2. Restoran koji ima najmanje na računu 
SELECT restoran.naziv AS restoran,
restoran_racun.stanje AS iznos_na_racunu,
restoran_racun.valuta
FROM restoran
JOIN restoran_racun ON restoran.id = restoran_racun.restoran_id
ORDER BY restoran_racun.stanje ASC
LIMIT 1;

-- Restorani > Restoran koji ima najmanje na računu

-- 3. Broj zaposlenika po restoranima i ukupnan iznos izdanih mjesečnih plaća
SELECT restoran.naziv AS restoran, 
       COUNT(DISTINCT zaposlenik.id) AS broj_zaposlenika, 
       SUM(zaposlenik_placa.iznos) AS ukupne_place
FROM restoran
LEFT JOIN zaposlenik ON restoran.id = zaposlenik.restoran_id
LEFT JOIN zaposlenik_placa ON zaposlenik.id = zaposlenik_placa.zaposlenik_id
GROUP BY restoran.naziv;

-- Restorani > Restorani sa podacima o plaćama zaposlenika

-- Pogledi
-- 1. Pogled koji prikazuje prosječni iznos izdanih plaća po restoranima

DROP VIEW IF EXISTS ProsjecnePlaceRadnikaPoRestoranu;

CREATE VIEW ProsjecnePlaceRadnikaPoRestoranu AS
SELECT 
    restoran.id AS restoran_id, 
    restoran.naziv, 
    AVG(zaposlenik_placa.iznos) AS prosjecna_placa
FROM restoran
JOIN zaposlenik ON zaposlenik.restoran_id = restoran.id
JOIN zaposlenik_placa ON zaposlenik.id = zaposlenik_placa.zaposlenik_id
GROUP BY restoran.id;

-- Restorani > Restorani s prosječnom plaćom zaposlenika

-- 2. Pogled koji prikazuje sve plaće po zaposlenicima
DROP VIEW IF EXISTS SvePlace;

CREATE VIEW SvePlace AS
SELECT zaposlenik.ime, 
       zaposlenik.prezime, 
       zaposlenik_placa.iznos AS placa, 
       zaposlenik_placa.mjesec, 
       restoran.naziv AS restoran
FROM zaposlenik
JOIN zaposlenik_placa ON zaposlenik.id = zaposlenik_placa.zaposlenik_id
JOIN restoran ON zaposlenik.restoran_id = restoran.id;

SELECT * FROM SvePlace;

-- Plaće > Sve Plaće

-- Indeksi
-- Dodavanje smislenih indeksa za poboljšanje performansi upita

DROP INDEX indx_restoran_naziv ON restoran;
DROP INDEX indx_zaposlenik_placa_mjesec ON zaposlenik_placa;

CREATE INDEX indx_restoran_naziv ON restoran(naziv);
CREATE INDEX indx_zaposlenik_placa_iznos ON zaposlenik_placa(iznos);

-- Korisnici
-- Stvaranje korisnika "Voditelj skladišta" s odgovarajućim pravima

DROP USER IF EXISTS 'voditelj_skladista'@'localhost';
CREATE USER 'voditelj_skladista'@'localhost' IDENTIFIED BY 'Voditelj_042';

-- Dodjela prava korisniku "Voditelj skladišta"
GRANT SELECT, INSERT, UPDATE ON skladiste TO 'voditelj_skladista'@'localhost';
GRANT SELECT ON narudzba TO 'voditelj_skladista'@'localhost';
GRANT SELECT ON sastojak TO 'voditelj_skladista'@'localhost';

-- Users skroz dolje

-- Funkcija
-- 1. Funkcija za računanje ukupne zarade zaposlenika
DROP FUNCTION IF EXISTS UkupnaZarada;

DELIMITER //
CREATE FUNCTION UkupnaZarada(p_zaposlenik_id INT)
RETURNS DECIMAL(10, 2)
DETERMINISTIC
BEGIN
    DECLARE ukupno DECIMAL(10, 2);
    SELECT SUM(iznos) INTO ukupno
    FROM zaposlenik_placa
    WHERE zaposlenik_id = p_zaposlenik_id;
    RETURN IFNULL(ukupno, 0);
END;
//
DELIMITER ;

-- Zaposlenici > Tablica stupac ukupna zarada

-- Procedura
-- 1. Procedura za procesiranje mjesečne plaće
DROP PROCEDURE IF EXISTS DajPlacu;

DELIMITER //
CREATE PROCEDURE DajPlacu(zaposlenik_id INT, iznos DECIMAL(10, 2), mjesec DATE)
BEGIN
    INSERT INTO zaposlenik_placa (zaposlenik_id, iznos, mjesec)
    VALUES (zaposlenik_id, iznos, mjesec);
END;
//
DELIMITER ;

# Plaće > Plati zaposlenicima plaću

-- 2. Procedura za zaposlenje novog zaposlenika
DROP PROCEDURE IF EXISTS ZaposliRadnika;
DELIMITER //

CREATE PROCEDURE ZaposliRadnika(
    IN restoran_id INT, 
    IN zaposlenik_tip ENUM('vlasnik', 'kuhar', 'glavni_konobar', 'konobar', 'cistac'), 
    IN ime VARCHAR(31), 
    IN prezime VARCHAR(31), 
    IN email VARCHAR(255), 
    IN datum_rodenja DATE, 
    IN iznos_place DECIMAL(10, 2),
    IN slika BLOB
)
BEGIN
    INSERT INTO zaposlenik (restoran_id, zaposlenik_tip, ime, prezime, email, datum_rodenja, iznos_place, slika)
    VALUES (restoran_id, zaposlenik_tip, ime, prezime, email, datum_rodenja, iznos_place, slika);
END;
//
DELIMITER ;

# Zaposlenici > Dodaj zaposlenika

-- Okidač za ažuriranje trenutnog stanja sastojaka nakon narudžbe

DROP TRIGGER IF EXISTS after_narudzba_zavrseno;

DELIMITER //

CREATE TRIGGER after_narudzba_zavrseno
AFTER UPDATE ON narudzba
FOR EACH ROW
BEGIN
    IF NEW.status_narudzbe = 'ZAVRSENO' AND OLD.status_narudzbe <> 'ZAVRSENO' THEN
        UPDATE sastojak s
        JOIN sastojak_narudzba sn ON s.id = sn.sastojak_id
        SET s.trenutna_kolicina = s.trenutna_kolicina + sn.kolicina
        WHERE sn.narudzba_id = NEW.id;
    END IF;
END;
//

DELIMITER ;

# Narudžbe > Kreirak narudžbu > Završi narudžbu
