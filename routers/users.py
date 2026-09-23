from fastapi import APIRouter,Depends,HTTPException,status,Response
from sqlalchemy.orm import Session
from routers.auth import get_current_user
from schemas import UserCreate,UserResponse
import models
from database import get_db
from utils import hash_password

routers = APIRouter(prefix="/users",tags=["Users"])

@routers.post("/",status_code=status.HTTP_201_CREATED,response_model=UserResponse)
def create_user(user: UserCreate,db:Session = Depends(get_db)):
    user_data = user.model_dump()
    user_data["hashed_password"] = hash_password(user_data.pop("password"))
    new_user = models.User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    

@routers.get("/{id}",response_model=UserResponse)
def get_user(id:int,db:Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} does not exist")
    return user