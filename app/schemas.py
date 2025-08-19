from pydantic import BaseModel, EmailStr, ConfigDict, Field



class CreateProduct(BaseModel):
    name: str
    description: str
    price: int
    image_url: str
    stock: int
    category: int


class CreateCategory(BaseModel):
    name: str
    parent_id: int | None = None



class CreateUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str


class ResponseUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class CreateReview(BaseModel):
    product_slug: str
    grade: int| None = Field(None, ge=1, le=10)
    comment: str| None = None


class ReviewOut(BaseModel):
    id: int
    product_id: int
    grade: int | None
    comment: str | None

    model_config = ConfigDict(from_attributes=True)


class ProductReviewsOut(BaseModel):
    product_id: int
    product_name: str
    reviews: list[ReviewOut]