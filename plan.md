# Što sve treba sadržavati

1. 4 tablice po osobi
2. 3 komplicirana upita po osobi
3. 1 komplicirani pogled po osobi
4. 1 indeks po osobi
5. 1 korisnik po osobi
6. 2 procedura po osobi
7. 1 funkcija po osobi
8. 1 okidač po osobi
9. 1 transakcija po osobi

Svaka osoba piše svoju dokumentaciju.

## Luka 

#### Tablice

1. narudzba
2. sastojak_narudzba
3. transakcija_restoran
4. transakcija_zaposlenik

#### Upiti

3 ili više upita po volji koji sadržava navedene tablice

#### Pogled

1 ili više pogleda po volji koji sadržava navedene tablice

#### Indeksi

1 ili više smislenih indeksa na navedene tablice

#### Korisnici

"Vlasnik" - ima privilegije pregledavati i mijenjati sve osim transakcija

#### Funkcija

Funkcija za računanje ukupne cijene narudžbe

#### Procedura

Procedura za ažuriranje stanja narudžbe

#### Okidač

Okidači za automatsko kreiranje transakcija

#### Transakcija

Transakcija za procesiranje narudžbe

## Patricia

#### Tablice

1. mala_nezgoda
2. velika_nezgoda
3. mala_nezgoda_sastojak
4. velika_nezgoda_stavka

#### Upiti

3 ili više upita po volji koji sadržava navedene tablice

#### Pogled

1 ili više pogleda po volji koji sadržava navedene tablice

#### Indeksi

1 ili više smislenih indeksa na navedene tablice

#### Korisnici

"Konobar" - ima privilegiju samo izdavati račune i zapisivati nezgode koje je napravio, i kreirati/uređivati rezervacije

#### Funkcija

Funkcija za računanje ukupne cijene nezgoda

#### Procedura

Procedura za zapisivanje incidenata

#### Okidač

Okidači za updatanje nezgoda kada se dodaju novi itemi

#### Transakcija

Transakcija za računanje odgovornosti za transakciju

## Dinko

#### Tablice

1. skladiste
2. sastojak
3. stavka
4. trosak

#### Upiti

3 ili više upta po volji koji sadržava navedene tablice

#### Pogled

1 ili više pogleda po volji koji sadržava navedene tablice

#### Indeksi

1 ili više smislenih indeksa na navedene tablice

#### Korisnici

"Kuhar" - ima samo pravo vidjeti podatke o jelovniku, receptima, sastojcima i stavkama

#### Funkcija

Funkcija za računanje ukupne vrijednosti skladišta

Funkcija za vračanje svih sastojaka koji se trebaju naručiti

#### Procedura

Procedura za dodavanje troška

Procedura za ažuriranje količinu sastojaka

procedura za stvaranje nove stavke sa računanjem cijene

#### Okidač

Okidač za praćenje stanja skladišta - kada nešto nedostaje

## Paula

#### Tablice

1. zaposlenik
2. zaposlenik_placa
3. restoran
4. restoran_racun

#### Upiti

3 ili više upita po volji koji sadržava navedene tablice

#### Pogled

1 ili više pogleda po volji koji sadržava navedene tablice

#### Indeksi

1 ili više smislenih indeksa na navedene tablice

#### Korisnici

"Voditelj skladišta" - može stvarati narudžbe i ima uvid u stanje skladišta i prijašnjih narudžbi

#### Funkcija

Funkcija za računanje ukupne zarade zaposlenika

#### Procedura

Procedura za procesiranje mjesečne plaće

Procedura za zaposlenje novog zaposlenika

#### Okidač

Okidači za ažuriranje restoranskog računa kada dođe nova restoranska transakcija

## Sara

#### Tablice

1. rezervacija
2. stol
3. jelovnik
4. jelovnik_stavka

#### Upiti

3 ili više upita po volji koji sadržava navedene tablice

#### Pogled

1 ili više pogleda po volji koji sadržava navedene tablice

#### Indeksi

1 ili više smislenih indeksa na navedene tablice

#### Korisnici

"Tajnik" - izdaje plače zaposlenicima, ima uvid u povijest transakcija, zapisuje troškove (mjesečne i jednokratne)

#### Funkcija

Funkcija za provjere dostupnosti stola

Funkcija za pronalazak prikladnog stola

#### Procedura

Procedura za stvaranje rezervacije

Procedura za upravu stavkama na jelovniku

#### Okidač

Okidač za validaciju dodjele stola i rezervacije

## Alma

#### Tablice

1. racun
2. recept
3. recept_sastojak
4. stavka_racun

#### Upiti

3 ili više upita po volji koji sadržava navedene tablice

#### Pogled

1 ili više pogleda po volji koji sadržava navedene tablice

#### Indeksi

1 ili više smislenih indeksa na navedene tablice

#### Korisnici

"Glavni kuhar" - ima pravo na uvid u stavke, recepte, jelovnike, sastojke. Može mijenjati jelovnike i recepte.

#### Funkcija

Funkcija za računanje ukupne vrijednosti, uključujući napojnicu

#### Procedura

Procedura za ispisivanje svih sastojaka potrebnih za recept uključujući i njihove sastojke

#### Okidač

Okidač za validaciju računa

#### Transakcija

Transakcija za stvaranje novog računa s stavkama

