from sqlalchemy_pos_declarative import Base, PositionEntity
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def initSession(lite_db_name):
    engine = create_engine('sqlite:///' + lite_db_name)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    DBSession = sessionmaker()
    DBSession.bind = engine
    session = DBSession()
    return session

# if not ('lite_db_name' in vars()):
#     lite_db_name = 'positionentity.db'

# print lite_db_name
# session = initSession(lite_db_name)
#engine = create_engine('sqlite:///:memory:')
#engine = create_engine('sqlite:////data_bt/s450022/orderentity.db')
#engine = create_engine('sqlite:///' + lite_db_name)
#engine = create_engine('sqlite:////data_bt/s450022/orderentity_20151105_0.db')
#Base.metadata.bind = engine
#Base.metadata.create_all(engine)
#DBSession = sessionmaker()
#DBSession.bind = engine
#session = DBSession()

