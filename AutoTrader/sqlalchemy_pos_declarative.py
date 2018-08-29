from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import create_engine
 
Base = declarative_base()

class PositionEntity(Base):
    __tablename__ = 'positionentity'
    # id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    autotrader_id = Column(String, primary_key=True, nullable=False)
    shortcd = Column(String, primary_key=True, nullable=False)
    datetime = Column(DateTime)
    buysell = Column(String)
    avgexecprice = Column(Float)
    holdqty = Column(Integer)
    # liveqty = Column(Integer)

# engine = create_engine('sqlite:///entityorder_20151007.db')
# engine = create_engine('sqlite:////home/s450022/python/comm/orderentity_20151012.db')
# engine = create_engine('sqlite:///:memory:')
# Base.metadata.create_all(engine)

