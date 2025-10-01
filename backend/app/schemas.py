from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    price: float
    reorder_level: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    supplier_id: int
    class Config: { "from_attributes": True }

class SupplierBase(BaseModel):
    name: str
    country: str

class SupplierCreate(SupplierBase):
    pass

class Supplier(SupplierBase):
    id: int
    products: list[Product] = []
    class Config: { "from_attributes": True }

class WarehouseBase(BaseModel):
    location: str
    capacity: int

class WarehouseCreate(WarehouseBase):
    pass

class Warehouse(WarehouseBase):
    id: int
    class Config: { "from_attributes": True }

# ADD INVENTORY SCHEMAS
class InventoryBase(BaseModel):
    product_id: int
    warehouse_id: int
    quantity: int

class InventoryCreate(InventoryBase):
    pass

class Inventory(InventoryBase):
    id: int
    class Config: { "from_attributes": True }