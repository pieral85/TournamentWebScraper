from scraper import Scraper


class Player(object):
    def __init__(self, site_id, name_first='', name_last=''):
        self.site_id = site_id
        self.name_first = name_first
        self.name_last = name_last
        self.tournament_player_site_id = None  # TODO This parameter must be placed in the Entry class
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
        return '{0} {1} ({2})'.format(self.name_first, self.name_last, self.site_id)

    def __eq__(self, other):
        # TODO A entry sould not be defined with the tournament associated!!!
        return self.site_id == other.site_id

    def __hash__(self):
        return hash(self.site_id)


class Helper(object):
    # scraper = Scraper()
    players = set()

    @staticmethod
    def scrape(tournament):
        # https://lfbb.tournamentsoftware.com/sport/player.aspx?id=D5D2E3E4-1C1C-4CD1-9661-1C6D8FDD3731&player=123
        # https://lfbb.tournamentsoftware.com/sport/players.aspx?id=D5D2E3E4-1C1C-4CD1-9661-1C6D8FDD3731
        players = set()
        Scraper.site_url_tournament_sid = tournament.site_sid
        # for td in self._get_bs('players').find('table', class_='players').tbody.find_all('td'):
        tags_td = Scraper.get_BeautifulSoup(Player.__name__, 'all').find('table', class_='players').tbody.find_all('td')
        for td in tags_td:
            lst_a = td.find_all('a')
            if len(lst_a) == 2:
                player_full_name = lst_a[1].text
                tournament_player_site_id = int(lst_a[1]['href'].split('player=')[1])
                player_full_id = Scraper.get_BeautifulSoup('player', 'all', {'player': tournament_player_site_id}) \
                    .find(id='content').find('div', class_='subtitle').find('a', title='Profil')['href'].split('id=')[1]
                players.add(Player(player_full_id,
                                   player_full_name.split(',')[0].strip(),
                                   player_full_name.split(',')[1].strip()))
        return players

    @staticmethod
    def add_player(player):
        for p in Helper.players:
            if p == player:
                return p
        Helper.players.add(player)
        return player
