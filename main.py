import json

class Inventory:
    def __init__(self):
        self.database_path = "database/products.json"
        
    def get_raw_inventory(self) -> dict[str, dict[str, str]]:
        """
        Function to get the inventory from the database.

        The returned format will be:

    ```json

    {

        "Product name": {

            "Description": "A brief description of the product.",

            "Comapny": "The name of the company that manufactures the product.",

            "Price": "0.0",

            "Stock": "0"

        }

    }
    ```

        """

        with open(self.database_path, "r") as file:
            inventory = file.read()

        return json.loads(inventory)

    def get_all_products_names(self) -> list[str]:
        """
        Function to get all product names from the inventory.

        Returns a list of product names.
        """

        inventory = self.get_raw_inventory()
        return list(inventory.keys())

    def get_price_of_product(self, product_name: str) -> float:
        """
        Function to get the price of a product.

        Returns the price of the product if it exists, otherwise returns None.
        """

        inventory = self.get_raw_inventory()
        if not product_name in inventory:
            return "Product not found."
        
        try:
            price = float(inventory[product_name]["Price"])
        except ValueError:
            return "Invalid price value. Please check the product data."
        
        return price
        
    def get_stock_of_product(self, product_name: str) -> int | str:
        """
        Function to get the stock of a product.

        Returns the stock of the product if it exists, otherwise returns None.
        """

        inventory = self.get_raw_inventory()
        if not product_name in inventory:
            return "Product not found."
        
        try:
            stock =  int(inventory[product_name]["Stock"])
        except ValueError:
            return "Invalid stock value. Please check the product data."
        
        if stock == 0 or stock < 0:
            return "Product is out of stock."
        
        return stock
    
    def update_raw_inventory(self, new_inventory: dict[str, dict[str, str]]) -> None:
        """
        Function to update the inventory with a new inventory.

        The new inventory should be in the same format as the one returned by get_raw_inventory.
        """

        with open(self.database_path, "w") as file:
            file.write(json.dumps(new_inventory), indent=4)

    def add_product(self, product_name: str, description: str, company: str, price: float, stock: str) -> None:
        """
        The product will be added with the given name, description, company, price, and stock.
        If the product already exists, it will increment the stock and notify the user about it.
        """

        inventory = self.get_raw_inventory()
        
        if product_name in inventory:
            inventory[product_name]["Description"] = description
            inventory[product_name]["Company"] = company
            inventory[product_name]["Price"] = str(price)
            inventory[product_name]["Stock"] = int(inventory[product_name]["Stock"]) + int(stock)
            print(f"Product '{product_name}' already exists. Stock has been updated.")
            print(f"New stock for '{product_name}': {inventory[product_name]['Stock']}")
        else:
            inventory[product_name] = {
                "Description": description,
                "Company": company,
                "Price": str(price),
                "Stock": str(stock)
            }
        
        self.update_raw_inventory(inventory)

    def sell_product(self, product_name: str, quantity: int) -> str:
        """
        Function to sell a product.

        If the product exists and has enough stock, it will decrement the stock and return a success message.
        If the product does not exist or has insufficient stock, it will return an error message.
        """

        inventory = self.get_raw_inventory()
        
        if product_name not in inventory:
            return "Product not found."
        
        current_stock = int(inventory[product_name]["Stock"])
        
        if current_stock < quantity:
            return "Insufficient stock available."
        
        inventory[product_name]["Stock"] = str(current_stock - quantity)
        self.update_raw_inventory(inventory)
        
        return f"Sold {quantity} of '{product_name}'. New stock: {inventory[product_name]['Stock']}"
    
class UserInteractionViaTerminal:
    def __init__(self):
        self.inventory = Inventory()

    def run(self):
        print("\nWelcome to the Inventory Management System")
        print("This app is made by Om Goyal.")
        while True:
            print("\n")
            print("1. View all products")
            print("2. Add a product")
            print("3. Sell a product")
            print("4. View stock of all the products")
            print("Type 'q' to quit")
            
            choice = input("Enter your choice: ")
            print("\n")

            if choice == "1":
                products = self.inventory.get_all_products_names()
                print("Available products:", products)

            elif choice == "2":
                name = input("Enter product name: ")
                description = input("Enter product description: ")
                company = input("Enter company name: ")
                price = float(input("Enter product price: "))
                stock = input("Enter stock quantity: ")
                self.inventory.add_product(name, description, company, price, stock)
                print(f"Product '{name}' added successfully.")

            elif choice == "3":
                name = input("Enter product name to sell: ")
                quantity = int(input("Enter quantity to sell: "))
                result = self.inventory.sell_product(name, quantity)
                print(result)

            elif choice == "4":
                print("Stock of all products:")
                getStockOfInputProduct(self.inventory)

            elif choice == "q":
                print("Exiting the system.")
                break

            else:
                print("Invalid choice. Please try again.")

def getStockOfInputProduct(inventory: Inventory) -> int:
    all_products = inventory.get_all_products_names()

    for product in all_products:
        print(f"- {product}: {inventory.get_stock_of_product(product)} in stock")

def main():
    user_interaction = UserInteractionViaTerminal()
    user_interaction.run()

if __name__ == "__main__":
    main()