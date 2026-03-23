from flask import Flask, request, jsonify

app = Flask(__name__)

# Alustava lista tuotteille
items_list = [
    {"id": 1, "name": "Laptop", "description": "Fast laptop", "price": 999.99, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Phone", "description": "Smartphone", "price": 699.99, "category": "Electronics", "in_stock": True},
    {"id": 3, "name": "Book", "description": "Novel", "price": 19.99, "category": "Books", "in_stock": True}
]

# GET /items – hae kaikki tuotteet
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items_list), 200

# POST /items – lisää uusi tuote
@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()

    new_item = {
        "id": len(items_list) + 1,
        "name": data.get("name"),
        "description": data.get("description"),
        "price": data.get("price"),
        "category": data.get("category"),
        "in_stock": data.get("in_stock")
    }

    items_list.append(new_item)
    return jsonify(new_item), 201

# DELETE /items/<id> – poista tuote
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items_list
    item = next((i for i in items_list if i["id"] == item_id), None)

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    items_list = [i for i in items_list if i["id"] != item_id]
    return jsonify({"message": f"Item {item_id} deleted"}), 200

# PUT /items/<id> – päivitä koko tuote
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

    return jsonify(item), 200

# Käynnistä Flask
if __name__ == "__main__":
    app.run(debug=True)
