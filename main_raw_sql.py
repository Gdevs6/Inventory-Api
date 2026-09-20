from fastapi import FastAPI,status,HTTPException,Response
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from datetime import datetime
app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="inventory",
            user="postgres",
            password="1Adewale...",
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection successful")
        time.sleep(2)
        break
    except Exception as e:
        print(f"Database connection failed: {e}")

class Products(BaseModel):
    name: str
    description: str| None = None
    price: float
    stock: int = 0
    in_stock: bool = True
    category_id: int| None = None

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str| None = None
    price: float
    stock: int
    in_stock: bool
"""
@app.get('/')
def root():
    return {'message': 'Inventory  Management API'}

@app.get('/products',response_model=list[ProductResponse])
def get_products(search:str =None,in_stock:bool =None):

    if search is not None and in_stock is not None:
        cursor.execute("SELECT * FROM products WHERE name ILIKE %s AND in_stock = %s", (search,in_stock))
        products = cursor.fetchall()
        return products
    elif search is not None:
        cursor.execute("SELECT * FROM products WHERE name ILIKE %s ",(search,))
        products = cursor.fetchall()
        return products
    elif in_stock is not None:
        cursor.execute("SELECT * FROM products WHERE in_stock = %s ",(in_stock,))
        products = cursor.fetchall()
        return products
    else:
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        return products


@app.post('/products', status_code= status.HTTP_201_CREATED,response_model=ProductResponse)
def create_product(product: Products):
    cursor.execute(
        """
            INSERT INTO products (name, description, price, stock, in_stock, category_id)
            VALUES(%s,%s,%s,%s,%s,%s)
            RETURNING * 
        """,
        (product.name,product.description,product.price,product.stock,product.in_stock,product.category_id)
    )
    new_product = cursor.fetchone()
    conn.commit()
    return new_product

@app.get('/products/{id}',response_model=ProductResponse)
def get_product(id: int):
    cursor.execute("SELECT * FROM products  WHERE id = %s ",(str(id),))
    product = cursor.fetchone()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Product with id {id} does not exist")
    
    return product

@app.put('/products/{id}',response_model=ProductResponse)
def update_product(id: int,products: Products):
    cursor.execute("""UPDATE products SET 
        name= %s,
        description=%s,
        price= %s,
        stock= %s
        WHERE id = %s RETURNING *""",(products.name,products.description,str(products.price),str(products.stock),str(id)))
    product = cursor.fetchone()
    conn.commit()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Product with id {id} does not exist")
    
    return product

@app.delete('/products/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int):
    cursor.execute("DELETE FROM products WHERE id = %s RETURNING *",(id,))
    product =cursor.fetchone()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Product with id {id} does not exist")
    
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

class Category(BaseModel):
    name:str

class CategoryResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    
@app.post('/category', response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: Category):
    cursor.execute("INSERT INTO categories (name) VALUES(%s) RETURNING *",(category.name,))
    new_category = cursor.fetchone()
    conn.commit()
    return new_category

@app.get('/category',response_model=list[CategoryResponse])
def get_categories():
    cursor.execute("SELECT * FROM categories")
    total_categories = cursor.fetchall()
    return total_categories

@app.get('/category/{id}',response_model=CategoryResponse)
def get_category(id: int):
    cursor.execute("SELECT * FROM categories WHERE id= %s",(str(id),))
    category = cursor.fetchone()
    if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Category with id {id} does not exist")
    return category

@app.delete("/category/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: int):
    cursor.execute("DELETE FROM categories WHERE id = %s RETURNING *",(str(id),))
    deleted_category = cursor.fetchone()
    conn.commit()
    if deleted_category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Category with id {id} does not exist")
    return  Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get('/category/{id}/products',response_model=list[ProductResponse])
def get_products_by_category(id: int):
    cursor.execute("SELECT * FROM categories WHERE id = %s", (str(id),))
    category = cursor.fetchone()
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {id} does not exist"
        )


    cursor.execute(""" SELECT products.* 
                        FROM products
                        JOIN categories ON products.category_id = categories.id
                        WHERE categories.id = %s""",(str(id),)
                    )
    products = cursor.fetchall()
    return products


"""