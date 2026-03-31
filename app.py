import json
from flask import Flask, request, jsonify

app = Flask(__name__)

DATA_FILE = "data.json"

# --- Helper functions ---

def load_items():
    """Lataa tuotteet JSON-tiedostosta."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_items(items):
    """Tallentaa tuotteet JSON-tiedostoon."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

# Lataa data käynnistyessä
items_list = load_items()

# --- API endpoints ---

# GET /items – hae kaikki tuotteet
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items_list), 200

# POST /items – lisää uusi tuote
@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()

    new_item = {
        "id": max([i["id"] for i in items_list], default=0) + 1,
        "name": data.get("name"),
        "description": data.get("description"),
        "price": data.get("price"),
        "category": data.get("category"),
        "in_stock": data.get("in_stock")
    }

    items_list.append(new_item)
    save_items(items_list)

    return jsonify(new_item), 201

# DELETE /items/<id> – poista tuote
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items_list
    item = next((i for i in items_list if i["id"] == item_id), None)

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    items_list = [i for i in items_list if i["id"] != item_id]
    save_items(items_list)

    return jsonify({"message": f"Item {item_id} deleted"}), 200

# PUT /items/<id> – päivitä tuote
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    item = next((i for i in items_list if i["id"] == item_id), None)

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    item.update({
        "name": data.get("name"),
        "description": data.get("description"),
        "price": data.get("price"),
        "category": data.get("category"),
        "in_stock": data.get("in_stock")
    })

    save_items(items_list)

    return jsonify(item), 200

# Käynnistä Flask
if __name__ == "__main__":
    app.run(debug=True)
