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

def test_get_one_item(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["product_name"] == "Almond Milk"

def test_get_item_not_found(client):
    response = client.get("/inventory/99")
    assert response.status_code == 404


def test_create_item(client):
    new_item = {"product_name": "Cereal", "price": 2.5, "stock": 30}
    response = client.post("/inventory", json=new_item)
    assert response.status_code == 201
    assert response.get_json()["id"] == 3
    assert len(inventory) == 3

def test__create_item_missing_name(client):
    response = client.post("/inventory", json={"price": 2.5})
    assert response.status_code == 400


def test_update_item(client):
    response = client.patch("/inventory/1", json={"price": 9.99, "stock": 5})
    assert response.status_code == 200
    assert response.get_json()["price"] == 9.99
    assert inventory[0]["stock"] == 5


def test_update_item_not_found(client):
    response = client.patch("/inventory/99", json={"price": 1})
    assert response.status_code == 404


def test_delete_item(client):
    response = client.delete("/inventory/1")
    assert response.status_code == 200
    assert len(inventory) == 1


def test_delete_item_not_found(client):
    response = client.delete("/inventory/99")
    assert response.status_code == 404


@patch("app.requests.get")
def test_get_product_by_barcode_found(mock_get):
    mock_get.return_value.json.return_value = {
        "status": 1,
        "product": {"product_name": "Nutella", "brands": "Ferrero", "ingredients_text": "Sugar"},
    }
    product = get_product_by_barcode("3017620422003")
    assert product["product_name"] == "Nutella"
    assert product["barcode"] == "3017620422003"


@patch("app.requests.get")
def test_get_product_by_barcode_not_found(mock_get):
    mock_get.return_value,json.return_value = {"status": 0}
    assert get_product_by_barcode("000") is None


@patch("app.requests.get")
def test_get_product_by_name_found(mock_get):
    mock_get.return_value.json.return_value = {
        "products": [{"product_name": "Oat Milk", "brands": "Oatly", "ingredients_text": "Oats", "code": "123"}]
    }
    product = get_product_by_name("oat")
    assert product["brands"] == "Oatly"


@patch("app.requests.get")
def test_get_product_by_name_not_found(mock.get):
    mock_get.return_value.json.return_value = {"products": []}
    assert get_product_by_name("zzz") is None


@patch("app.requests.get")
def test_barcode_route_not_found(mock_get, client):
    mock_get.return_value.json.return_value = {
        "status": 1,
        "product": {"product_name": "Nutella", "brands": "Ferrero", "ingredients_text": "Sugar"}
    }
    response = client.get("/search/barcode/3017620422003")
    assert response.status_code == 200
    assert response.get_json()["prooduct_name"] == "Nutella"


@patch("app.requests.get")
def test_barcode_route_not_found(mock_get, client):
    mock_get.return_value.json.return_value = {"status": 0}
    response = client.get("/search/barcode/000")
    assert response.status_code == 404


@patch("app.requests.get")
def test_barcode_route_api_down(mock_get, client):
    mock_get.side_effect = requests.exceptions.ConnectionError
    response = client.get("/search/barcode/123")
    assert response.status_code == 503


@patch("app.requests.get")
def test_name_route_found(mock_get, client):
    mock_get.return_value.json.return_value = {
        "products": [{"product_name": "Oat Milk", "brands": "Oatly", "ingredients_text": "Oats", "code": "1"}]
    }
    response = client.get("/search/name/oat")
    assert response.status_code == 200
    assert response.get_json()["product_name"] == "Oat Milk"


@patch("app.requests.get")
def test_name_route_api_down(mock_get, client):
    mock_get.side_effect = requests.exceptions.Timeout
    response = client.get("/search/name/oat")
    assert response.status_code == 503







