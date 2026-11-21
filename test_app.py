import pytest
import requests
from unittest.mock import patch
from app import app, inventory, get_product_by_barcode, get_product_by_name


@pytest.fixture
def client():
    app.config["TESTING"] = True
    inventory.clear()
    inventory.append({
        "id": 1,
        "product_name": "Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Water, almonds",
        "barcode": "111",
        "price": 3.99,
        "stock": 10,
    })
    inventory.append({
        "id": 2,
        "product_name": "Peanut Butter",
        "brands": "Jif",
        "ingredients_text": "Peanuts, salt",
        "barcode": "222",
        "price": 4.49,
        "stock": 20,
    })
    return app.test_client()


def test_get_all_items(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    assert len (response.get_json()) == 2

def test_get_all_items(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert len (response.get_json()["product_name"]) == "Almond Milk"

def test_get_all_items(client):
    response = client.get("/inventory/99")
    assert response.status_code == 404



