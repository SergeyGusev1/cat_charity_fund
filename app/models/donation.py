from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        Text)

from app.core.db import Base


class Donation(Base):
    __tablename__ = 'donation'

    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)
    full_amount = Column(Integer)
    invested_amount = Column(Integer)
    fully_invested = Column(Boolean)
    create_date = Column(DateTime)
    close_date = Column(DateTime)