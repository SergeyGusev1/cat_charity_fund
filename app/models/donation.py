from datetime import datetime
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        Text)

from app.core.db import Base


class Donation(Base):
    __tablename__ = 'donation'

    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, nullable=False)
    close_date = Column(DateTime, nullable=True)