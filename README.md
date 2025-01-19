# Dokumentacija Flask Aplikacije

## Struktura Projekta

```
app/
    __init__.py
    config/
        __init__.py
        config.py
    interfaces/
        __init__.py
    router/
        __init__.py
        sql_routes.py
    routes/
        __init__.py
        recept_routes.py
        narudzba_routes.py
        trosak_routes.py
        zaposlenik_routes.py
        ...
    services/
        __init__.py
        recept_service.py
        narudzba_service.py
        trosak_service.py
        zaposlenik_service.py
        ...
    static/
        css/
        js/
        images/
    templates/
        index.html
        recept_create.html
        narudzba_create.html
        trosak_create.html
        zaposlenik_create.html
        ...
    utils/
        __init__.py
        sql_utils.py
certificates/
main.py
README.md
requirements.txt
sql/
    auth/
    jelovnik/
    mala_nezgoda/
    narudzba/
    racun/
    recept/
    restoran/
    restoran_racun/
    rezervacija/
    sastojak/
    skladiste/
    stavka/
    stol/
    transakcija_restoran/
    transakcija_zaposlenik/
    trosak/
venv/
```

## Opis Projekta

Ovaj projekt je web aplikacija za upravljanje restoranom koja omogućuje korisnicima upravljanje narudžbama, računima, receptima, zaposlenicima, skladištima i troškovima. Aplikacija je razvijena koristeći Flask framework i MySQL bazu podataka.

## Instalacija

1. Klonirajte repozitorij:

   ```sh
   git clone <URL_REPOZITORIJA>
   cd <NAZIV_REPOZITORIJA>
   ```

2. Kreirajte virtualno okruženje i aktivirajte ga:

   ```sh
   python -m venv venv
   source venv/bin/activate  # Na Windowsima: venv\Scripts\activate
   ```

3. Instalirajte potrebne pakete:

   ```sh
   pip install -r requirements.txt
   ```

4. Pokrenite aplikaciju:
   ```sh
   flask run
   ```

## Konfiguracija

Konfiguracijske datoteke se nalaze u direktoriju `app/config`. Ovdje možete postaviti različite parametre aplikacije kao što su baza podataka, API ključevi i drugi parametri.

## Struktura Koda

### `app/__init__.py`

Ova datoteka inicijalizira Flask aplikaciju i registrira sve potrebne blueprintove i rute.

```python
from flask import Flask
from app.routes.recept_routes import recept_routes
from app.routes.narudzba_routes import narudzba_routes
from app.routes.trosak_routes import trosak_routes
from app.routes.zaposlenik_routes import zaposlenik_routes
# Import drugih ruta...

def create_app():
    app = Flask(__name__)

    # Registracija blueprintova
    app.register_blueprint(recept_routes, url_prefix='/recept')
    app.register_blueprint(narudzba_routes, url_prefix='/narudzba')
    app.register_blueprint(trosak_routes, url_prefix='/trosak')
    app.register_blueprint(zaposlenik_routes, url_prefix='/zaposlenik')
    # Registracija drugih blueprintova...

    return app
```

### `app/routes`

Ovaj direktorij sadrži sve rute aplikacije. Svaka ruta je definirana u zasebnoj datoteci.

#### Primjer: `app/routes/recept_routes.py`

```python
from flask import Blueprint, request, jsonify
from app.services.recept_service import ReceptService

recept_routes = Blueprint('recept_routes', __name__)
recept_service = ReceptService()

@recept_routes.route('/create', methods=['POST'])
def create_recept():
    data = request.get_json()
    recept_service.create_recept(data)
    return jsonify({'message': 'Recept created successfully'}), 201

@recept_routes.route('/<int:id>', methods=['GET'])
def get_recept(id):
    recept = recept_service.get_recept(id)
    return jsonify(recept)
```

### `app/services`

Ovaj direktorij sadrži sve servisne klase koje obavljaju poslovnu logiku aplikacije.

#### Primjer: `app/services/recept_service.py`

```python
class ReceptService:
    def __init__(self):
        self.cursor = mysql.connection.cursor()

    def create_recept(self, data):
        sql_script = "INSERT INTO recept (naziv, upute) VALUES (%s, %s)"
        self.cursor.execute(sql_script, (data['naziv'], data['upute']))
        mysql.connection.commit()

    def get_recept(self, id):
        sql_script = "SELECT * FROM recept WHERE id = %s"
        self.cursor.execute(sql_script, (id,))
        recept = self.cursor.fetchone()
        return recept
```

### `app/templates`

Ovaj direktorij sadrži sve HTML predloške koji se koriste za prikazivanje stranica.

#### Primjer: `app/templates/recept_create.html`

```django-html
{% extends "index.html" %}
{% block content %}
<h2>Dodaj Recept</h2>
<form action="{{ url_for('recept_routes.create_recept') }}" method="POST">
    <div class="form-group">
        <label for="naziv">Naziv:</label>
        <input type="text" name="naziv" id="naziv" required>
    </div>
    <div class="form-group">
        <label for="upute">Upute:</label>
        <textarea name="upute" id="upute" required></textarea>
    </div>
    <button type="submit">Dodaj Recept</button>
</form>
{% endblock %}
```

### `sql`

Ovaj direktorij sadrži sve SQL skripte koje se koriste za kreiranje i upravljanje bazom podataka.

#### Primjer: `sql/recept/select-all.sql`

```sql
SELECT  rec.id id,
        rec.created_at created_at,
        rec.updated_at updated_at,
        rec.deleted_at deleted_at,
        rec.disabled disabled,
        res.naziv naziv_restoran,
        rec.naziv naziv,
        rec.upute upute
FROM recept rec
JOIN restoran res ON rec.restoran_id = res.id
WHERE rec.disabled = false;
```

## Zaključak

Ova dokumentacija pruža osnovne informacije o strukturi Flask aplikacije, instalaciji, konfiguraciji, korištenju i primjerima koda. Za detaljnije informacije, molimo vas da pregledate kod i komentare unutar projekta.
