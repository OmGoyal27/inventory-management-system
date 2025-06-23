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

            "Stock": "0",

            "Category": "The category of the product; e.g. AC, Battery, TV etc."

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
    
    def get_details_of_product(self, product_name: str) -> dict[str, str] | None:
        """
        Function to get the details of a product.

        Returns a dictionary with the product details if it exists, otherwise returns None.
        """

        inventory = self.get_raw_inventory()
        if not product_name in inventory:
            return None
        
        return inventory[product_name]

    def update_raw_inventory(self, new_inventory: dict[str, dict[str, str]]) -> None:
        """
        Function to update the inventory with a new inventory.

        The new inventory should be in the same format as the one returned by get_raw_inventory.
        """

        with open(self.database_path, "w") as file:
            file.write(json.dumps(new_inventory, indent=4))

    def add_product(self, product_name: str, description: str, company: str, price: float | str, stock: str, category: str) -> None:
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
            inventory[product_name]["Category"] = category
            print(f"Product '{product_name}' already exists. Stock has been updated.")
            print(f"New stock for '{product_name}': {inventory[product_name]['Stock']}")
        else:
            inventory[product_name] = {
                "Description": description,
                "Company": company,
                "Price": str(price),
                "Stock": str(stock),
                "Category": category
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
    
    def get_all_categories(self) -> list[str]:
        """
        Function to get all categories from the inventory.

        Returns a list of unique categories.
        """

        inventory = self.get_raw_inventory()
        categories = set()

        for product in inventory.values():
            categories.add(product["Category"])

        return list(categories)
class UserInteractionViaTerminal:
    def __init__(self):
        self.inventory = Inventory()
        self.options = {
            "1.": "View all products",
            "2.": "Add a product",
            "3.": "Sell a product",
            "4.": "View stock of all the products",
            "5.": "View Price of all the products",
            "6.": "View details of a product",
            "7.": "Increase stock of a product"
        }

    def printOptions(self) -> None:
        """
        Function to print the available options for the user.
        """
        print("Available options:")
        for key, value in self.options.items():
            print(f"{key} {value}")
        print("Type 'q' to quit")

    def run(self):
        print("\nWelcome to the Inventory Management System")
        print("This app is made by Om Goyal.")
        while True:
            print("\n")
            self.printOptions()
            
            choice = input("Enter your choice: ")
            print("\n")

            if choice.lower() == 'q':
                print("Thank you for using the Inventory Management System. Goodbye!\n")
                break

            self.handleUserInput(choice)  

    def handleUserInput(self, choice: str) -> None:
        match choice:
            case "1":
                self.option_view_all_products()

            case "2":
                name = input("Enter product name: ")
                description = input("Enter product description: ")
                company = input("Enter company name: ")
                price = float(input("Enter product price: "))
                stock = input("Enter stock quantity: ")
                formatted_categories = ""
                for category in self.inventory.get_all_categories():
                    formatted_categories += f"- {category}\n"

                print(f"Available categories:\n{formatted_categories}")
                print("Please enter the category of the product from the above list or a new category.")
                category = input("Enter product category: ")
                self.inventory.add_product(name, description, company, price, stock, category)
                print(f"Product '{name}' added successfully.")
                
            case "3":
                self.printAllProducts()
                name = input("Enter product index to sell: ")
                all_products = self.inventory.get_all_products_names()
                if not name.isdigit() or int(name) < 0 or int(name) >= len(all_products):
                    print("Invalid product index. Please try again.")
                    return

                name = all_products[int(name)]
                print(f"Selected product: {name} with stock {self.inventory.get_stock_of_product(name)}")
                quantity = int(input("Enter quantity to sell: "))
                result = self.inventory.sell_product(name, quantity)
                print(result)

            case "4":
                print("Stock of all products:")
                self.getStockOfAllProduct()

            case "5":
                all_products = self.inventory.get_all_products_names()
                print("Price of all products:")
                for product in all_products:
                    price = self.inventory.get_price_of_product(product)
                    print(f"{product}: {price}")

            case "6":
                self.printAllProducts()
                product_index = int(input("Enter the index of the product to view details: "))
                all_products = self.inventory.get_raw_inventory()
                if not 0 <= product_index < len(all_products):
                    print("Invalid index. Please try again.")
                    return

                product_name = all_products[product_index]
                self.viewProductDetails(product_name)

            case "7":
                self.printAllProducts()
                product_index = input("Enter the index of the product to increase stock or type 'new' to add a new product: ")
                if product_index.lower() == 'new':
                    self.handleUserInput("2")
                    return
                
                product_index = int(product_index)
                all_products = self.inventory.get_all_products_names()
                if not 0 <= product_index < len(all_products):
                    print("Invalid index. Please try again.")
                    return
                
                product_name = all_products[product_index]
                current_stock = self.inventory.get_stock_of_product(product_name)
                print(f"Selected product: {product_name} with current stock {current_stock}")
                stock_increase = int(input(f"Enter the amount to increase stock for '{product_name}': "))
                if stock_increase < 0:
                    print("Stock increase cannot be negative. Please try again.")
                    return

                product_details = self.inventory.get_details_of_product(product_name)
                self.inventory.add_product(product_name, 
                                          product_details["Description"],
                                          product_details["Company"],
                                          self.inventory.get_price_of_product(product_name),
                                          stock_increase,
                                          product_details["Category"])

            case _:
                print("Invalid choice. Please try again.")

    def option_view_all_products(self) -> None:
        products = self.inventory.get_all_products_names()
        print("Available products:")
        for product in products:
            stock = self.inventory.get_stock_of_product(product)
            print(f"- {product}: {stock} in stock")

    def viewProductDetails(self, product_name: str) -> None:
        """
        Function to view the details of a specific product.
        """

        product_details = self.inventory.get_details_of_product(product_name)

        if not product_details:
            print(f"Product '{product_name}' not found in the inventory.")
            return

        print(f"Details of '{product_name}':\n")
        print(f"Description: {product_details['Description']}")
        print(f"Company: {product_details['Company']}")
        print(f"Price: {product_details['Price']}")
        print(f"Stock: {product_details['Stock']}")
        print(f"Category: {product_details['Category']}")

    def printAllProducts(self) -> None:
        all_products = self.inventory.get_all_products_names()

        for index, product in enumerate(all_products):
            print(f"{index}: {product}")

    def getStockOfAllProduct(self) -> int:
        all_products = self.inventory.get_all_products_names()

        for product in all_products:
            print(f"- {product}: {self.inventory.get_stock_of_product(product)} in stock")

def main():
    user_interaction = UserInteractionViaTerminal()
    user_interaction.run()

if __name__ == "__main__":
    main()