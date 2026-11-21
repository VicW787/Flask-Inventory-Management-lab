import requests

Base_url = "http://127.0.0.1:5555"

def show_item(item):
    """Print one inventory item."""
    print("-" * 30)
    print("ID:", item["id"])
    print("Name:", item["product_name"])
    print("Brand:", item["brands"])
    print("Ingredients:", item["ingredients_text"])
    print("Barcode:", item["barcode"])
    print("Price:", item["price"])
    print("Stock:", item["stock"])

def show_product(product):
    """Print a product found on OpenFoodFacts."""
    print("-" * 30)
    print("Name:", product["product_name"])
    print("Brand:", product["brands"])
    print("Ingredients:", product["ingredients_text"])
    print("Barcode:", product["barcode"])

def ask_id(message):
    """Ask for an ID. Returns a number, or None if the input is not a number."""
    try:
        return int(input(message))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return None

def view_all():
    response = requests.get(f"{Base_url}/inventory")
    items = response.json()


    if len(items) == 0:
        print("The inventory is empty.")
    for item in items:
        show_item(item)


def view_one():
    item_id = ask_id("Enter the item ID: ")
    if item_id is None:
        return


    response = requests.get(f"{Base_url}/inventory/{item_id}")
    if response.status_code == 200:
        show_item(response.json())
    else:
        print("Error:", response.json()["error"])


def add_item():
    name = input("Product name: ")
    brand = input("Brand: ")
    ingredients = input("Ingredients: ")
    barcode = input("Barcode: ")
    try:
        price = float(input("Price: "))
        stock = int(input("Stock: "))
    except ValueError:
        print("Invalid number. Item not added.")
        return

    new_item = {
        "product_name": name,
        "brands": brand,
        "ingredients_text": ingredients,
        "barcode": barcode,
        "price": price,
        "stock": stock,
    }

    response = requests.post(f"{Base_url}/inventory", json=new_item)
    if response.status_code == 201:
        print("Item added!")
        show_item(response.json())
    else:
        print ("Error:", response.json()["error"])


def update_item():
    item_id = ask_id("Enter the ID of the item to update: ")
    if item_id is None:
        return

    new_price = input("New price (press Enter to skip): ")
    new_stock = input("New stock (press Enter to skip): ")

    changes = {}
    try: 
        if new_price != "":
            changes["price"] = float(new_price)
        if new_stock != "":
            changes["stock"] = int(new_stock)
    except ValueError:
        print("Invalid number. Nothing was updated.")
        return

    if changes == {}:
        print("Invalid number. Nothing was updated.")
        return

    response =  requests.patch(f"{Base_url}/inventory/{item_id}", json=changes)
    if response.status_code == 200:
        print("Item updated!")
        show_item(response.json())
    else:
        print("Error:", response.json()["error"])


def delete_item():
    item_id = ask_id("Enter the ID of the item to delete: ")
    if item_id is None:
        return

    response = requests.delete(f"{Base_url}/inventory/{item_id}")
    if response.status_code == 200:
        print("Item deleted.")
    else:
        print("Error:", response.json()["error"])



def find_on_api():
    print("1. Search by barcode")
    print("2. Search by name")
    choice = input("Choose 1 or 2: ")

    if choice == "1":
        barcode == input("Enter the barcode: ")
        if barcode == "":
            print("The barcode cannot be empty.")
            return
        response = requests.get(f"{Base_url}/search/barcode/{barcode}")
    elif choice == "2":
        name = input("Enter the product name: ")
        if name == "":
            print("The name cannot be empty.")
            return
        response = requests.get(f"{Base_url}/search/name/{name}")
    else:
        print("Invalid choice.")
        return

    if response.status_code != 200:
        print("Error:", response.json()["error"])
        return

    product = response.json()
    show_product(product)

    answer = input("Add this product to the inventory? (y/n): ")
    if answer == "y":
        try:
            product["price"] = float(input("Price: "))
            product["stock"] = int(input("Stock: "))
        except ValueError:
            print("Invalid number. Product not added.")
            return

        response = requests.post(f"{Base_url}/inventory", json=product)
        if response.status_code == 201:
            print("Product added to the inventory!")
        else:
            print("Error:", response.json()["error"])


def main():
    while True:
        print("\n=== Inventory Manager ===")
        print("1. View all items")
        print("2. View one item")
        print("3. Add a new item")
        print("4. Update price / stock")
        print("5. Delete an item")
        print("6. Find a product on OpenFoodFacts")
        print("7. Quit")
        choice = input("Choose an option: ")


        try:
            if choice == "1":
                view_all()
            elif choice == "2":
                view_one()
            elif choice == "3":
                add_item()
            elif choice == "4":
                update_item()
            elif choice == "5":
                delete_item
            elif choice == "6":
                find_on_api()
            elif choice == "7":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please choose 1-7.")
        except requests.exceptions.RequestException:
            print("Could not reach the server. is app.py running?")


if __name__ == "__main__"
    main()


