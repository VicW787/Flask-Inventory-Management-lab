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
        "ingredients_text": "Roasted peanuts, sugar, molasses, salt",
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
        "ingredients_text": data.get("ingredients_text", ""), 
        "barcode": data.get("barcode", ""),
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
        "ingredients_text": product.get("ingredients_text", ""),
        "barcode": barcode,
    }


def get_product_by_name(name):
    """Search by name. Returns the first maitch as a dictionary, or None."""
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 1,
    }
    response = requests.get(url, params=params, timeout=10)
    data = response.json

    products = data.get("products", [])
    if len(products) == 0:
        return None

    product = products[0]
    return {
        "product_name": product.get("product_name", "Unknown"),
        "brands": product.get("brands", "Unknown"),
        "ingredients_text": product.get("ingredients_text", ""),
        "barcode": product.get("code", ""),
    }


@app.route("/search/barcode/<barcode>", methods=["GET"])
def search_by_barcode(barcode):
    try:
        product = get_product_by_barcode(barcode)
    except requests.exceptions.RequestException:
        return jsonify({"error": "Could not reach the OpenFoodFacts API"}), 503

    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)


@app.route("/search/name/<name>", methods=["GET"])
def search_by_name(name):
    try:
        product = get_product_by_name(name)
    except requests.exceptions.RequestException:
        return jsonify({"error": "Could not reach the OpenFoodFacts API"}), 503

    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
