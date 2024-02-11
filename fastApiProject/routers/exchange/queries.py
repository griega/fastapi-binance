from models.models import Pairs
from sqlalchemy import orm


def get_all_pairs(symbol: str, db: orm.Session):
    return db.query(Pairs).filter(Pairs.symbol.like(f"%{symbol}%")).all()