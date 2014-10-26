__author__ = 'andrewapperley'

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *


Base = declarative_base()

def createDatabase(environment='mysql+pymysql://root:root@localhost:8889/announcements?charset=utf8&use_unicode=0', debug=True):
    environment = environment
    _debug = debug
    # CreateDatabase
    global db
    db = create_engine(environment, echo=bool(_debug), pool_size=20, max_overflow=0, pool_recycle=499, pool_timeout=20)
    global DBSession
    DBSession = sessionmaker(bind=db)
    Base.metadata.create_all(db)