from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from sqlalchemy.exc import NoResultFound
from . import models, schemas


async def get_products(db: AsyncSession):
    result = await db.execute(select(models.Product))
    return result.scalars().all()


async def get_product_by_id(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(models.Product).where(models.Product.id == product_id)
    )
    product = result.scalars().first()
    if not product:
        raise NoResultFound(f"Продукт с ID {product_id} не найден")
    return product


async def create_product(db: AsyncSession, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def update_product(
    db: AsyncSession, product_id: int, product: schemas.ProductUpdate
):
    result = await db.execute(
        select(models.Product).where(models.Product.id == product_id)
    )
    db_product = result.scalars().first()

    if not db_product:
        raise NoResultFound(f"Продукт с ID {product_id} не найден")

    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)

    await db.commit()
    await db.refresh(db_product)
    return db_product


async def delete_product(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(models.Product).where(models.Product.id == product_id)
    )
    db_product = result.scalars().first()

    if not db_product:
        raise NoResultFound(f"Продукт с ID {product_id} не найден")

    await db.delete(db_product)
    await db.commit()
    return db_product


async def get_orders(db: AsyncSession):
    result = await db.execute(select(models.Order))
    return result.scalars().all()


async def get_order_by_id(db: AsyncSession, order_id: int):
    result = await db.execute(select(models.Order).where(models.Order.id == order_id))
    order = result.scalars().first()
    if not order:
        raise NoResultFound(f"Заказ с ID {order_id} не найден")
    return order


async def create_order(db: AsyncSession, order: schemas.OrderCreate):
    db_order = models.Order(status=order.status)
    db.add(db_order)
    await db.commit()

    for item_id in order.items:
        db_item = models.OrderItem(order_id=db_order.id, product_id=item_id)
        db.add(db_item)

    await db.commit()
    await db.refresh(db_order)
    return db_order


async def update_order(db: AsyncSession, order_id: int, order: schemas.OrderCreate):
    result = await db.execute(select(models.Order).where(models.Order.id == order_id))
    db_order = result.scalars().first()

    if not db_order:
        raise NoResultFound(f"Заказ с ID {order_id} не найден")

    db_order.status = order.status
    await db.commit()
    await db.refresh(db_order)
    return db_order


async def delete_order(db: AsyncSession, order_id: int):
    result = await db.execute(select(models.Order).where(models.Order.id == order_id))
    db_order = result.scalars().first()

    if not db_order:
        raise NoResultFound(f"Заказ с ID {order_id} не найден")

    await db.delete(db_order)
    await db.commit()
    return db_order
