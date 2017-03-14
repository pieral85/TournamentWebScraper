from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, Numeric, String
from contextlib import contextmanager

from config import DB_FILE_PATH


engine = create_engine('sqlite:///' + DB_FILE_PATH, echo=True)
_Session = sessionmaker(bind=engine)
session = _Session(autoflush=True)
Base = declarative_base(bind=engine)

# @contextmanager
# def db_session():
#     engine = create_engine('sqlite:///' + DB_FILE_PATH, echo=True)
#     Session = sessionmaker(bind=engine)
#     # global session, Base
#     session = Session(autoflush=True)
#     # Base = declarative_base()
#     # Base.metadata.create_all(engine)
#     # return Base
#     yield session
#     session.commit()
#     session.close()
