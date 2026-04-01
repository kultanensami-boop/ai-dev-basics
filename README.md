AI Dev Basics – Flask Full‑Stack Inventory App
Tämä projekti on ensimmäinen harjoitus osana laajempaa kokonaisuutta, jossa opettelen AI‑kehittäjän taitoja ja rakennan täyden kehityspolun backendistä käyttöliittymään ja myöhemmin tekoälytoimintoihin.
Tavoitteena on oppia modernin ohjelmistokehityksen peruspalikat ja rakentaa vaihe vaiheelta kohti tuotantotasoista AI‑sovellusta.

Tämä sovellus on Flask‑pohjainen full‑stack‑projekti, joka tarjoaa täyden CRUD‑toiminnallisuuden (Create, Read, Update, Delete), kuvan latauksen, kategoriasuodatuksen ja responsiivisen HTML‑käyttöliittymän.
Sovellus toimii pohjana myöhemmille laajennuksille, kuten tietokantaintegraatiolle, autentikaatiolle ja AI‑toiminnoille.

🚀 Ominaisuudet
✔ GET /items
Hakee kaikki tuotteet.

✔ POST /items
Lisää uuden tuotteen (FormData + kuvan lataus).

✔ PUT /items/<id>
Päivittää olemassa olevan tuotteen.

✔ PUT /items/<id>/stock
Muokkaa varastosaldoa (+ / –).

✔ DELETE /items/<id>
Poistaa tuotteen ja siihen liittyvän kuvan.

✔ Frontend‑ominaisuudet
– Tuotekortit
– Placeholder‑kuva tuotteille ilman kuvaa
– Kategoriasuodatus
– Varastosaldon päivitys
– Responsiivinen layout
– Kuvan lataus uniikilla tiedostonimellä

🧱 Asennus
1. Asenna riippuvuudet
pip install -r requirements.txt

2. Käynnistä palvelin
python app.py

3. Sovellus toimii osoitteessa
http://localhost:5000

🧪 Testaus (REST Client)
Projektissa on mukana test.http‑tiedosto, jota voi käyttää VS Coden REST Client ‑laajennuksella.

Esimerkkejä:

GET http://localhost:5000/items

PUT http://localhost:5000/items/1/stock
Content-Type: application/json
{ "change": -1 }

DELETE http://localhost:5000/items/1

🔧 Teknologiat
– Python 3.11
– Flask
– HTML / CSS
– JavaScript
– JSON‑persistenssi
– REST Client (VS Code)

📌 Tulevat ominaisuudet
– Tietokantaintegraatio (SQLite / PostgreSQL)
– Käyttäjätilit ja kirjautuminen
– Hakutoiminto
– AI‑pohjainen tuotesuositus / kategorisointi

👤 Tekijä
Sami Kultanen  
Ensimmäinen askel matkalla AI‑kehittäjäksi.
