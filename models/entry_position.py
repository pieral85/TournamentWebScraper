# from .match import Match


class EntryPosition(object):
    # def __init__(self, draw, site_drc_id):
    # noinspection PyShadowingBuiltins
    def __init__(self, round, index):  # , entry, co_entry=None):
        self.entry = None
        self.co_entry = None
        # self.draw = None
        # self.set_draw(draw)
        # self.site_drc_id = site_drc_id

        self.round = round
        self.index = index
        self.match = None
        # self.set_entry(entry, co_entry)

    def set_entry(self, entry=None, co_entry=None):
        EntryPosition._check_entries_same_draw(entry, co_entry)
        if entry and self.entry is not entry:
            self.entry = entry
            entry.add_entryPosition(self, False)
        if co_entry and self.co_entry is not co_entry:
            self.co_entry = co_entry
            co_entry.add_entryPosition(self, True)
        # TOASK add a entry list into the draw object???

    def set_match(self, match, match_index):
        if self.match is not match:
            self.match = match
            self.match.set_entryPosition(self if match_index == 1 else None,
                                         self if match_index == 2 else None)

    @staticmethod
    def _check_entries_same_draw(entry1, entry2):
        if entry1 and entry2 and entry1.draw != entry2.draw:
            raise Exception('Both entries {0} and {1} should belong to the same draw.'
                            .format(entry1, entry2))

    # def set_draw(self, draw):
    #     if self.draw is not draw:
    #         self.draw = draw
    #         draw.add_entryPosition(self)

    def print_(self, until_class='EntryPosition', offset=0):
        print('{0}EntryPosition "{1}"'.format(' ' * offset, str(self)))
        if until_class != self.__class__.__name__:
            if self.match:
                self.match.print_(until_class, offset+1)

    def __str__(self):
        return '{0} & {1} (round {2}, index {3})'.\
            format(str(self.entry), str(self.co_entry), self.round, self.index)

    def __eq__(self, other):
        if not self.entry or self.round is None or self.index is None:
            raise Exception('Either entry ({0}), round ({1}) or index ({2}) has not been defined in '
                            'EntryPosition instance {3}.'
                            .format(str(self.entry), str(self.round), str(self.index), str(self)))
        return self.entry == other.entry and self.round == other.round and self.index == other.index

    def __hash__(self):
        return hash('{0}|{1}|{2}'.format(self.entry.__hash__(),
                                         self.round,
                                         self.index))
