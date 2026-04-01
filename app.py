from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from uuid import uuid4
import os
import json

# --- Perusasetukset ---
app = Flask(__name__)
CORS(app)

DATA_FILE = "data.json"
UPLOAD_FOLDER = "static/images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

CATEGORIES = [
    "Tietokoneet",
    "Kirjat",
    "Näytöt",
    "Työkalut",
    "Muut"
]

# --- Helper-funktiot ---

def load_items():
    """Lataa tuotteet JSON-tiedostosta."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_items(items):
    """Tallentaa tuotteet JSON-tiedostoon."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

def get_next_id():
    """Palauttaa seuraavan vapaan ID:n."""
    items = load_items()
    if not items:
        return 1
    return max(item["id"] for item in items) + 1

# --- Staattinen index.html ---
@app.route("/")
def index():
    return send_from_directory("static", "index.html")

# --- API: Kategoriat ---
@app.get("/categories")
def get_categories():
    return jsonify(CATEGORIES)

# --- API: Hae kaikki tuotteet ---
@app.get("/items")
def get_items():
    return jsonify(load_items()), 200

# --- API: Lisää tuote ---
@app.post("/items")
def add_item():
    name = request.form.get("name")
    description = request.form.get("description")
    price = request.form.get("price")
    stock = request.form.get("stock")
    category = request.form.get("category")

    # --- Validointi ---
    errors = []

    if not name:
        errors.append("Nimi puuttuu.")

    if not description:
        errors.append("Kuvaus puuttuu.")

    try:
        price = float(price)
        if price < 0:
            errors.append("Hinta ei voi olla negatiivinen.")
    except (TypeError, ValueError):
        errors.append("Virheellinen hinta.")

    try:
        stock = int(stock)
        if stock < 0:
            errors.append("Varastosaldo ei voi olla negatiivinen.")
    except (TypeError, ValueError):
        errors.append("Virheellinen varastosaldo.")

    if category not in CATEGORIES:
        errors.append("Virheellinen kategoria.")

    if errors:
        return jsonify({"errors": errors}), 400

    # --- Kuvan tallennus ---
    image_url = None
    if "image" in request.files:
        image = request.files["image"]
        if image.filename:
            original = secure_filename(image.filename)
            unique_id = uuid4().hex
            filename = f"{unique_id}_{original}"

            filepath = os.path.join(UPLOAD_FOLDER, filename)
            image.save(filepath)
            image_url = f"/static/images/{filename}"

    # --- Luo uusi tuote ---
    new_item = {
        "id": get_next_id(),
        "name": name,
        "description": description,
        "price": price,
        "stock": stock,
        "in_stock": stock > 0,
        "category": category,
        "image_url": image_url
    }

    items = load_items()
    items.append(new_item)
    save_items(items)

    return jsonify(new_item), 201

# --- API: Poista tuote ---
@app.delete("/items/<int:item_id>")
def delete_item(item_id):
    items = load_items()
    item = next((i for i in items if i["id"] == item_id), None)

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    # Poista kuva tiedostojärjestelmästä
    if item.get("image_url"):
        image_path = item["image_url"].lstrip("/")
        if os.path.exists(image_path):
            os.remove(image_path)

    # Poista tuote listasta
    items = [i for i in items if i["id"] != item_id]
    save_items(items)

    return jsonify({"message": f"Item {item_id} deleted"}), 200

# --- API: Päivitä tuote ---
@app.put("/items/<int:item_id>")
def update_item(item_id):
    data = request.get_json()
    items = load_items()

    for item in items:
        if item["id"] == item_id:
            item.update({
                "name": data.get("name", item["name"]),
                "description": data.get("description", item["description"]),
                "price": data.get("price", item["price"]),
                "category": data.get("category", item["category"]),
                "in_stock": data.get("in_stock", item["in_stock"])
            })
            save_items(items)
            return jsonify(item), 200

    return jsonify({"error": "Item not found"}), 404

# --- API: Päivitä varastosaldo ---
@app.put("/items/<int:item_id>/stock")
def update_stock(item_id):
    data = request.get_json()
    change = data.get("change", 0)

    items = load_items()
    for item in items:
        if item["id"] == item_id:
            item["stock"] = max(0, item["stock"] + change)
            item["in_stock"] = item["stock"] > 0
            save_items(items)
            return jsonify(item), 200

    return jsonify({"error": "Item not found"}), 404

# --- Käynnistä palvelin ---
if __name__ == "__main__":
    app.run(debug=True)
