from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


class ProductCreate(BaseModel):
    name: str
    price: int


class Product(BaseModel):
    id: int
    name: str
    price: int


products: list[Product] = []

next_product_id = 1


@app.get("/")
def root():
    return {"message": "Hello, online store!"}


@app.get("/health")
def get_health():
    return {"status": "ok"}


@app.get("/about")
def about():
    return {"name": "Online Store API", "version": "1.0.0"}


@app.get("/products")
def get_all_products():
    return products


@app.post("/products")
def create_product(product: ProductCreate):
    global next_product_id

    current_id = next_product_id

    full_product = Product(id=current_id, **product.model_dump())
    products.append(full_product)

    next_product_id += 1

    return full_product


@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product.id == product_id:
            return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
    )

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for i, product in enumerate(products):
        if product.id == product_id:
            deleted_product = products.pop(i)
            return deleted_product
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Product not found"
    )