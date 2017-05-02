import models
from db import Base, Column, Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from custom_type import SetLike


class Team(Base):
    __tablename__ = 't_team'
    team_id = Column(Integer, primary_key=True)
    entry_site_drc_id = Column(Integer)

    draw_id = Column(Integer, ForeignKey('t_draw.draw_id'))
    draw = relationship('Draw', back_populates='teams')

    teamPositions = relationship('TeamPosition',
                                 primaryjoin=models.TeamPosition.team_id == team_id)

    entry1_id = Column(Integer,
                       ForeignKey('t_entry.entry_id'),
                       nullable=False)
    entry1 = relationship('Entry',
                          foreign_keys=[entry1_id],
                          back_populates='_team1')
    entry2_id = Column(Integer,
                       ForeignKey('t_entry.entry_id'),
                       nullable=True)
    entry2 = relationship('Entry',
                          foreign_keys=[entry2_id],
                          back_populates='_team2')

    # def __init__(self, entry_site_drc_id, draw, entry1, entry2=None):
    def __init__(self, entry_site_drc_id, draw):
        self.draw = None
        self.entry1 = None
        self.entry2 = None
        self.entry_site_drc_id = entry_site_drc_id
        self.teamPositions = SetLike()
        self.set_draw(draw)
        # self.set_entry(entry1, entry2)

    def set_draw(self, draw):
        if draw is not self.draw:  # TODO Use != instead of 'is not'?
            self.draw = draw
            self.draw.add_team(self)

    def set_entry(self, entry1, entry2):
        """

        :param entry1: ... Can be None
        :param entry2: ... Can be None
        :return: None
        """
        if entry1 and self.entry1 != entry1:
        # if entry1 and self.entry1 is not entry1:
            self.entry1 = entry1
            self.entry1.set_team(self, 1)
        if entry2 and self.entry2 != entry2:
        # if entry2 and self.entry2 is not entry2:
            self.entry2 = entry2
            self.entry2.set_team(self, 2)
            # TODO Raise Exception if both entry1 and entry2 have not the same draw

    # noinspection PyPep8Naming
    def add_teamPosition(self, teamPosition):
        if teamPosition not in self.teamPositions:
            self.teamPositions.append(teamPosition)
            teamPosition.set_team(self)

    def print_(self, until_class='Team', offset=0):
        print('{0}Team "{1}"'.format(' ' * offset, str(self)))
        if until_class != self.__class__.__name__:
            for teamPosition in self.teamPositions:
                # if teamPosition:
                teamPosition.print_(until_class, offset + 1)

    def __str__(self):
        return '{0} - {1}'.format(str(self.draw), self.entry_site_drc_id)
        # s = '{}'.format(str(self.entry1))
        # if self.entry2:
        #     s += '{}'.format(str(self.entry2))
        # return s

    def __eq__(self, other):
        if not other:
            return None
        # return self.draw == other.draw and self.entry1 == other.entry1 and self.entry2 == other.entry2
        return self.draw == other.draw and self.entry_site_drc_id == other.entry_site_drc_id

    def __hash__(self):
        return hash('{0}|{1}'.format(self.draw.__hash__(),
                                     self.entry_site_drc_id))
        # return hash('{0}|{1}|{2}'.format(self.draw.__hash__(),
        #                                  self.entry1.__hash__(),
        #                                  self.entry2.__hash__()))


class Helper(object):
    teams = set()

    @staticmethod
    def add_team(team):
        Helper.teams.add(team)
