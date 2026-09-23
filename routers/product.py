from fastapi import APIRouter,Depends,HTTPException,status,Response
from sqlalchemy.orm import Session
from schemas import ProductCreate,ProductResponse
import models
from database import get_db
from routers.auth import get_current_user

router = APIRouter()#prefix="/products",tags=["Products"])

@router .get("/")
def root():
    return {"message": "Inventory Management API"}

@router.get("/products", response_model=list[ProductResponse])
def get_products(db:Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@router.get("/products/{id}", response_model =ProductResponse)
def get_product(id: int,db:Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id==id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Product with id {id} does not exist")
    
    return product

@router.post("/products", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
def create_product(product: ProductCreate,db:Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    #new_product = models.Product(**product.dict()).
    new_product = models.Product(name= product.name,description= product.description,price= product.price,stock= product.stock)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.delete("/products/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int,db:Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if product.first() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Product with id {id} does not exist")
    product.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/products/{id}',response_model=ProductResponse)
def update_product(id: int,products: ProductCreate,db:Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if product.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Product with id {id} does not exist")
    product.update(products.model_dump(),synchronize_session=False)
    db.commit()
    return product.first()
