from fastapi import APIRouter,Depends,HTTPException,status,Response
from sqlalchemy.orm import Session
from routers.auth import get_current_user
from schemas import CategoryCreate,CategoryResponse
import models
from database import get_db

router = APIRouter()    


@router.post("/category",response_model=CategoryResponse,status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate,db:Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    new_category = models.Category(**category.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get("/category",response_model= list[CategoryResponse])
def get_categories(db:Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return categories

@router.get("/category/{id}",response_model=CategoryResponse)
def get_category(id: int,db:Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == id).first()
    if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Category with id {id} does not exist")
    return category

@router.delete("/category/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: int,db:Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    category = db.query(models.Category).filter(models.Category.id == id)
    if category.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Category with id {id} does not exist")
    category.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
        