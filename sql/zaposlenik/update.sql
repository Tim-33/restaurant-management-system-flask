UPDATE zaposlenik
SET restoran_id = %s, 
    zaposlenik_tip = %s, 
    ime = %s, 
    prezime = %s, 
    email = %s, 
    datum_rodenja = %s, 
    iznos_place = %s, 
    slika = %s
WHERE id = %s;