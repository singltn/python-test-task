from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from src.models.base import Base


class Wallet(Base):
    __tablename__ = "wallet"

    id = Column(Integer, primary_key=True)
    uuid = Column(String, nullable=True, unique=True)
    balance = Column(Integer, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
