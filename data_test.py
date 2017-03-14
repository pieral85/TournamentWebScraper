# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, Session
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, Numeric, String
#
# from config import DB_FILE_PATH
#
# # engine = create_engine('mysql://{0}:{1}@{2}:{3}'.format('admin', 'default', '127.0.0.1', ))
# engine = create_engine('sqlite:///' + DB_FILE_PATH)
# # engine = create_engine('sqlite:///:memory:', echo=False)
# Session = sessionmaker(bind=engine)
# session = Session()
# Base = declarative_base()
from db import db_session, Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Cookie(Base):
    __tablename__ = 'cookies'

    cookie_id = Column(Integer, primary_key=True)
    cookie_name = Column(String(50), index=True)
    cookie_recipe_url = Column(String(255))
    cookie_sku = Column(String(55))
    quantity = Column(Integer())
    unit_cost = Column(Numeric(12, 2))

    def __init__(self, cookie_name, cookie_recipe_url, cookie_sku):
        self.cookie_name = cookie_name
        self.cookie_recipe_url = cookie_recipe_url
        self.cookie_sku = cookie_sku

    def __str__(self):
        return '{0} (#{1})'.format(self.cookie_name, self.cookie_id)

    def __repr__(self):
        return 'toto'


if __name__ == '__main__':
    # Creates all tables:
    # Base.metadata.create_all(engine)
    # Inserts one row:
    # session = db_session.init_db()
    cc_cookie = Cookie(cookie_name='123',
                       cookie_recipe_url='https://www.youtube.com',
                       cookie_sku='CC007')
    cc_cookie.quantity = 12
    cc_cookie.unit_cost = 0.5
    with db_session() as session:
        session.add(cc_cookie)
        # session.commit()
        session.flush()
        print(cc_cookie.cookie_id)

    # Bulk insert:
    # c1 = Cookie(cookie_name='peanuts butter',
    #                    cookie_recipe_url='https://www.google.fr/?gws_rd=ssl',
    #                    cookie_sku='PB01',
    #                    quantity=24,
    #                    unit_cost=0.25)
    # c2 = Cookie(cookie_name='catmeal raisin',
    #                    cookie_recipe_url='https://www.facebook.com/',
    #                    cookie_sku='EWW01',
    #                    quantity=100,
    #                    unit_cost=1)
    # session.bulk_save_objects([c1, c2])
    # session.commit()
    # print(str(c1), str(c2))

        cookies = session.query(Cookie).all()
        print(cc_cookie.cookie_id)
        # print(cookies)
        for c in cookies:
            print(str(c))
            print(' ', repr(c))
            # print('c', c)



