#1 Upit koji računa trošak svakoga restorana na mjesečnoj bazi i nemjesečnoj bazi te računa ukupan trošak i slaže ih po veličini počevši od restorana koji je naviše potrošio. 
SELECT restoran.naziv,
	   SUM(CASE WHEN mjesecno = TRUE THEN iznos ELSE 0 END) AS mjesecni_trosak,
	   SUM(CASE WHEN mjesecno = FALSE THEN iznos ELSE 0 END) AS nemjesecni_trosak,
	   SUM(iznos) AS ukupni_trosak
FROM trosak join restoran on restoran_id=restoran.id
	GROUP BY restoran.naziv
		ORDER BY ukupni_trosak DESC;

#2 Upit koji pronalazi najskuplju stavku u svakom restoranu i zatim sortira te stavke prema cijeni u opadajućem rasporedu.
SELECT restoran.naziv AS naziv_restorana,
       stavka.naziv AS najskuplja_stavka, 
       stavka.cijena AS najvisa_cijena
FROM stavka
	JOIN restoran ON stavka.restoran_id = restoran.id
WHERE (stavka.restoran_id, stavka.cijena) IN (
    SELECT restoran_id, MAX(cijena)
    FROM stavka
    GROUP BY restoran_id
)
ORDER BY najvisa_cijena DESC;

#3 Prikaz najčešće koriščenih sastojaka u svim skladištima. ¸
SELECT naziv, SUM(trenutna_kolicina) AS ukupna_kolicina
	FROM sastojak
		GROUP BY naziv
			ORDER BY ukupna_kolicina DESC;

#4 Pogled koji prikazuje koliko broj stavki po tipu i restoranu.
DROP VIEW IF EXISTS broj_stavki_po_restoranu;
CREATE VIEW broj_stavki_po_restoranu AS
SELECT restoran.naziv AS naziv_restorana, 
       stavka.stavka_tip, 
       COUNT(*) AS broj_stavki
FROM stavka
JOIN restoran ON stavka.restoran_id = restoran.id
	GROUP BY restoran.naziv, stavka.stavka_tip
		ORDER BY restoran.naziv, broj_stavki DESC;

#5 "Kuhar" - ima samo pravo vidjeti podatke o jelovniku, receptima, sastojcima i stavkama.  
DROP ROLE IF EXISTS kuhar;
DROP USER IF EXISTS 'Dinko_nad'@'localhost';
create role kuhar;
GRANT SELECT ON sustav_za_upravljanje_restoranom.jelovnik TO kuhar;
GRANT SELECT ON sustav_za_upravljanje_restoranom.recept TO kuhar;
GRANT SELECT ON sustav_za_upravljanje_restoranom.sastojak TO kuhar;
GRANT SELECT ON sustav_za_upravljanje_restoranom.stavka TO kuhar;
CREATE USER 'Dinko_nad'@'localhost' IDENTIFIED BY 'bravo';
GRANT kuhar TO 'Dinko_nad'@'localhost';
SET DEFAULT ROLE kuhar TO 'Dinko_nad'@'localhost';

#6 Izračunava ukupnu vrijednost svih namjernica koje se trenutno nalaze u skladištu za odabrani restoran 
DROP FUNCTION IF EXISTS cijena_skladista_restorana;

DELIMITER //
CREATE FUNCTION cijena_skladista_restorana(f_restoran_id INT) 
RETURNS DECIMAL(10, 2)
DETERMINISTIC
BEGIN
    DECLARE ukupno DECIMAL(10, 2);
		SELECT SUM(cijena * trenutna_kolicina) INTO ukupno
			FROM sastojak
		JOIN skladiste ON skladiste.id = skladiste_id
		WHERE skladiste.restoran_id = f_restoran_id;
    RETURN ukupno;
END //
DELIMITER ;

#7 Funkcija provjerava razliku između potrebne i trenutne količine sastojaka te vraća "TREBA NARUČITI" ili "NE TREBA NARUČITI" za svaki sastojak.
DROP FUNCTION IF EXISTS treba_naruciti;

DELIMITER //
CREATE FUNCTION treba_naruciti(f_sastojak_id INT)
RETURNS varchar(20)
DETERMINISTIC
BEGIN
    DECLARE ukupno int;
    DECLARE rezultat Varchar(20);
		select trenutna_kolicina-potrebna_kolicina INTO ukupno  
			from sastojak group by id 
				HAVING id=f_sastojak_id;
        If ukupno >=0 then 
			set rezultat="NE TREBA NARUCITI"; 
		else 
        set rezultat="TREBA NARUCITI"; 
			end if;
         	return rezultat;   
END //
DELIMITER ;

#8 Procedura za dodavanje troška u tablicu trošak.
DROP PROCEDURE IF EXISTS dodaj_trosak;

DELIMITER //
CREATE PROCEDURE dodaj_trosak(
    IN p_restoran_id INT,
    IN p_naziv VARCHAR(64),
    IN p_iznos DECIMAL(10, 2),
    IN p_mjesecno BOOLEAN 
)
BEGIN
    IF p_restoran_id IS NULL OR p_naziv IS NULL OR p_iznos IS NULL OR p_mjesecno IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Niste uneli sve podatke, molimo vas da popunite sve parametre!';
    ELSE
        INSERT INTO trosak (restoran_id, naziv, iznos, mjesecno)
        VALUES (p_restoran_id, p_naziv, p_iznos, p_mjesecno);
    END IF;
END //

DELIMITER ;

#9 Procedura za ažuriranje količinu sastojaka.
DROP PROCEDURE IF EXISTS azuriraj_kolicinu_sastojka;

DELIMITER //
CREATE PROCEDURE azuriraj_kolicinu_sastojka(
    IN p_sastojak_id INT,
    IN p_sastojak_naziv VARCHAR(255),
    IN p_nova_kolicina INT
)
BEGIN
    IF NOT EXISTS (SELECT 1 FROM sastojak WHERE id = p_sastojak_id AND naziv = p_sastojak_naziv) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Greška: Sastojak sa unetim ID-om i nazivom ne postoji!';
    END IF;
    IF p_nova_kolicina < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Greška: Nova količina ne može biti negativna!';
    END IF;
    UPDATE sastojak
    SET trenutna_kolicina = p_nova_kolicina
    WHERE id = p_sastojak_id AND naziv = p_sastojak_naziv;

END //

DELIMITER ;

#10 Triggeri koji ažurira stanje skladišta prilikom unosa podataka u tablicu sastojak.
#AŽURIRA SE NAKON INSERT SASTOJAK
DROP TRIGGER IF EXISTS after_sastojak;

DELIMITER //
CREATE TRIGGER after_sastojak
AFTER INSERT ON sastojak
FOR EACH ROW
BEGIN
    DECLARE ukupna_trenutna_kolicina INT;
    DECLARE ukupna_potrebna_kolicina INT;
    DECLARE postotak INT;
    DECLARE novo_stanje ENUM('puno', 'prazno', 'kritično', 'normalno');
    
    SELECT SUM(trenutna_kolicina), SUM(potrebna_kolicina)
    INTO ukupna_trenutna_kolicina, ukupna_potrebna_kolicina
    FROM sastojak
    WHERE skladiste_id = NEW.skladiste_id;

    IF ukupna_potrebna_kolicina > 0 THEN
        SET postotak = (ukupna_trenutna_kolicina / ukupna_potrebna_kolicina) * 100;
        
			IF postotak = 0 THEN
				SET novo_stanje = 'prazno';
			ELSEIF postotak <= 50 THEN
				SET novo_stanje = 'kritično';
			ELSEIF postotak < 100 THEN
				SET novo_stanje = 'normalno';
			ELSE
				SET novo_stanje = 'puno';
			END IF;


        UPDATE skladiste
			SET stanje = novo_stanje
        WHERE id = NEW.skladiste_id;
        
    ELSE
        UPDATE skladiste
			SET stanje = 'prazno'
        WHERE id = NEW.skladiste_id;
    END IF;
END //
DELIMITER ;

#UPDATE TRIGGER
#11 AŽURIRA SE NAKON OBAVLJANJA UPDATE NA TABLICI SASTOJCI 
DROP TRIGGER IF EXISTS after_update_sastojak;

DELIMITER //
CREATE TRIGGER after_update_sastojak
AFTER UPDATE ON sastojak
FOR EACH ROW
BEGIN
    DECLARE ukupna_trenutna_kolicina INT;
    DECLARE ukupna_potrebna_kolicina INT;
    DECLARE postotak INT;
    DECLARE novo_stanje ENUM('puno', 'prazno', 'kritično', 'normalno');
    SELECT SUM(trenutna_kolicina), SUM(potrebna_kolicina)
    INTO ukupna_trenutna_kolicina, ukupna_potrebna_kolicina
    FROM sastojak
    WHERE skladiste_id = NEW.skladiste_id;
    IF ukupna_potrebna_kolicina > 0 THEN
        SET postotak = (ukupna_trenutna_kolicina / ukupna_potrebna_kolicina) * 100;
        IF postotak = 0 THEN
            SET novo_stanje = 'prazno';
        ELSEIF postotak <= 50 THEN
            SET novo_stanje = 'kritično';
        ELSEIF postotak < 100 THEN
            SET novo_stanje = 'normalno';
        ELSE
            SET novo_stanje = 'puno';
        END IF;

        UPDATE skladiste
        SET stanje = novo_stanje
        WHERE id = NEW.skladiste_id;

    ELSE
        UPDATE skladiste
        SET stanje = 'prazno'
        WHERE id = NEW.skladiste_id;
    END IF;
END //

DELIMITER ;