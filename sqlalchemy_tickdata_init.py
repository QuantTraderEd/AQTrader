from sqlalchemy_tickdata_declarative import Base, TickData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


def initSession(lite_db_name):
    if lite_db_name == 'memory':
        engine = create_engine('sqlite://',
                               connect_args={'check_same_thread': False},
                               poolclass=StaticPool)
    else:
        engine = create_engine('sqlite:///' + lite_db_name)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    session = make_session(engine)
    return session, engine


def make_session(engine):
    DBSession = sessionmaker()
    DBSession.bind = engine
    session = DBSession()
    return session
