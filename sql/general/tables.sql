DROP DATABASE IF EXISTS sustav_za_upravljanje_restoranom;
CREATE DATABASE sustav_za_upravljanje_restoranom;
USE sustav_za_upravljanje_restoranom;

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

CREATE TABLE skladiste (
	id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    deleted_at DATETIME,
    disabled BOOLEAN DEFAULT FALSE NOT NULL,
    
    restoran_id INT NOT NULL,
    stanje ENUM('puno', 'prazno', 'kritično', 'normalno') DEFAULT 'prazno' NOT NULL,
    
    FOREIGN KEY (restoran_id) REFERENCES restoran (id)
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

CREATE TABLE trosak (
	id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    deleted_at DATETIME,
    disabled BOOLEAN DEFAULT FALSE NOT NULL,
    
	restoran_id INT NOT NULL,
    naziv VARCHAR (64) NOT NULL,
    iznos DECIMAL (10, 2) NOT NULL,
    mjesecno BOOLEAN DEFAULT FALSE NOT NULL,
    
    FOREIGN KEY (restoran_id) REFERENCES restoran (id)
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

CREATE TABLE racun (
	id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    deleted_at DATETIME,
    disabled BOOLEAN DEFAULT FALSE NOT NULL,

	stol_id INT NOT NULL,
    restoran_id INT NOT NULL,
    zaposlenik_id INT NOT NULL,
    broj_racuna VARCHAR (31),
    napojnica DECIMAL (10, 2) DEFAULT 0 NOT NULL,
    iznos DECIMAL (10, 2) DEFAULT 0 NOT NULL,
    
    FOREIGN KEY (stol_id) REFERENCES stol (id),
    FOREIGN KEY (restoran_id) REFERENCES restoran (id),
    FOREIGN KEY (zaposlenik_id) REFERENCES zaposlenik (id)
);

CREATE TABLE recept (
	id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    deleted_at DATETIME,
    disabled BOOLEAN DEFAULT FALSE NOT NULL,
    
    restoran_id INT NOT NULL,
    naziv VARCHAR (256) NOT NULL,
    upute TEXT NOT NULL,
    
    FOREIGN KEY (restoran_id) REFERENCES restoran (id)
);

CREATE TABLE stavka (
	id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    deleted_at DATETIME,
    disabled BOOLEAN DEFAULT FALSE NOT NULL,
    
    restoran_id INT NOT NULL,
    recept_id INT NOT NULL,
    naziv VARCHAR (31) NOT NULL,
    stavka_tip ENUM ('riba', 'salata', 'meso', 'alkohol', 'gazirano', 'kava', 'prilog', 'juha') NOT NULL,
    cijena DECIMAL (10, 2) NOT NULL,
    opis TEXT NOT NULL,
    slika BLOB,
    
    FOREIGN KEY (restoran_id) REFERENCES restoran (id),
    FOREIGN KEY (recept_id) REFERENCES recept (id)
);

CREATE TABLE stavka_racun (
	id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    deleted_at DATETIME,
    disabled BOOLEAN DEFAULT FALSE NOT NULL,
    
    stavka_id INT NOT NULL,
    racun_id INT NOT NULL,
    kolicina TINYINT UNSIGNED DEFAULT 1 NOT NULL,
    
    FOREIGN KEY (stavka_id) REFERENCES stavka (id),
    FOREIGN KEY (racun_id) REFERENCES racun (id)
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

CREATE TABLE sastojak (
	id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    deleted_at DATETIME,
    disabled BOOLEAN DEFAULT FALSE NOT NULL,
    
    skladiste_id INT NOT NULL,
    naziv VARCHAR (31) NOT NULL,
    cijena DOUBLE (10, 2) NOT NULL,
	kolicina_tip ENUM ('g', 'mg', 'kg', 'l', 'ml', 'kol', 'tsp', 'tbsp') NOT NULL,
    slika BLOB,
    
    potrebna_kolicina INT DEFAULT 0 NOT NULL,
    trenutna_kolicina INT DEFAULT 0 NOT NULL,
    
    FOREIGN KEY (skladiste_id) REFERENCES skladiste (id)
);

CREATE TABLE recept_sastojak (
	id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    deleted_at DATETIME,
    disabled BOOLEAN DEFAULT FALSE NOT NULL,
    
    recept_id INT NOT NULL,
    sastojak_id INT NOT NULL,
    kolicina DECIMAL (10, 2) NOT NULL DEFAULT 1,
    
    FOREIGN KEY (recept_id) REFERENCES recept (id),
    FOREIGN KEY (sastojak_id) REFERENCES sastojak (id)
);

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
