from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from . import crud, models, schemas
from .database import get_db

app = FastAPI()


@app.post(
    "/products/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED
)
async def create_product(
    product: schemas.ProductCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.create_product(db, product)


@app.get("/products/", response_model=List[schemas.Product])
async def read_products(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    products = await crud.get_products(db)
    return products[skip : skip + limit]


@app.get("/products/{product_id}", response_model=schemas.Product)
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await crud.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    return product


@app.put("/products/{product_id}", response_model=schemas.Product)
async def update_product(
    product_id: int, product: schemas.ProductUpdate, db: AsyncSession = Depends(get_db)
):
    updated_product = await crud.update_product(db, product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    return updated_product


@app.delete("/products/{product_id}", response_model=schemas.Product)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    deleted_product = await crud.delete_product(db, product_id)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    return deleted_product


@app.post("/orders/", response_model=schemas.Order, status_code=status.HTTP_201_CREATED)
async def create_order(order: schemas.OrderCreate, db: AsyncSession = Depends(get_db)):

    for item in order.items:
        product = await db.get(models.Product, item.product_id)
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400, detail=f"Недостаточно товара: {product.name}"
            )
        product.stock -= item.quantity
        await db.commit()

    return await crud.create_order(db, order)


@app.get("/orders/", response_model=List[schemas.Order])
async def read_orders(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    orders = await crud.get_orders(db)
    return orders[skip : skip + limit]


@app.get("/orders/{order_id}", response_model=schemas.Order)
async def read_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await crud.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order


@app.put("/orders/{order_id}", response_model=schemas.Order)
async def update_order(
    order_id: int, order: schemas.OrderCreate, db: AsyncSession = Depends(get_db)
):
    updated_order = await crud.update_order(db, order_id, order)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return updated_order


@app.delete("/orders/{order_id}", response_model=schemas.Order)
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db)):
    deleted_order = await crud.delete_order(db, order_id)
    if not deleted_order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return deleted_order
