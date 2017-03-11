class Club(object):
    def __init__(self, name):
        self.name = name
        # self.players = set()

    # def add_player(self, player):
    #     if player not in self.players:
    #         self.players.add(player)
    #         player.add_club(self)

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
