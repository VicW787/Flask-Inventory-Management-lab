# Flask-Inventory-Management-lab
An inventory tool for a retail company:

(a) A FlaskRESTAPI with full CRUD(Create,Read,Update,Delete). 

(b) OpenFoodFacts lookups by barcode or product name. 

(c) A CLI to use the API from the terminal. 

(d) Tests written with pytest and unittest.mock. 
 
The inventory is stored in a Python list in *app.py*, so it resets every time the server restarts.

# File

app.py
cli.py
test_app.py
test_cli.py
requirements.txt

# Installation
git clone https://github.com/VicW787/Flask-Inventory-Management-lab.git
cd Flask-Inventory-Management-lab
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Running the App
Use two terminals(activate *.venv* in both)
Terminal 1, start the API(runs at http://127.0.0.1:5555):

` python3 app.py `

Terminal 2, start the CLI:

`python3 cli.py`

## API Endpoints

|   Method      |   Route      |    What it Does       |
| :-------------| :------------| :---------------------|
|   GET         | /inventory   | Get all items         |
|   GET         |/inventory/< id >| Get one item       |
| POST          | /inventory   | Add a new item        |
 PATCH          | /inventory/< id> | Update an item    |
 | DELETE       | /inventory/< id> | Delete an item    |
| GET           | /search/barcode/< barcode> | Find a product on OpenFoodFacts |
| GET           | /search/name/< name> | Find the first matching product by name |



Errors come back as JSON, for example `{"error": "item not found"}`, with status 400, 404 or 503 (OpenFoodFacts could not be reached).

## CLI Usage
Run `python3 cli.py` and type a number from the menu:
1. View all items
2. View one item
3. Add a new item
4. Update price / stock
5. Delete an item
6. Find a product on OpenFoodFacts
7. Quit

option 2, 4 and 5 ask for an item ID.
option 4: press Enter to skip the price or the stock.
option 6: search by barcode or name, then type `y` to add the product to the inventory (you enter the price and stock).
If you type something invalid or the server is not running, the CLI prints a message instead of crashing.

## Running the Tests

`pytest`

The tests do not need the server or the internet. `unittest.mock.patch` fakes the `requests` calls and the user's typing.




