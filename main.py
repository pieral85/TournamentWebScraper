# TODO Rename methods starting with add_... by set_... when it is not for an iterable
# TODO Calling get_BeautifulSoup shoud be surrounded by a TRY CATCH
# TODO Manage eventual existing instance(s) of PhantomJS at startup of it
# TODO Manage multiple langages within config.py (surtout for html tags/values/...)

# from itertools import zip_longest

# import urllib.parse as urlparse


# from models.tournament import Helper as th
# from models.event import Helper as eh
# from models.draw import Draw, Helper as dh
# # from models.player import Player, Helper as ph
# # from models.entry_position import EntryPosition
# # from models.club import Club
from scraper import Scraper
from models import TournamentHelper as th, EventHelper as eh, DrawHelper as dh
# link = 'https://lfbb.tournamentsoftware.com/sport/tournament.aspx?id=D5D2E3E4-1C1C-4CD1-9661-1C6D8FDD3731'
# url_root = 'https://lfbb.tournamentsoftware.com/sport/'


class TournamentScraper(object):
    def __init__(self, tournament_site_id):
        # self.driver = webdriver.PhantomJS(executable_path='C:\\Users\\Pierre\\PycharmProjects\\WebScraping\\
        # phantomjs-2.1.1-windows\\phantomjs-2.1.1-windows\\bin\\phantomjs')
        # TODO check that file exists (to be secured):
        # self.driver = webdriver.PhantomJS(executable_path=os.getcwd() + '\\phantomjs')
        # self.driver.set_window_size(100, 500)  # TODO Useful???
        self.tournament_site_id = tournament_site_id
        Scraper.site_url_tournament_sid = tournament_site_id
        # self.tournament = Tournament(tournament_site_id)

        self.tournaments = set()
        # self.events = set()
        self.players = set()
        # self.draws = set()
        # self.clubs = set()

    # # @staticmethod
    # @classmethod
    # def is_player(cls, tag):
    #     return tag.a.has_attr('href') and 'entry=' in tag.a['href']

    def scrape(self):
        # print('=== EVENTS ===')
        # for event in self.scrape_events():
        #     print(event)
        # print('\n\n=== PLAYERS ===')
        # for entry in self.scrape_players():
        #     print('{0}: {1} {2}'.format(entry.site_id, entry.name_first, entry.name_last))
        # self.driver.quit()

        # self.events = self.scrape_events()
        # self.players = self.scrape_players()
        # self.draws = self.scrape_draws()

        self.tournaments = th.scrape(self.tournament_site_id)

        for tournament in self.tournaments:
# self.players = ph.scrape(tournament)
            # TODO: Here, should link player with tournament
            for event in eh.scrape(tournament):
                for draw in dh.scrape(event):
                    pass

    def print_all(self):
        for tournament in self.tournaments:
            tournament.print_('')
        for player in self.players:
            player.print_('')

    # def scrape_players(self):
    #     # https://lfbb.tournamentsoftware.com/sport/player.aspx?id=D5D2E3E4-1C1C-4CD1-9661-1C6D8FDD3731&player=123
    #     # https://lfbb.tournamentsoftware.com/sport/players.aspx?id=D5D2E3E4-1C1C-4CD1-9661-1C6D8FDD3731
    #     players = set()
    #     for td in self._get_bs('players').find('table', class_='players').tbody.find_all('td'):
    #         lst_a = td.find_all('a')
    #         if len(lst_a) == 2:
    #             player_full_name = lst_a[1].text
    #             player_full_id = int(lst_a[1]['href'].split('entry=')[1])
    #             players.add(Player(player_full_id,
    #                                player_full_name.split(',')[0].strip(),
    #                                player_full_name.split(',')[1].strip()))
    #     return players

    # def scrape_draws(self):
    #     # TODO To be implemented
    #     draws = set()
    #     for draw_id in [3]:
    #         d = self._scrape_draw(draw_id)
    #         d.round = 0
    #         d.index = 0
    #         draws.add(d)
    #     return draws
    #
    # def _scrape_draw(self, draw_id):
    #     d = Draw
    #     x_club = 0
    #
    #     table = self._get_bs('draw', {'draw', draw_id}).find('div', class_='draw').table
    #     # equivalent to: table = self._get_bs('draw', {'draw', draw_id}).find('div', class_='draw').find('table')
    #     d.name = table.caption.text
    #     # TODO Can be improved by replacing find('thead').find('tr') by sth shorter
    #     for x, td in enumerate(table.thead.tr.find_all('td')):
    #         if td.text.upper().strip() == 'CLUB':
    #             x_club = x
    #             break
    #     if not x_club:
    #         print('No club has been setup')
    #
    #     lTags = []  # List of Tag #NavigableString
    #     dTags = {}  # Dictionary of Tag TODO Use lTags or dTags but not both of them
    #     for y, tr in enumerate(table.tbody.find_all('tr')):
    #         lTags.append([])
    #         for x, td in enumerate(tr.find_all('td')):
    #             lTags[y].append(td)
    #             dTags[(x, y)] = td
    #     lTags = map(list, zip(*lTags))  # Transpose list
    #
    #     for x, tag in enumerate(lTags):
    #         for y, td in enumerate(tag):
    #             if x_club and x == x_club:
    #                 self.link_player_club(td, lTags[x+1][y])
    #             elif x > x_club:
    #                 if 'drawrulercell' in td.attrs('class'):
    #                     # TODO replace td.attr('class')[2] with a re:
    #                     pp = self.get_playerPosition(d, td.attr('class')[2])
    #                     pp.round = x - x_club
    #                     pp.index = y
    #                     players = []
    #                     for tag_a in td.find_all(TournamentScraper.is_player):
    #                         players.append(self.get_player(Player(int(tag_a['href'].split('entry=')[1]))))
    #                     pp.add_player(*players[:2])  # TODO Ensure that players contains 1 or 2 players MAX!
    #             # TODO Encode here match results
    #     return d

    # # noinspection PyPep8Naming
    # def get_playerPosition(self, draw, site_drc_id):
    #     return None  # TODO

    # def link_player_club(self, tag_td_club, tag_td_team):
    #     clubs_name = tag_td_club.stripped_strings
    #     players_tag_a = tag_td_team.find_all(TournamentScraper.is_player)
    #     if len(clubs_name) != len(players_tag_a):
    #         raise Exception()
    #     for club_name, player_tag_a in zip(clubs_name, players_tag_a):
    #         # add club in list of clubs
    #         club = self.get_club(Club(club_name))
    #         player = self.get_player(Player(int(player_tag_a['href'].split('entry=')[1])))
    #         club.add_player(player)

    # def get_player(self, entry):
    #     for p in self.players:
    #         if p == entry:
    #             return p
    #     self.players.append(entry)
    #     return entry
    #     # if entry not in self.players:
    #     #     self.players.append(entry)
    #
    # def get_player(self, player_id):
    #     return self.get_player(Player(player_id))

    # def get_club(self, club):
    #     for c in self.clubs:
    #         if c == club:
    #             return c
    #     self.clubs.append(club)
    #     return club
    #
    # def _get_bs(self, url_prefix, args={}):
    #     link = url_root + url_prefix + '.aspx?id=' + self.tournament.site_sid
    #     for name, value in args.items:
    #         link += '&{0}={1}'.format(name, value)
    #     self.driver.get(link)
    #     return BeautifulSoup(self.driver.page_source, "html.parser")

    # def __del__(self):
    #     self.driver.quit()

if __name__ == '__main__':
    # config.init()
    # tournamentScraper = TournamentScraper('D5D2E3E4-1C1C-4CD1-9661-1C6D8FDD3731')  # Bertrix 2017
    tournamentScraper = TournamentScraper('9E9A83F7-77CE-4B60-B0BA-F5041F45DE19')  # Namur 2016
    # TODO Try with a list/tupl/set of site_ids
    tournamentScraper.scrape()
    tournamentScraper.print_all()

    # for player_id, first_name, last_name in [[123, 'Pierre', 'Alaime'],
    #                                          [456, 'Sophie', 'Ferreira'],
    #                                          [789, 'Lin', 'Dan'],
    #                                          [951, 'M', 'Sch']]:
    #     scraper.players.add(Player(player_id, first_name, last_name))
    # for name in ['Carlsbad',
    #              'Bertrix',
    #              'Saint-Léger']:
    #     scraper.clubs.add(Club(name))
    # scraper.tournament.print_('')
