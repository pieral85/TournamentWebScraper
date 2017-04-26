import models

from db import Base, Column, Integer, String, Boolean
from sqlalchemy import ForeignKey, or_, CheckConstraint
from sqlalchemy.orm import relationship
from custom_type import SetLike
from points_assignment import PointAssignment, getPointsAssignment


class TeamPosition(Base):
    __tablename__ = 't_teamPosition'
    teamPosition_id = Column(Integer, primary_key=True)
    round = Column(Integer)
    index = Column(Integer)
    factor = Column(Integer)
    isWinner = Column(Boolean)

    team_id = Column(Integer, ForeignKey('t_team.team_id'), nullable=False)
    team = relationship('Team',
                         foreign_keys=[team_id],
                         back_populates='teamPositions')
    # entry = relationship('Entry',
    #                 foreign_keys=[entry_id],
    #                 back_populates='teamPositions')
    # CheckConstraint('entry_id != co_entry_id', name='single_entry_constraint'),
    # co_entry_id = Column(Integer,
    #                 ForeignKey('t_entry.entry_id'),
    #                 nullable=True)
    # co_entry = relationship('Entry',
    #                    foreign_keys=[co_entry_id],
    #                    back_populates='teamPositions')

    # match_id = Column(Integer, ForeignKey('t_match.match_id'), nullable=True)
    match_index = Column(Integer)
    _match1 = relationship('Match',
                          primaryjoin=models.Match.teamPosition1_id == teamPosition_id,
                          uselist=False)
    _match2 = relationship('Match',
                          primaryjoin=models.Match.teamPosition2_id == teamPosition_id,
                          uselist=False)
    # match3 = or_(match, _match2)

    # match = relationship('Match',
    #                      primaryjoin=or_(models.Match.teamPosition1_id == teamPosition_id,
    #                                      models.Match.teamPosition2_id == teamPosition_id),
    #                      uselist=False)
    # TODO Check all cascade="all, delete-orphan" of all relationships
    pointsAssignement = getPointsAssignment()

    # noinspection PyShadowingBuiltins
    def __init__(self, round, index):  # , entry, co_entry=None):
        self.team = None
        #self.co_entry = None
        # self.draw = None
        # self.set_draw(draw)
        # self.site_drc_id = site_drc_id

        self.round = round
        self.index = index
        self.factor = 0
        self.isWinner = None
        self.match_index = None
        # self.match = None
        # self.set_team(entry, co_entry)

    @property
    def match(self):
        if self.match_index == 1:
            return self._match1
        elif self.match_index == 2:
            return self._match2

    @match.setter
    def match(self, value):
        if self.match_index == 1:
            self._match1 = value
        elif self.match_index == 2:
            self._match2 = value
        else:
            raise Exception('self.match_index should be 1 or 2 (currently: {})'.
                            format(self.match_index))

    def set_team(self, team):
        # TeamPosition._check_entries_same_draw(entry, co_entry)
        if self.team != team:
            self.team = team
            team.add_teamPosition(self)
        #if co_entry and self.co_entry is not co_entry:
         #   self.co_entry = co_entry
          #  co_entry.add_teamPosition(self)
        # TOASK add a entry list into the draw object???

    def set_match(self, match, match_index):
        self.match_index = match_index
        if self.match != match:
            self.match = match
            self.match.set_teamPosition(self if match_index == 1 else None,
                                         self if match_index == 2 else None)

    @property
    def pointAsignement(self):
        return TeamPosition.pointsAssignement[self.match.factor]


    # # noinspection PyPep8Naming
    # def get_previous_teamPosition(self):
    #     if self.round == 0 and self.entry.draw.round > 0:
    #         draw = self.entry.draw.event.get_draw(self.entry.draw.round - 1)
    #         if draw:
    #             return draw.get_last_teamPosition(self.entry)
    #         else:
    #             print("Oups, this should not happen...")
    #     return None
    #
    #     else:
    #         for teamPosition in self.entry.teamPositions:
    #             if teamPosition.round == self.round - 1:
    #                 return teamPosition
    #     return None

#    @staticmethod
#    def _check_entries_same_draw(entry1, entry2):
#        if entry1 and entry2 and entry1.draw != entry2.draw:
#            raise Exception('Both entries {0} and {1} should belong to the same draw.'
#                            .format(entry1, entry2))

    # def set_draw(self, draw):
    #     if self.draw is not draw:
    #         self.draw = draw
    #         draw.add_teamPosition(self)

    def print_(self, until_class='TeamPosition', offset=0):
        print('{0}TeamPosition "{1}"'.format(' ' * offset, str(self)))
        if until_class != self.__class__.__name__:
            if self.match:
                self.match.print_(until_class, offset+1)

    def __str__(self):
        if self.co_entry:
            return '{0} & {1} (round {2}, index {3})'.\
                format(str(self.team), str(self.co_entry), self.round, self.index)
        else:
            return '{0} (round {1}, index {2})'.\
                format(str(self.team), self.round, self.index)

    def __eq__(self, other):
        if not other:
            return self is None
        elif not self.team or self.round is None or self.index is None:
            raise Exception('Either entry ({0}), round ({1}) or index ({2}) has not been defined in '
                            'TeamPosition instance {3}.'
                            .format(str(self.team), str(self.round), str(self.index), str(self)))
        return self.team == other.team and self.round == other.round and self.index == other.index

    def __hash__(self):
        return hash('{0}|{1}|{2}'.format(self.team.__hash__(),
                                         self.round,
                                         self.index))
