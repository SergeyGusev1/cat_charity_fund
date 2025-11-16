from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer


class BaseModelMixin:
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    full_amount = Column(Integer)
