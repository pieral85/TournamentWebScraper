from scraper import Scraper
# from db import db_session, Column, Integer, String, Numeric
from db import Base, Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from custom_type import SetLike

# Base = declarative_base()


class Tournament(Base):
    __tablename__ = 't_tournament'
    site_sid = Column(String(100), primary_key=True)
    name = Column(String(100), index=True)
    events = relationship('Event',
                          back_populates='tournament',
                          cascade="all, delete-orphan")

    def __init__(self, site_sid):
        self.site_sid = str(site_sid)
        self.name = ''
        self.events = []#SetLike()  ### set()

    def add_event(self, event):
        if event not in self.events:
            self.events.append(event)###add
            event.set_tournament(self)

    # @classmethod
    def print_(self, until_class='Tournament'):
        print('Tournament "{}"'.format(str(self)))
        if until_class != self.__class__.__name__:
            for event in self.events:
                if event:
                    event.print_(until_class, 1)

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.site_sid)

    def __eq__(self, other):
        return self.site_sid == other.site_sid

    def __hash__(self):
        return hash(self.site_sid)


class Helper(object):
    # def __init__(self):
    # scraper = Scraper()
    tournaments = set()
    until_class = Tournament  # ??? keep it???

    # @staticmethod
    # def create_table():
    #     with db_session() as session:
    #         Base.metadata.create_all(session.bind)
    #
    # @staticmethod
    # def save():
    #     with db_session() as session:
    #         # if create_table:
    #         #     Base.metadata.create_all(session.bind)
    #         for tournament in Helper.tournaments:
    #             session.add(tournament)

    @staticmethod
    def scrape(site_sid):
        if isinstance(site_sid, (list, tuple, set)):
            for sid in site_sid:
                Helper.tournaments.add(Helper._scrape_tournament(sid))
        else:
            Helper.tournaments.add(Helper._scrape_tournament(site_sid))
        return Helper.tournaments

    @staticmethod
    def _scrape_tournament(site_sid):
        # TODO Scrape tournament
        t = Tournament(site_sid)
        Scraper.site_url_tournament_sid = site_sid
        # noinspection PyPep8Naming
        bsTournamentInfo = Scraper.get_BeautifulSoup(Tournament.__name__, 'single').find(id='divTournamentHeader')
        if not bsTournamentInfo:
            raise Exception('An issue appeared while trying to generate a '
                            'BeautifulSoup object in the _scrape_tournament method.')
        t.name = bsTournamentInfo.find('div', class_='title').h3.text
        return t

    # @staticmethod
    # def set_tournament(tournament):
    #     Helper.tournaments.add(tournament)

    @staticmethod
    def print_(until_class=Tournament):
        for t in Helper.tournaments:
            t.print_(until_class)
