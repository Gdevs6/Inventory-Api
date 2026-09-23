from fastapi import FastAPI, status, HTTPException, Response, Depends
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from schemas import ProductCreate, ProductResponse, CategoryCreate, CategoryResponse
from routers import product, category, users, auth

# this creates all tables in the database automatically
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(product.router)
app.include_router(category.router)
app.include_router(users.router)
app.include_router(auth.router)