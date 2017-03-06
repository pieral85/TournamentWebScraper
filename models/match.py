class Match(object):
    def __init__(self, entryPosition1, entryPosition2):
        self.entryPosition1 = None
        self.entryPosition2 = None
        self.result_set1 = None
        self.result_set2 = None
        self.result_set3 = None
        self.set_entryPosition(entryPosition1, entryPosition2)

    # noinspection PyPep8Naming
    def set_entryPosition(self, entryPosition1=None, entryPosition2=None):
        if entryPosition1 and self.entryPosition1 is not entryPosition1:
            self.entryPosition1 = entryPosition1
            self.entryPosition1.set_match(self, 1)
        if entryPosition2 and self.entryPosition2 is not entryPosition2:
            self.entryPosition2 = entryPosition2
            self.entryPosition2.set_match(self, 2)

    def add_result(self, result_set1, result_set2, result_set3=None, swap_result=False):
        self.result_set1 = Match._convert_result(result_set1, swap_result)
        self.result_set2 = Match._convert_result(result_set2, swap_result)
        self.result_set3 = Match._convert_result(result_set3, swap_result)

    # noinspection PyPep8Naming
    def get_winner_entryPositon(self):
        sets_summary = self._get_match_sets_summary()
        return self.entryPosition1 if max(sets_summary) == sets_summary[0] else self.entryPosition2

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
        if isinstance(result, str):
            # noinspection PyUnusedLocal
            converted_result = result.split('-')
        elif not isinstance(result, (tuple, list, set)):
            raise Exception('Variable "result" (={0}) must be either a list, tuple or string (type found:{1})'
                            .format(result, type(result)))
        converted_result = tuple(result) if not swap_result else tuple(result[::-1])

        if len(converted_result) != 2:
            raise Exception('Wrong match result type: {}'.format(result))
        return converted_result

    def __eq__(self, other):
        return self.entryPosition1 == other.entryPosition1 and \
               self.entryPosition2 == other.entryPosition2

    def __hash__(self):
        return hash('{0}|{1}'.format(self.entryPosition1.__hash__(),
                                     self.entryPosition2.__hash__()))
