class Entry(object):
    def __init__(self, player, club, draw, entry_site_drc_id, tournament_player_site_id):
        self.draw = None
        self.player = player
        self.club = club
        self.entry_site_drc_id = entry_site_drc_id
        self.tournament_player_site_id = tournament_player_site_id
        self.entryPositions = set()
        self.set_draw(draw)  # self.draw = draw
        # self.tournaments = {}

    # def add_player_site_id(self, tournament, player_site_id):
    #     self.tournaments[tournament] = player_site_id
    #
    # def get_player_site_id(self, tournament):
    #     return self.tournaments[tournament]

    def set_draw(self, draw):
        if draw is not self.draw:  # TODO Use != instead of 'is not'?
            self.draw = draw
            self.draw.add_entry(self)

    # noinspection PyPep8Naming
    def add_entryPosition(self, entryPosition, is_co_entry=False):
        if entryPosition not in self.entryPositions:
            self.entryPositions.add(entryPosition)
            entryPosition.set_entry(self if not is_co_entry else None,
                                    self if is_co_entry else None)

    def print_(self, until_class='Entry', offset=0):
        print('{0}Entry "{1}"'.format(' ' * offset, str(self)))
        if until_class != self.__class__.__name__:
            # print('{}Matchs:"'.format(' ' * (offset + 1)))
            for entryPosition in self.entryPositions:
                if entryPosition:
                    entryPosition.print_(until_class, offset+1)
        # if until_class != self.__class__.__name__:
        #     for entry in self.entries:
        #         pass

    def __str__(self):
        return '{0} - {1} (#{2})'.format(str(self.player),
                                         str(self.club),
                                         self.tournament_player_site_id)

    def __eq__(self, other):
        return self.player == other.player and \
               self.club == other.club and \
               self.draw == other.draw

    def __hash__(self):
        return hash('{0}|{1}|{2}'.format(self.player.__hash__(),
                                         self.club.__hash__(),
                                         self.draw.__hash__()))


class Helper(object):
    entries = set()

    @staticmethod
    def add_entry(entry):
        # for e in Helper.entries:
        #     if e == entry:
        #         return e
        Helper.entries.add(entry)
        return entry
        # if entry not in self.players:
        #     self.players.append(entry)

    # def get_entry(self, player_id):
    #     return self.get_entry(Player(player_id))