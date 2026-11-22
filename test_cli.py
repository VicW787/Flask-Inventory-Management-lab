import requests
from unittest.mock import patch
import cli

SAMPLE_ITEM = {
    "id": 1,
    "product_name": "Almond Milk",
    "brands": "Silk",
    "ingredients_text": "Water, almonds",
    "barcode": "111",
    "price": 3.99,
    "stock": 10,
}

@patch("cli.requests.get")
def test_view_all(mock_get, capsys):
    mock_get.return_value.json.return_value = [SAMPLE_ITEM]
    cli.view_all()
    assert "Almond Milk" in capsys.readouterr().out

@patch("cli.requests.get")
def test_view_all_empty(mock_get, capsys):
    mock_get.return_value.json.return_value = []
    cli.view_all()
    assert "empty" in capsys.readouterr().out



@patch("builtins.input", side_effect=["1"])
@patch("cli.requests.get")
def test_view_one(mock_get, mock_input, capsys):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = SAMPLE_ITEM
    cli.view_one()
    assert "Almond Milk" in capsys.readouterr().out



@patch("builtins.input", side_effect=["99"])
@patch("cli.requests.get")
def test_view_one_not_found(mock_get, mock_input, capsys):
    mock_get.return_value.status_code = 404
    mock_get.return_value.json.return_value = {"error": "Item not found"}
    cli.view_one()
    assert "Item not found" in capsys.readouterr().out



@patch("builtins.input", side_effect=["abc"])
@patch("cli.requests.get")
def test_view_one_invalid_id(mock_get, mock_input, capsys):
    cli.view_one()
    assert "Invalid ID" in capsys.readouterr().out
    assert not mock_get.called


@patch("builtins.input", side_effect=["Cereal", "Kellogg", "Corn", "123", "2.5", "10"])
@patch("cli.requests.post")
def test_add_item(mock_post, mock_input, capsys):
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = SAMPLE_ITEM
    cli.add_item()


    sent_data = mock_post.call_args.kwargs["json"]
    assert sent_data["product_name"] == "Cereal"
    assert sent_data["price"] == 2.5
    assert sent_data["stock"] == 10
    assert "item added" in capsys.readouterr().out




@patch("builtins.input", side_effect=["Cereal", "Kellogg", "Corn", "123", "abc", "10"])
@patch("cli.requests.post")
def test_add_item_invalid_price(mock_post, mock_input, capsys):
    cli.add_item()
    assert "Invalid number" in capsys.readouterr().out
    assert not mock_post.called


@patch("builtins.input", side_effect=["1", "4.5", ""])
@patch("cli.requests.patch")
def test_update_item(mock_patch, mock_input, capsys):
    mock_patch.return_value.status_code = 200
    mock_patch.return_value.json.return_value = SAMPLE_ITEM
    cli.update_item()

    assert mock_patch.call_args.kwargs["json"] == {"price": 4.5}
    assert "Item updated" in capsys.readouterr().out


@patch("builtins.input", side_effect=["1", "", ""])
@patch("cli.requests.patch")
def test_update_item_nothing_to_change(mock_patch, mock_input, capsys):
    cli.update_item()
    assert not mock_patch.called
    assert "Nothing to update" in capsys.readouterr().out



@patch("builtins.input", side_effect=["1"])
@patch("cli.requests.delete")
def test_delete_item(mock_delete, mock_input, capsys):
    mock_delete.return_value.status_code = 200
    cli.delete_item()
    assert mock_delete.called
    assert "Item deleted" in capsys.readouterr().out


@patch("builtins.input", side_effect=["1", "3017620422003", "y", "6.5", "12"])
@patch("cli.requests.post")
@patch("cli.requests.get")
def test_find_by_barcode_and_add(mock_get, mock_post, mock_input, capsys):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "product_name": "Nutella",
        "brands": "Ferrero",
        "ingredients_text": "Sugar",
        "barcode": "3017620422003",
    }
    mock_post.return_value.status_code = 201
    cli.find_on_api()


    sent_data =  mock_post.call_args.kwargs["json"]
    assert sent_data["product_name"] == "Nutella"
    assert sent_data["price"] == 6.5
    assert sent_data["stock"] == 12
    assert"added to the inventory" in capsys.readouterr().out


@patch("builtins.input", side_effect=["2", "oat", "n"])
@patch("cli.requests.post")
@patch("cli.requests.get")
def test_find_by_name_and_decline(mock_get, mock_post, mock_input, capsys):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "product_name": "Oat Milk",
        "brands": "Oatly",
        "ingredients_text": "Oats",
        "barcode": "1",
    }
    cli.find_on_api()
    assert "Oat Milk" in capsys.readouterr().out
    assert not mock_post.called


@patch("builtins.input", side_effect=["1", "000"])
@patch("cli.requests.get")
def test_find_not_found(mock_get, mock_input, capsys):
    mock_get.return_value.status_code = 404
    mock_get.return_value.json.return_value = {"error": "Product not found"}
    cli.find_on_api()
    assert "Product not found" in capsys.readouterr().out


@patch("builtins.input", side_effect=["1", "7"])
@patch("cli.requests.get")
def test_server_down(mock_get, mock_input, capsys):
    mock_get.side_effect = requests.exceptions.ConnectionError
    cli.main()
    assert "Could not reach the server." in capsys.readouterr().out