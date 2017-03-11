from scraper import Scraper


class Player(object):
    def __init__(self, site_id, name_first='', name_last=''):
        self.site_id = site_id
        self.name_first = name_first
        self.name_last = name_last
        # self.tournament_player_site_id = None  # TODO This parameter must be placed in the Entry class
        # self.club = None

    # def add_club(self, club):
    #     if self.club is not club:
    #         self.club = club
    #         club.add_player(self)

    def print_(self, until_class='Player', offset=0):
        print(' '*offset + str(self))
        # if until_class != self.__class__.__name__:
        #     pass

    def __str__(self):
        return '{0} {1} (#{2})'.format(self.name_first, self.name_last, self.site_id)

    def __eq__(self, other):
        return self.site_id == other.site_id

    def __hash__(self):
        return hash(self.site_id)


class Helper(object):
    # scraper = Scraper()
    players = set()
    players_in_tournament = {}  # TODO Convert it into a new custom class 'tournament_player'

    @staticmethod
    def scrape(tournament):
        # https://lfbb.tournamentsoftware.com/sport/player.aspx?id=D5D2E3E4-1C1C-4CD1-9661-1C6D8FDD3731&player=123
        # https://lfbb.tournamentsoftware.com/sport/players.aspx?id=D5D2E3E4-1C1C-4CD1-9661-1C6D8FDD3731
        # players = set()
        Scraper.site_url_tournament_sid = tournament.site_sid
        # for td in self._get_bs('players').find('table', class_='players').tbody.find_all('td'):
        tags_td = Scraper.get_BeautifulSoup(Player.__name__, 'all').find('table', class_='players').tbody.find_all('td')
        for td in tags_td:
            lst_a = td.find_all('a')
            if len(lst_a) > 0:
                player_full_name = lst_a[-1].text
                tournament_player_site_id = int(lst_a[-1]['href'].split('player=')[1])
                interm = Scraper.get_BeautifulSoup(Player.__name__, 'single', player=tournament_player_site_id)
                player_full_id = interm.find(id='content').find('div', class_='subtitle').find('a', title='Profil')['href'].split('id=')[1]
                player = Player(player_full_id,
                                player_full_name.split(',')[0].strip(),
                                player_full_name.split(',')[1].strip())
                Helper.players.add(player)
                Helper.players_in_tournament[(tournament, tournament_player_site_id)] = player
        return Helper.players

    # @staticmethod
    # def add_player(player):
    #     for p in Helper.players:
    #         if p == player:
    #             return p
    #     Helper.players.add(player)
    #     return player
    @staticmethod
    def add_player(tournament, tournament_player_site_id):
        if (tournament, tournament_player_site_id) not in Helper.players_in_tournament:
            Helper.scrape(tournament)
        # # tournament_player = Helper.players_in_tournament.intersection()
        # for player in Helper.players:
        #     if player.tournament_player_site_id == tournament_player_site_id:
        #         return player
        player = Helper.players_in_tournament.get((tournament, tournament_player_site_id), None)
        if not player:
            raise Exception('Not able to get player {0} in tournament {1]'
                            .format(tournament_player_site_id, tournament))
        return player
