from db import Base, Column, Integer, String, Boolean
# from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
# from custom_type import SetLike


class Club(Base):
    __tablename__ = 't_club'
    club_id = Column(Integer, primary_key=True)
    name = Column(String(50), index=True)
    entries = relationship('Entry',
                           back_populates='club',
                           cascade='all, delete-orphan')
    _points = 0

    def __init__(self, name):
        self.name = name
        self._points = 0
        # self.players = set()

    # def add_player(self, player):
    #     if player not in self.players:
    #         self.players.add(player)
    #         player.add_club(self)

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        self._points = value

    def __str__(self):
        return '{}'.format(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class Helper(object):
    clubs = set()

    @staticmethod
    def add_club(club):
        for c in Helper.clubs:
            if c == club:
                return c
        Helper.clubs.add(club)
        return club
