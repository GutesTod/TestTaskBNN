from .base_model import OrmBase
from sqlalchemy import Column, Integer, String

class SumResult(OrmBase):
    __tablename__ = "sum_results"

    id = Column(Integer, primary_key=True, )
    session_id = Column(String)
    sum = Column(Integer)