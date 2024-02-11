from core.database import Base
import sqlalchemy as sa


class Pairs(Base):
    __tablename__ = "pairs"
    symbol = sa.Column(
        sa.String(length=20),
        primary_key=True,
        unique=True,
    )
    price = sa.Column(
        sa.Numeric(precision=20, scale=10)
    )