from scraper import Scraper
# from db import db_session, Column, Integer, String, Numeric
from db import Base, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from custom_type import SetLike

# Base = declarative_base()


class Event(Base):
    __tablename__ = 't_event'
    event_id = Column(Integer, primary_key=True)
    name = Column(String(10), index=True)
    site_sid = Column(Integer)
    tournament_id = Column(String(100), ForeignKey('t_tournament.site_sid'), nullable=False)
    tournament = relationship('Tournament', back_populates='events')
    draws = relationship('Draw',
                         back_populates='event',
                         cascade='all, delete-orphan')

    def __init__(self, tournament, site_sid, name):
        self.tournament = None
        self.site_sid = site_sid
        self.name = name
        self.draws = SetLike()  # set()
        self.set_tournament(tournament)

    def set_tournament(self, tournament):
        if self.tournament is not tournament:
            self.tournament = tournament
            tournament.add_event(self)

    def add_draw(self, draw):
        if draw not in self.draws:
            self.draws.append(draw)###add
            draw.set_event(self)

    def get_draw(self, round):
        for draw in self.draws:
            if draw.round == round:
                return draw
        return None

    def print_(self, until_class='Event', offset=0):
        print('{0}Event "{1}"'.format(' '*offset, str(self)))
        if until_class != self.__class__.__name__:
            for draw in self.draws:
                if draw:
                    draw.print_(until_class, offset+1)

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.site_sid)

    def __eq__(self, other):
        return self.tournament == other.tournament and self.site_sid == other.site_sid

    def __hash__(self):
        # TODO Check if __hash__ is working fine
        return hash('{0}|{1}'.format(self.tournament.__hash__(),
                                     self.site_sid))


class Helper(object):
    # scraper = Scraper()
    events = set()

    # @staticmethod
    # def create_table():
    #     with db_session() as session:
    #         Base.metadata.create_all(session.bind)
    #
    # @staticmethod
    # def save():
    #     with db_session() as session:
    #         for event in Helper.events:
    #             session.add(event)

    @staticmethod
    def calculate_factor(event):
        draw_round = 0
        for draw in event.draws:
            if draw.round == draw_round:
                for entry in draw.entries:
                    for teamPosition in entry.teamPositions:
                        teamPosition.get_teamPosition_previous_round()
                        #teamPosition.match.

    @staticmethod
    def scrape(tournament):
        # link = url_root + 'tournament.aspx?id=' + self.tournament.site_sid
        # self.driver.get(link)
        # events = set()
        # bs = BeautifulSoup(self.driver.page_source, "html.parser")
        # r = re.compile(r'...')
        # table class="tournamentevents"
        # bs.find_all('ul', class_="score")

        Scraper.site_url_tournament_sid = tournament.site_sid
        # for a in self._get_bs('tournament').find('table', class_='tournamentevents').td.find_all('a'):
        # for a in Scraper.get_BeautifulSoup(Event.__name__, 'all').find('table', class_='tournamentevents').td.find_all('a'):
        for a in Scraper.get_BeautifulSoup(Event.__name__, 'all')\
                .find('table', class_='admintournamentevents').tbody.find_all('a'):
            # print(a.text, a['href'])
            # print(a.text, urlparse.urljoin(link, a['href']))
            Helper.events.add(Event(tournament,
                                    int(a['href'].split('event=')[1]),
                                    a.text.upper().strip()))


        return Helper.events

    # @staticmethod
    # def print_(until_class='Event'):
    #     print(str(self))
    #     # TODO finish implementing this method