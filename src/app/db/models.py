from sqlalchemy import (
    Column,
    ARRAY,
    BigInteger,
    String,
    DateTime,
    ForeignKey,
    Boolean,
    Float,
    func,
    Date,
)
from app.db.initdb import AsyncBase


class User(AsyncBase):
    """Роли Суперадмин, Руководитель"""

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    chat_id = Column(BigInteger, nullable=False)
    username = Column(String(256))
    price = Column(Float, default=82)
    amount = Column(Float, default=0)
    dimension = Column(Float, default=0)
