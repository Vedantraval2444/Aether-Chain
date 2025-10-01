import requests
import random
from faker import Faker

API_URL = "http://localhost:8000"
fake = Faker()

def create_suppliers(count=50):
    print("Creating suppliers...")
    created = []
    for _ in range(count):
        try:
            res = requests.post(f"{API_URL}/suppliers/", json={"name": fake.company(), "country": fake.country()})
            if res.status_code == 200: created.append(res.json())
        except requests.exceptions.RequestException as e: print(f"Error: {e}")
    print("Supplier creation complete.\n")
    return created

def create_warehouses(count=10):
    print("Creating warehouses...")
    created = []
    for _ in range(count):
        try:
            res = requests.post(f"{API_URL}/warehouses/", json={"location": fake.address(), "capacity": random.randint(1000, 10000)})
            if res.status_code == 200: created.append(res.json())
        except requests.exceptions.RequestException as e: print(f"Error: {e}")
    print("Warehouse creation complete.\n")
    return created

def create_products(suppliers, count=200):
    print("Creating products...")
    created = []
    if not suppliers: return []
    for _ in range(count):
        supplier = random.choice(suppliers)
        try:
            res = requests.post(f"{API_URL}/suppliers/{supplier['id']}/products/", json={
                "name": fake.bs().title(),
                "price": round(random.uniform(10.0, 500.0), 2),
                "reorder_level": random.randint(10, 50)
            })
            if res.status_code == 200: created.append(res.json())
        except requests.exceptions.RequestException as e: print(f"Error: {e}")
    print("Product creation complete.\n")
    return created

def create_inventory(products, warehouses):
    print("Creating inventory...")
    if not products or not warehouses: return
    for product in products:
        # Assign product to a random number of warehouses (1 to 3)
        for _ in range(random.randint(1, 3)):
            warehouse = random.choice(warehouses)
            try:
                requests.post(f"{API_URL}/inventory/", json={
                    "product_id": product['id'],
                    "warehouse_id": warehouse['id'],
                    "quantity": random.randint(5, 100) # Start with some stock
                })
            except requests.exceptions.RequestException as e: print(f"Error: {e}")
    print("Inventory creation complete.\n")

if __name__ == "__main__":
    print("--- Starting Full Data Generation ---")
    suppliers = create_suppliers(50)
    warehouses = create_warehouses(10)
    products = create_products(suppliers, 200)
    create_inventory(products, warehouses)
    print("--- Data Generation Finished ---")