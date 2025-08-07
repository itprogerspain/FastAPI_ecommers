from fastapi import APIRouter, Depends, status, HTTPException
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from sqlalchemy import insert, select, update
from slugify import slugify

from app.backend.db_depends import get_db
from app.schemas import CreateProduct
from app.models import *
# from app.models.category import Category
# from app.models.products import Product

router = APIRouter(prefix='/products', tags=['products'])




# @router.get('/')
# async def all_products(db: Annotated[Session, Depends(get_db)]):
#     products = db.scalars(select(Product).join(Category).where(Product.is_active == True, Category.is_active == True,
#                                                                Product.stock > 0)).all()
#     if not products:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail='There are no product'
#         )
#     return products


@router.get('/')
async def all_products(db: Annotated[AsyncSession, Depends(get_db)]):
    products = await db.scalars(select(Product).where(Product.is_active == True, Product.stock > 0))
    all_products = products.all()
    if not all_products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no product'
        )
    return all_products





# @router.post('/', status_code=status.HTTP_201_CREATED)
# async def create_product(db: Annotated[Session, Depends(get_db)], create_product: CreateProduct):
#     category = db.scalar(select(Category).where(Category.id == create_product.category))
#     if category is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail='There is no category found'
#         )
#     db.execute(insert(Product).values(name=create_product.name,
#                                       description=create_product.description,
#                                       price=create_product.price,
#                                       image_url=create_product.image_url,
#                                       stock=create_product.stock,
#                                       category_id=create_product.category,
#                                       rating=0.0,
#                                       slug=slugify(create_product.name)))
#     db.commit()
#     return {
#         'status_code': status.HTTP_201_CREATED,
#         'transaction': 'Successful'
#     }



@router.post('/')
async def create_product(db: Annotated[AsyncSession, Depends(get_db)], create_product: CreateProduct):
    category = await db.scalar(select(Category).where(Category.id == create_product.category))
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no category found'
        )
    await db.execute(insert(Product).values(name=create_product.name,
                                      description=create_product.description,
                                      price=create_product.price,
                                      image_url=create_product.image_url,
                                      stock=create_product.stock,
                                      category_id=create_product.category,
                                      rating=0.0,
                                      slug=slugify(create_product.name)))
    await db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }



# @router.get('/{category_slug}')
# async def product_by_category(
#         db: Annotated[Session, Depends(get_db)],
#         category_slug: str):
#     category = db.scalar(select(Category).where(Category.slug == category_slug))
#     if category is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail='Category not found'
#         )
#     subcategories = db.scalars(
#         select(Category).where(Category.parent_id == category.id)).all()
#     categories_and_subcategories = [category.id] + [i.id for i in subcategories]
#     products_category = db.scalars(
#         select(Product).where(Product.category_id.in_(categories_and_subcategories), Product.is_active == True,
#                               Product.stock > 0)).all()
#     return products_category


@router.get('/{category_slug}')
async def product_by_category(db: Annotated[AsyncSession, Depends(get_db)], category_slug: str):
    category = await db.scalar(select(Category).where(Category.slug == category_slug))
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Category not found'
        )
    subcategories = await db.scalars(select(Category).where(Category.parent_id == category.id))
    categories_and_subcategories = [category.id] + [i.id for i in subcategories.all()]
    products_category = await db.scalars(
        select(Product).where(Product.category_id.in_(categories_and_subcategories), Product.is_active == True,
                              Product.stock > 0))
    return products_category.all()



# @router.get('/detail/{product_slug}')
# async def product_detail(
#         db: Annotated[Session, Depends(get_db)],
#         product_slug: str
# ):
#     product = db.scalar(
#         select(Product).where(
#             Product.slug == product_slug,
#             Product.is_active == True,
#             Product.stock > 0)
#     )
#     if not product:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail='There is no product found'
#         )
#     return product


@router.get('/detail/{product_slug}')
async def product_detail(db: Annotated[AsyncSession, Depends(get_db)], product_slug: str):
    product = await db.scalar(
        select(Product).where(Product.slug == product_slug, Product.is_active == True, Product.stock > 0))
    if product is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no product'
        )
    return product




# @router.put('/{product_slug}')
# async def update_product(db: Annotated[Session, Depends(get_db)],
#                          product_slug: str,
#                          update_product_model: CreateProduct):
#     product_update = db.scalar(select(Product).where(Product.slug == product_slug))
#     if product_update is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail='There is no product found'
#         )
#     category = db.scalar(select(Category).where(Category.id == update_product_model.category))
#     if category is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail='There is no category found'
#         )
#     db.execute(update(Product).where(Product.slug == product_slug)
#                .values(name=update_product_model.name,
#                        description=update_product_model.description,
#                        price=update_product_model.price,
#                        image_url=update_product_model.image_url,
#                        stock=update_product_model.stock,
#                        category_id=update_product_model.category,
#                        slug=slugify(update_product_model.name)))
#     db.commit()
#     return {
#         'status_code': status.HTTP_200_OK,
#         'transaction': 'Product update is successful'
#     }


@router.put('/{product_slug}')
async def update_product(db: Annotated[AsyncSession, Depends(get_db)], product_slug: str,
                         update_product_model: CreateProduct):
    product_update = await db.scalar(select(Product).where(Product.slug == product_slug))
    if product_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no product found'
        )
    category = await db.scalar(select(Category).where(Category.id == update_product_model.category))
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no category found'
        )

    product_update.name = update_product_model.name
    product_update.description = update_product_model.description
    product_update.price = update_product_model.price
    product_update.image_url = update_product_model.image_url
    product_update.stock = update_product_model.stock
    product_update.category_id = update_product_model.category
    product_update.slug = slugify(update_product_model.name)

    await db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Product update is successful'
    }




# @router.delete('/{product_slug}')
# async def delete_product(db: Annotated[Session, Depends(get_db)], product_slug: str):
#     product_delete = db.scalar(select(Product).where(
#         Product.slug == product_slug, Product.is_active == True))
#     if product_delete is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail='There is no product found'
#         )
#     db.execute(update(Product).where(Product.slug == product_slug).values(is_active=False))
#     db.commit()
#     return {
#         'status_code': status.HTTP_200_OK,
#         'transaction': 'Product delete is successful'
#     }



@router.delete('/{product_slug}')
async def delete_product(db: Annotated[AsyncSession, Depends(get_db)], product_slug: str):
    product_delete = await db.scalar(select(Product).where(Product.slug == product_slug))
    if product_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no product found'
        )

    product_delete.is_active = False
    await db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Product delete is successful'
    }


