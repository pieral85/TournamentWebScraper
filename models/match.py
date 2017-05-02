from db import Base, Column, Integer, String, Boolean
from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship, validates,  column_property, synonym
# import points_assignment as pa
from sqlalchemy.ext.hybrid import hybrid_property
from custom_type import SetLike


class Match(Base):
    __tablename__ = 't_match'
    match_id = Column(Integer, primary_key=True)
    s_result_set1 = Column('set1', String(5))
    s_result_set2 = Column('set2', String(5))
    s_result_set3 = Column('set3', String(5))

    teamPosition1_id = Column(Integer, ForeignKey('t_teamPosition.teamPosition_id'), nullable=False, unique=True)
    teamPosition1 = relationship('TeamPosition',
                                  foreign_keys=[teamPosition1_id],
                                  back_populates='_match1')

    teamPosition2_id = Column(Integer,
                               CheckConstraint('teamPosition1_id != teamPosition2_id',
                                               name='single_teamPosition_constraint'),
                               ForeignKey('t_teamPosition.teamPosition_id'),
                               nullable=False,
                               unique=True)
    teamPosition2 = relationship('TeamPosition',
                                  foreign_keys=[teamPosition2_id],
                                  back_populates='_match2')
    # teamPosition1_id = Column(Integer, ForeignKey('t_teamPosition.teamPosition_id'), nullable=False)
    # teamPosition1 = relationship('TeamPosition',
    #                               foreign_keys=[teamPosition1_id],
    #                               back_populates='match')
    #
    # teamPosition2_id = Column(Integer, ForeignKey('t_teamPosition.teamPosition_id'), nullable=False)
    # teamPosition2 = relationship('TeamPosition',
    #                               foreign_keys=[teamPosition2_id],
    #                               back_populates='match')


    # noinspection PyPep8Naming
    def __init__(self, teamPosition1, teamPosition2):
        self.teamPosition1 = None
        self.teamPosition2 = None
        # self._result_set1 = None
        # self.result_set2 = None
        # self.result_set3 = None
        self.set_teamPosition(teamPosition1, teamPosition2)

    # @validates('_s_result_set1')
    # def update_set1(self, key, value):
    #     self.result_set1 = Match._convert_result(value, False)
    #     return value
    #
    # @property
    # def s_result_set1(self):
    #     return self._s_result_set1
    #
    # @s_result_set1.setter
    # def s_result_set1(self, value):
    #     self._s_result_set1 = value
    #     self.result_set1 = Match._convert_result(value, False)

    # noinspection PyPep8Naming
    @staticmethod
    def _getStrResult(result):
        return '-'.join([str(score) for score in result]) if result else ''

    # noinspection PyPep8Naming
    def set_teamPosition(self, teamPosition1=None, teamPosition2=None):
        if teamPosition1 and self.teamPosition1 != teamPosition1:
            if teamPosition1 == teamPosition2:
                print(teamPosition1)
            self.teamPosition1 = teamPosition1
            self.teamPosition1.set_match(self, 1)
        if teamPosition2 and self.teamPosition2 != teamPosition2:
            if teamPosition1 == teamPosition2:
                print(teamPosition2)
            self.teamPosition2 = teamPosition2
            self.teamPosition2.set_match(self, 2)

    @property
    def result_set1(self):
        return Match._convert_result(self.s_result_set1, False)

    @property
    def result_set2(self):
        return Match._convert_result(self.s_result_set2, False)

    @property
    def result_set3(self):
        return Match._convert_result(self.s_result_set3, False)

    @hybrid_property  # @property
    def factor(self):
        return self.teamPosition1.factor + self.teamPosition2.factor

    # @result_set1.setter
    # def result_set1(self, value):
    #     self._result_set1 = value

    def add_result(self, s_result_set1, s_result_set2, s_result_set3=None, swap_result=False):
        # if result_set1.upper() == 'WALKOVER':
        #     result_set1, result_set2 = '21-0', '21-0'
        # self.result_set1 = Match._convert_result(s_result_set1, swap_result)
        # self.result_set2 = Match._convert_result(s_result_set2, swap_result)
        # self.result_set3 = Match._convert_result(s_result_set3, swap_result)
        self.s_result_set1 = s_result_set1  # Match._getStrResult(self.result_set1)
        self.s_result_set2 = s_result_set2  # Match._getStrResult(self.result_set2)
        self.s_result_set3 = s_result_set3  # Match._getStrResult(self.result_set3)
        self.teamPosition1.isWinner = not swap_result
        self.teamPosition2.isWinner = swap_result

    # noinspection PyPep8Naming
    def get_winner_entryPositon(self):
        sets_summary = self._get_match_sets_summary()
        return self.teamPosition1 if max(sets_summary) == sets_summary[0] else self.teamPosition2

    @staticmethod
    def _check_match_result(match_result):
        win, los = max(match_result), min(match_result)
        return win == 2 and (los == 0 or los == 1)

    def _get_match_sets_summary(self):
        """

        :return: Tuple containing sets win summary (eg: (2, 1) or (0, 2))
        """
        match_result = [0, 0]
        for result_set in (self.result_set1, self.result_set2, self.result_set3):
            match_result = [sum(elt) for elt in zip(match_result, Match._get_set_winner(result_set))]

        if not Match._check_match_result(match_result):
            raise Exception('Following match result does not match: {0} {1} {2}'
                            .format(self.result_set1, self.result_set2, self.result_set3))
        return match_result

    @staticmethod
    def _get_set_winner(result_set):
        if result_set:
            if not Match._check_set_result(result_set):
                raise Exception('Following set result does not match: {}'.format(result_set))
            return [1 if max(result_set) == result_set[0] else 0,
                    1 if max(result_set) == result_set[1] else 0]
        return [0, 0]

    @staticmethod
    def _check_set_result(result_set):
        los, win = min(result_set), max(result_set)
        return (win == 21 and 0 <= los <= 19) or \
               (22 <= win <= 30 and los == win - 2) or \
               (win == 30 and los == 29)

    @staticmethod
    def _convert_result(result, swap_result):
        # converted_result = None
        if not result:
            return None
        elif isinstance(result, str):
            # noinspection PyUnusedLocal
            result = result.split('-')
        elif not isinstance(result, (tuple, list)):
            raise Exception('Variable "result" (={0}) must be either a list or a tuple (type found:{1})'
                            .format(result, type(result)))
        result = tuple(result) if not swap_result else tuple(result[::-1])

        if len(result) != 2:
            raise Exception('Wrong match result type: {}'.format(result))
        return result

    def print_result(self):
        return ' '.join([str(s[0]) + '-' + str(s[1])
                         for s in (self.result_set1, self.result_set2, self.result_set3) if s])

    def print_(self, until_class='Match', offset=0):
        print('{0}Match "{1}"'.format(' ' * offset, str(self)))
        # if not isinstance(self, until_class):
        if until_class != self.__class__.__name__:
            pass

    def __str__(self):
        return '{0}   VS.   {1}: {2}'.format(str(self.teamPosition1),
                                             str(self.teamPosition2),
                                             self.print_result())

    def __eq__(self, other):
        return self.teamPosition1 == other.teamPosition1 and \
               self.teamPosition2 == other.teamPosition2

    def __hash__(self):
        return hash('{0}|{1}'.format(self.teamPosition1.__hash__(),
                                     self.teamPosition2.__hash__()))
