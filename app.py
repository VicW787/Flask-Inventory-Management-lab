from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar",
        "barcode": "0025293001015",
        "price": 3.99,
        "stock": 25,
    },
    {
        "id": 2,
        "product_name": "Crunchy Peanut Butter",
        "brands": "Jif",
        "ingredients_text": "Roassted peanuts, sugar, molasses, salt",
        "barcode": "0051500240006",
        "price": 4.49,
        "stock": 40,
    },
    {
        "id": 3,
        "product_name": "Whole Grain Oats",
        "brands": "Quaker",
        "ingredients_text": "Whole grain rolled oats",
        "barcode": "0030000010204",
        "price": 5.25,
        "stock": 15,
    }
]

@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory)


@app.route("/inventory/<int:id>", methods=["GET"])
def get_item(id):
    item = next((i for i in inventory if i["id"] == id), None)
    if item is None:
        return jsonify({"error": "Item is not found"}), 404
    return jsonify(item)

@app.route("/inventory", methods=["POST"])
def create_item():
    data = request.get_json()
    if "product_name" not in data:
        return jsonify({"error": "product_name is required"}), 400

    new_id = max([i["id"] for i in inventory]) + 1 if inventory else 1
    new_item = {
        "id": new_id,
        "product_name": data["product_name"],
        "brands": data.get("brands", ""),
        "ingredients_text": data.get("ingredients_text"), "barcode": data.get("barcode", ""),
        "price": data.get("price", 0),
        "stock": data.get("stock", 0),
    }
    inventory.append(new_item)
    return jsonify(new_item), 201

@app.route("/inventory/<int:id>", methods=["PATCH"])
def update_item(id):
    item = next((i for i in inventory if i["id"] == id), None)
    if item is None:
        return jsonify({"error": "Item not found"}), 404


    data = request.get_json()
    for field in ["product_name", "brands", "ingredients_text", "barcode", "price", "stock"]:
        if field in data:
            item[field] = data[field]
            return jsonify(item)


@app.route("/inventory/<int:id>", methods=["DELETE"])
def delete_item(id):
    item = next((i for i in inventory if i["id"] == id), None)
    if item is None:
        return jsonify({"error": "Item not found"}), 404

    inventory.remove(item)
    return jsonify({"message": "Item deleted"})


def get_product_by_barcode(barcode):
    """Look up a product by barcode. Returns a dictionary, or None if not found."""
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url, timeout=10)
    data = response.json()

    if data.get("status") != 1:
        return None

    product = data["product"]
    return {
        "product_name": product.get("product_name", "Unknown"),
        "brands": product.get("brands", "Unknown"),
        "ingredients_text": product.get("Ingredients_text", ""),
        "barcode": barcode,
    }






















OPEN_FOOD_FACTS = "https://world.openfoodfacts.org"

def find_item(item_id):
    """Return the item with this id, or None if it does not exist."""
    for item in inventory:
        if item["id"] == item_id:
            return item
        return None


def get_next_id():
    """Return the next free id"""

if __name__ == "__main__":
    app.run(port=5555, debug=True)