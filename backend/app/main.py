from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal

app = FastAPI(title="AetherChain API")

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

# ... (create_supplier_endpoint is now simpler)
@app.post("/suppliers/", response_model=schemas.Supplier)
def create_supplier_endpoint(supplier: schemas.SupplierCreate, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier_by_name(db, name=supplier.name)
    if db_supplier:
        raise HTTPException(status_code=400, detail="Supplier with this name already exists")
    return crud.create_supplier(db=db, supplier=supplier)

@app.post("/suppliers/{supplier_id}/products/", response_model=schemas.Product)
def create_product_for_supplier_endpoint(supplier_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    supplier = db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return crud.create_product_for_supplier(db=db, product=product, supplier_id=supplier_id, supplier_name=supplier.name)

# ... (read_suppliers, read_products, warehouse endpoints are unchanged)
@app.get("/suppliers/", response_model=list[schemas.Supplier])
def read_suppliers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_suppliers(db, skip=skip, limit=limit)
@app.get("/products/", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_products(db, skip=skip, limit=limit)
@app.post("/warehouses/", response_model=schemas.Warehouse)
def create_warehouse_endpoint(warehouse: schemas.WarehouseCreate, db: Session = Depends(get_db)):
    db_warehouse = crud.get_warehouse_by_location(db, location=warehouse.location)
    if db_warehouse:
        raise HTTPException(status_code=400, detail="Warehouse at this location already exists")
    return crud.create_warehouse(db=db, warehouse=warehouse)
@app.get("/warehouses/", response_model=list[schemas.Warehouse])
def read_warehouses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_warehouses(db, skip=skip, limit=limit)

# --- ADD NEW ENDPOINTS ---
@app.post("/inventory/", response_model=schemas.Inventory)
def create_inventory_item(item: schemas.InventoryCreate, db: Session = Depends(get_db)):
    return crud.add_inventory_item(db=db, item=item)

@app.get("/inventory/alerts/")
def get_inventory_alerts(db: Session = Depends(get_db)):
    alerts = crud.get_low_stock_alerts(db=db)
    return [{"product_name": a[0], "reorder_level": a[1], "total_quantity": a[2]} for a in alerts]

@app.get("/graph/product-path/{product_name}")
def get_product_path(product_name: str):
    with crud.driver.session() as session:
        result = session.execute_read(crud.find_product_supply_path, product_name)
        if not result:
            raise HTTPException(status_code=404, detail="Product path not found in graph.")
        return dict(result)
    
@app.get("/inventory/", response_model=list[schemas.Inventory])
def read_inventory(skip: int = 0, limit: int = 500, db: Session = Depends(get_db)):
    return crud.get_inventory(db, skip=skip, limit=limit)