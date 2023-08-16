from config.db.manager import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from products.models import Product as ProductModel
from products.schemas import ProductSchema, ProductCreateSchema, ProductUpdateSchema

router = APIRouter()


@router.get("/{pk}", response_model=ProductSchema)
async def get_product(pk: int, db: AsyncSession = Depends(get_db)):
    return await ProductModel.get(db, pk)


@router.get("/", response_model=list[ProductSchema])
async def get_products(db: AsyncSession = Depends(get_db), category_id: int | None = None, price: float | None = None):
    if category_id and price:
        products = ProductModel.get_by_category_and_price(db, category_id, price)
        return await products
    elif category_id:
        products = ProductModel.get_by_category(db, category_id)
        return await products
    elif price:
        products = ProductModel.get_by_price(db, price)
        return await products
    return await ProductModel.get_all(db)


@router.post("/", response_model=ProductSchema)
async def create_product(body: ProductCreateSchema, db: AsyncSession = Depends(get_db)):
    new_product = ProductModel.create(
        db,
        name=body.name,
        is_active=body.is_active,
        discount=body.discount,
        price=body.price,
        category_id=body.category_id,
    )
    return await new_product


@router.patch("/{pk}", response_model=ProductSchema)
async def update_product(pk: int, product_attrs: ProductUpdateSchema, db: AsyncSession = Depends(get_db)):
    return await ProductModel.update(db, pk, product_attrs.model_dump(exclude_unset=True))


@router.delete("/{pk}", response_model=ProductSchema)
async def delete_product(pk: int, db: AsyncSession = Depends(get_db)):
    product = await ProductModel.get(db, pk)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product = await ProductModel.delete(db, pk)
    return product
