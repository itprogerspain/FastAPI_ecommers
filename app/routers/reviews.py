from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from sqlalchemy import insert, select, update, func
from slugify import slugify

from app.backend.db_depends import get_db
from app.schemas import *
from app.models import *
from app.routers.auth import get_current_user

router = APIRouter(prefix='/reviews', tags=['reviews'])




@router.get('/')
async def all_reviews(db: Annotated[AsyncSession, Depends(get_db)]):
    stmt = select(Review).join(Product).where(Product.is_active == True, Product.stock > 0)
    result = await db.scalars(stmt)
    all_reviews = result.all()

    if not all_reviews:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no reviews'
        )
    return [
        ReviewOut.model_validate(review, from_attributes=True)
        for review in all_reviews
    ]



@router.get('/{product_slug}')
async def products_reviews(db: Annotated[AsyncSession, Depends(get_db)], product_slug: str):
    product_stmt = select(Product).where(
        Product.slug == product_slug,
        Product.is_active == True,
        Product.stock > 0
    )
    product = await db.scalar(product_stmt)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found'
        )

    reviews_stmt = select(Review).where(
        Review.product_id == product.id,
        Review.is_active == True
    )
    result = await db.scalars(reviews_stmt)
    all_product_reviews = result.all()

    if not all_product_reviews:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no reviews'
        )
    return ProductReviewsOut(
        product_id=product.id,
        product_name=product.name,
        reviews=[
            ReviewOut.model_validate(review, from_attributes=True)
            for review in all_product_reviews
        ]
    )





@router.post('/{product_slug}', )
async def add_reviews(db: Annotated[AsyncSession, Depends(get_db)],
                      product_slug: str,
                      add_reviews: CreateReview,
                      get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user.get('is_customer'):
        product_stmt = select(Product).where(
            Product.slug == product_slug,
            Product.is_active == True,
            Product.stock > 0
        )
        product = await db.scalar(product_stmt)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Product not found'
            )

        review_stmt = select(Review).where(
            Review.user_id == get_user['id'],
            Review.product_id == product.id
        )
        existing_review = await db.scalar(review_stmt)
        if existing_review:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='You have already reviewed this product'
            )

        new_review = Review(
            user_id=get_user['id'],
            product_id=product.id,
            grade=add_reviews.grade,
            comment=add_reviews.comment
        )
        db.add(new_review)
        await db.commit()
        await db.refresh(new_review)

        avg_stmt = select(func.avg(Review.grade)).where(
            Review.product_id == product.id,
            Review.is_active == True
        )
        result = await db.execute(avg_stmt)
        avg_grade = result.scalar()

        product.rating = avg_grade
        await db.commit()
        await db.refresh(product)

        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Review creation was successful',
            'new_review': new_review.id,
            'new_rating': product.rating
        }

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Only customers can leave reviews'
        )




@router.delete('/{review_id}')
async def delete_reviews(
    review_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    get_user: Annotated[dict, Depends(get_current_user)]
):
    if not get_user.get('is_admin'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can delete reviews"
        )

    review_stmt = select(Review).where(
        Review.id == review_id,
        Review.is_active == True
    )
    review = await db.scalar(review_stmt)

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    review.is_active = False
    await db.commit()
    await db.refresh(review)

    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "Review delete is successful",
        "deleted_review": ReviewOut.model_validate(review, from_attributes=True)
    }

