from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/items')
def items():
    items_list = [
        {"id": 1, "name": "item1"},
        {"id": 2, "name": "item2"}
    ]
    return jsonify(items_list)

if __name__ == '__main__':
    app.run(debug=True)