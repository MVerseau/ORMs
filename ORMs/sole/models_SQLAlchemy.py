from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, Text, Float, Boolean


class Base(DeclarativeBase):
    pass

class A_Game(Base):
    __tablename__ = 'sole_game'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text)
    cost = Column(Float)
    size = Column(Integer)
    description = Column(Text)
    age_limited = Column(Boolean)
    buyer = Column(Text)



class A_Buyer(Base):
    __tablename__ = 'sole_buyer'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text)
    balance = Column(Float)
    age = Column(Integer)

