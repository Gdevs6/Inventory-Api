from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas import UserLogin
import utils
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    return user_id



router =  APIRouter(tags=["Authentication"])

@router.post("/login",status_code =status.HTTP_202_ACCEPTED )
def login(user_credentials: UserLogin, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if user is None:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials")
    if not utils.verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials")

    return {"access_token": create_access_token(data={"user_id": user.id}), "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    user_id = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise credentials_exception

    return user
