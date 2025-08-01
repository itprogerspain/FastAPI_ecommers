# debug_sql.py
from sqlalchemy.schema import CreateTable
from app.models.category import Category
from app.models.products import Product

print(CreateTable(Category.__table__))
print(CreateTable(Product.__table__))



# python debug_sql.py