class Product:
    def __init__(self, product_id, name, quantity, price):
        self.product_id = product_id
        self.name = name
        self.quantity = quantity
        self.price = price

    def update_quantity(self, new_quantity):
        self.quantity = new_quantity

    def update_price(self, new_price):
        self.price = new_price

    def __str__(self):
        return f"ID: {self.product_id} | {self.name} | Qty: {self.quantity} | Price: ₦{self.price}"


class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        if product.product_id in self.products:
            print("❌ Product with this ID already exists.")
        else:
            self.products[product.product_id] = product
            print("✅ Product added successfully!")

    def view_products(self):
        if not self.products:
            print("📭 Inventory is empty.")
        else:
            print("\n📦 INVENTORY LIST")
            for product in self.products.values():
                print(product)

    def update_product(self, product_id, quantity=None, price=None):
        if product_id in self.products:
            if quantity is not None:
                self.products[product_id].update_quantity(quantity)
            if price is not None:
                self.products[product_id].update_price(price)
            print("🔁 Product updated successfully!")
        else:
            print("❌ Product not found.")

    def delete_product(self, product_id):
        if product_id in self.products:
            del self.products[product_id]
            print("🗑️ Product deleted successfully!")
        else:
            print("❌ Product not found.")

    def search_product(self, keyword):
        results = [p for p in self.products.values() if keyword.lower() in p.name.lower()]

        if results:
            print("\n🔍 SEARCH RESULTS:")
            for product in results:
                print(product)
        else:
            print("❌ No product matched your search.")


# ================= MAIN PROGRAM ================= #
def menu():
    inventory = Inventory()

    while True:
        print("\n====== INVENTORY MANAGEMENT SYSTEM ======")
        print("1. Add Product")
        print("2. View Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Search Product")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            pid = input("Enter Product ID: ")
            name = input("Enter Name: ")
            qty = int(input("Enter Quantity: "))
            price = float(input("Enter Price: "))
            product = Product(pid, name, qty, price)
            inventory.add_product(product)

        elif choice == '2':
            inventory.view_products()

        elif choice == '3':
            pid = input("Enter Product ID to update: ")
            qty = input("New Quantity (leave blank to skip): ")
            price = input("New Price (leave blank to skip): ")
            inventory.update_product(
                pid,
                quantity=int(qty) if qty else None,
                price=float(price) if price else None
            )

        elif choice == '4':
            pid = input("Enter Product ID to delete: ")
            inventory.delete_product(pid)

        elif choice == '5':
            keyword = input("Enter product name to search: ")
            inventory.search_product(keyword)

        elif choice == '6':
            print("🛑 Exiting... Goodbye!")
            break

        else:
            print("❌ Invalid choice. Try again.")

# Run Program
menu()