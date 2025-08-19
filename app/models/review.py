from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, UniqueConstraint, DateTime, func
from sqlalchemy.orm import relationship

from app.backend.db import Base


class Review(Base):
    __tablename__ = 'reviews'
    __table_args__ = (UniqueConstraint('user_id', 'product_id', name='uq_user_product'),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    grade = Column(Integer)
    comment = Column(String)
    comment_date = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)


    user = relationship('User', back_populates='reviews')
    product = relationship("Product", back_populates="reviews")