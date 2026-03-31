# AI Dev Basics – Flask REST API

Tämä projekti on yksinkertainen Flask-pohjainen REST API, joka tarjoaa täyden CRUD-toiminnallisuuden (Create, Read, Update, Delete).  
API hallinnoi tuotteiden listaa ja toimii pohjana myöhemmille laajennuksille, kuten:

- JSON-tiedostoon tallennus
- Yksinkertainen HTML-käyttöliittymä
- Mahdolliset AI-toiminnot

---

## 🚀 Ominaisuudet

### ✔ GET /items  
Hakee kaikki tuotteet.

### ✔ POST /items  
Lisää uuden tuotteen.

### ✔ PUT /items/<id>  
Päivittää olemassa olevan tuotteen kokonaan.

### ✔ DELETE /items/<id>  
Poistaa tuotteen.

---

## 🧱 Asennus

### 1. Asenna riippuvuudet
```bash
pip install -r requirements.txt
```

### 2. Käynnistä palvelin
```bash
python app.py
```

### 3. API toimii osoitteessa
```
http://localhost:5000
```

---

## 🧪 Testaus (REST Client)

Projektissa on mukana `test.http`-tiedosto, jota voi käyttää VS Coden REST Client -laajennuksella.

Esimerkkejä:
```http
GET http://localhost:5000/items
```

```http
POST http://localhost:5000/items
Content-Type: application/json

{
  "name": "Example",
  "description": "Test item",
  "price": 9.99,
  "category": "Misc",
  "in_stock": true
}
```

```http
PUT http://localhost:5000/items/1
Content-Type: application/json

{
  "name": "Updated",
  "description": "Updated item",
  "price": 19.99,
  "category": "Misc",
  "in_stock": false
}
```

```http
DELETE http://localhost:5000/items/1
```

---

## 🔧 Teknologiat

- Python 3.11
- Flask
- REST Client (VS Code)

---

## 📌 Tulevat ominaisuudet

- JSON-tiedostoon tallennus (persistenssi)
- HTML-käyttöliittymä API:n päälle
- Parempi virheenkäsittely
- Mahdolliset AI-toiminnot

---

## 👤 Tekijä

**Sami Kultanen**
