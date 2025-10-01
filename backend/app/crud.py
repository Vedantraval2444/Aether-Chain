from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas
from neo4j import GraphDatabase

uri = "bolt://neo4j_db:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "aetherpass"))

def add_supplier_node(tx, name, country):
    tx.run("MERGE (s:Supplier {name: $name}) SET s.country = $country", name=name, country=country)

def add_product_node(tx, name, supplier_name):
    tx.run("""
    MATCH (s:Supplier {name: $supplier_name})
    MERGE (p:Product {name: $name})
    MERGE (s)-[:SUPPLIES]->(p)
    """, name=name, supplier_name=supplier_name)

# NEW Graph Query
def find_product_supply_path(tx, product_name: str):
    result = tx.run("""
        MATCH (s:Supplier)-[:SUPPLIES]->(p:Product {name: $product_name})
        RETURN s.name AS supplier, s.country AS country, p.name AS product
    """, product_name=product_name)
    return result.single()

# --- PostgreSQL Functions ---
def create_supplier(db: Session, supplier: schemas.SupplierCreate):
    db_supplier = models.Supplier(name=supplier.name, country=supplier.country)
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    with driver.session() as session:
        session.execute_write(add_supplier_node, supplier.name, supplier.country)
    return db_supplier

def create_product_for_supplier(db: Session, product: schemas.ProductCreate, supplier_id: int, supplier_name: str):
    db_product = models.Product(**product.model_dump(), supplier_id=supplier_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    with driver.session() as session:
        session.execute_write(add_product_node, product.name, supplier_name)
    return db_product

# ADD Inventory Function
def add_inventory_item(db: Session, item: schemas.InventoryCreate):
    db_item = models.Inventory(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_low_stock_alerts(db: Session):
    total_stock = db.query(
        models.Inventory.product_id,
        func.sum(models.Inventory.quantity).label("total_quantity")
    ).group_by(models.Inventory.product_id).subquery()
    
    alerts = db.query(
        models.Product.name,
        models.Product.reorder_level,
        total_stock.c.total_quantity
    ).join(
        total_stock, models.Product.id == total_stock.c.product_id
    ).filter(
        total_stock.c.total_quantity < models.Product.reorder_level
    ).all()
    return alerts
    
# ... (other get functions are unchanged)
def get_supplier_by_name(db: Session, name: str):
    return db.query(models.Supplier).filter(models.Supplier.name == name).first()
def get_suppliers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Supplier).offset(skip).limit(limit).all()
def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()
def create_warehouse(db: Session, warehouse: schemas.WarehouseCreate):
    db_warehouse = models.Warehouse(**warehouse.model_dump())
    db.add(db_warehouse)
    db.commit()
    db.refresh(db_warehouse)
    return db_warehouse
def get_warehouses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Warehouse).offset(skip).limit(limit).all()
def get_warehouse_by_location(db: Session, location: str):
    return db.query(models.Warehouse).filter(models.Warehouse.location == location).first()
def get_inventory(db: Session, skip: int = 0, limit: int = 500):
    return db.query(models.Inventory).offset(skip).limit(limit).all()