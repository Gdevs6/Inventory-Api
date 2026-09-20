from pydantic import BaseModel,ConfigDict
from datetime import datetime

# write your four schemas here
class CategoryCreate(BaseModel):
    name:str

class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    created_at: datetime


class ProductCreate(BaseModel):
    name: str
    description: str| None = None
    price: float
    stock: int = 0
    in_stock: bool = True
    category_id: int| None = None

class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str| None = None
    price: float
    stock: int
    in_stock: bool
    created_at: datetime
