from pydantic import BaseModel, EmailStr, ConfigDict


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

