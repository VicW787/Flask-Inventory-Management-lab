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
    }
    {
        "id": 3,
        "product_name": "Whole Grain Oats"
        "brands": "Quaker",
        "ingredients_text": "Whole grain rolled oats",
        "barcode": "0030000010204",
        "price": 5.25,
        "stock": 15,
    }
]

