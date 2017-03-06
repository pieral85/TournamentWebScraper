from scraper import Scraper
# from .club import Club, Helper as ClubHelper
# from .player import Player, Helper as PlayerHelper
# from .entry import Entry, Helper as EntryHelper
# # import models.knockout
# # import models.round_robin
# from .knockout import Knockout, Helper as KnockoutHelper
# from .round_robin import RoundRobin, Helper as RoundRobinHelper
# # from .entry_position import EntryPosition
# # from .match import Match

import models
# from models import Player, PlayerHelper, Club, ClubHelper, Entry, EntryHelper, Knockout, KnockoutHelper, RoundRobin, RoundRobinHelper


class Draw(object):
    def __init__(self):  # , event , name):
        # TODO include site_sid and modify __eq__ and __hash__ with it
        self.event = None
        self.site_id = 0
        self.name = ''  # name
        self.round = None
        self.index = None
        self.type_ = ''  # TODO Add an enum with 'KO' and 'RR'
        self.qualifying = None
        # self.entryPositions = set()
        self.entries = set()

        # self.set_event(event)

    def set_event(self, event):
        if self.event is not event:
            self.event = event
            self.event.add_draw(self)

    def add_entry(self, entry):
        if entry not in self.entries:
            self.entries.add(entry)
            entry.set_draw(self)

    def test_abstract_method(self):
        raise NotImplementedError()

    # # noinspection PyPep8Naming
    # def add_entryPosition(self, entryPosition):
    #     if entryPosition not in self.entryPositions:
    #         self.entryPositions.add(entryPosition)
    #         entryPosition.set_draw(self)

    # noinspection PyShadowingBuiltins,PyPep8Naming
    def get_entryPosition(self, round, index):
        # for entryPosition in self.entryPositions:
        #     if entryPosition.round == round and entryPosition.index == index:
        #         return entryPosition
        # return None
        for entry in self.entries:
            for entryPosition in entry.entryPositions:
                if entryPosition.round == round and entryPosition.index == index:
                    return entryPosition

    def print_(self, until_class='Draw', offset=0):
        print(' '*offset + str(self))
        if until_class != self.__class__.__name__:
            for entry in self.entries:
                entry.print_(until_class, offset+1)

    def __str__(self):
        return '{0} ({1}: round {2}, index {3}) (#{4})'\
            .format(self.name, self.type_, self.round, self.index, self.site_id)

    def __eq__(self, other):
        if not self.event or self.site_id:
            raise Exception('Either event or site_id has not been define in draw instance {}.'.format(str(self)))
            # TODO Replicate this securisation in all equivalent methods (within a generic function?)
        return self.event == other.event and self.site_id == other.site_id

    def __hash__(self):
        return hash('{0}|{1}'.format(self.event.__hash__(),
                                     self.site_id))


class Helper(object):
    # scraper = Scraper()
    draws = set()
    # Following attributes should be return by the caller to do an update:
    players = set()
    clubs = set()
    _entries = set()
    # matchs = set()

    # @staticmethod
    # def scrape():
        ## draws = set()
        ## Scraper.site_url_tournament_sid = event.tournament.site_sid
        # x_draw, x_type, x_qualify = 0, 0, 0
        # table = Scraper.get_BeautifulSoup(Draw.__name__, 'all').find('div', id='content').find('table', class_='ruler')
        #
        # for x, td in enumerate(table.thead.tr.find_all('td')):
        #     header = td.text.upper().strip()
        #     if header == 'TIRAGE AU SORT':
        #         x_draw = x
        #     elif header == 'TYPE':
        #         x_type = x
        #     elif header == 'QUALIFICATION':
        #         x_qualify = x
        # if not x_draw or not x_type or not x_qualify:
        #     raise Exception('Header not matching while trying to extract draws.')
        #
        # for y, tr in enumerate(table.tbody.find_all('tr')):
        #     # lTags.append([])
        #     draw = Draw()
        #     for x, td in enumerate(tr.find_all('td')):
        #         if x == x_draw:
        #             draw.site_id = int(draw. td.a['href'].split('draw=')[1])
        #             draw.name = td.a.text
        #         elif x == x_type:
        #             type_ = td.text.upper().strip()
        #             if type_ == 'POULE':
        #                 draw.type_ = 'RR'  # Round Robin
        #             elif type_ == 'TOURNOI D''ELIMINATION':
        #                 draw.type_ = 'KO'  # Knock-out
        #             else:
        #                 raise Exception('Unknown type while trying to exctract draws.')
        #
        #         elif x == x_qualify:
        #             qualify = td.text.upper().strip()
        #             if qualify == 'OUI':
        #                 draw.qualifying = True
        #             elif qualify == 'NON':
        #                 draw.qualifying = False
        #             else:
        #                 raise Exception('Unknown qualification while trying to exctract draws.')
        #     Helper.draws.add(draw)

        # for draw_id in [3]:
        #     d = Helper._scrape_draw(draw_id)
        #     d.round = 0
        #     d.index = 0
        #     Helper.draws.add(d)
        # return Helper.draws

    # noinspection PyPep8Naming
    # @staticmethod
    # def scrape_eventDraws(event):
    #     Helper.setup_eventDraw(event,
    #         Scraper.get_BeautifulSoup(event.__class__.__name__, 'single', {'event': event.site_sid}))

    # noinspection PyPep8Naming
    @staticmethod
    def scrape(event):
        x_draw, x_type, x_qualify = [None]*3
        table = Scraper.get_BeautifulSoup(event.__class__.__name__, 'single', {'event': event.site_sid})\
            .find('div', id='content').find('table', class_='ruler')
        for x, td in enumerate(table.thead.tr.find_all('td')):
            header = td.text.upper().strip()
            if header == 'TIRAGE AU SORT':
                x_draw = x
            elif header == 'TYPE':
                x_type = x
            elif header == 'QUALIFICATION':
                x_qualify = x
        if x_draw is None or x_type is None or x_qualify is None:
            raise Exception('Header not matching while trying to extract draws.')

        for y, tr in enumerate(table.tbody.find_all('tr')):
            # lTags.append([])
            # draw = Draw()
            draw_child, scrape = [None]*2

            type_ = tr.find_all('td')[x_type].text.upper().strip()
            if type_ == 'POULE':
                # draw.type_ = 'RR'  # Round Robin
                draw_child = models.RoundRobin()
                scrape = models.RoundRobinHelper.scrape
            elif type_ == "TOURNOI D'ÉLIMINATION":
                # draw.type_ = 'KO'  # Knockout
                draw_child = models.Knockout()
                scrape = models.KnockoutHelper.scrape
            else:
                raise Exception('Unknown type while trying to exctract draws.')

            for x, td in enumerate(tr.find_all('td')):
                if x == x_draw:
                    draw_child.site_id = int(td.a['href'].split('draw=')[1])
                    draw_child.name = td.a.text
                # elif x == x_type:
                #     type_ = td.text.upper().strip()
                #     if type_ == 'POULE':
                #         # draw.type_ = 'RR'  # Round Robin
                #         draw_child = RoundRobin()
                #     elif type_ == 'TOURNOI D''ELIMINATION':
                #         # draw.type_ = 'KO'  # Knockout
                #         draw_child = Knockout()
                #     else:
                #         raise Exception('Unknown type while trying to exctract draws.')

                elif x == x_qualify:
                    qualify = td.text.upper().strip()
                    if qualify == 'OUI':
                        draw_child.qualifying = True  # TODO Is this attribute useful?
                        draw_child.round = 0
                    elif qualify == 'NON':
                        draw_child.qualifying = False
                        draw_child.round = 1  # TODO Should manage special cases (see https://lfbb.tournamentsoftware.com/sport/event.aspx?id=82B349B5-F02F-4CC9-A93F-51AB3E83016A&event=3)
                    else:
                        raise Exception('Unknown qualification while trying to exctract draws.')
            draw_child.set_event(event)
            scrape(draw_child)
            Helper.draws.add(draw_child)
        return Helper.draws

    # @staticmethod
    # def _scrape_draw(draw_id):
    #     draw = Draw
    #     x_club = 0
    #
    #     table = Scraper.get_BeautifulSoup(Draw.__name__, 'single', {'draw', draw_id}).find('div', class_='draw').table
    #     # table = self._get_bs('draw', {'draw', draw_id}).find('div', class_='draw').table
    #     # equivalent to: table = self._get_bs('draw', {'draw', draw_id}).find('div', class_='draw').find('table')
    #     draw.name = table.caption.text
    #     # TODO Can be improved by replacing find('thead').find('tr') by sth shorter
    #     for x, td in enumerate(table.thead.tr.find_all('td')):
    #         if td.text.upper().strip() == 'CLUB':
    #             x_club = x
    #             break
    #     if not x_club:
    #         raise Exception('Header not matching while trying to extract draw content.')
    #
    #     # noinspection PyPep8Naming
    #     lTags = []  # List of Tag #NavigableString
    #     # noinspection PyPep8Naming
    #     dTags = {}  # Dictionary of Tag TODO Use lTags or dTags but not both of them
    #     for y, tr in enumerate(table.tbody.find_all('tr')):
    #         lTags.append([])
    #         for x, td in enumerate(tr.find_all('td')):
    #             lTags[y].append(td)
    #             dTags[(x, y)] = td
    #     lTags = map(list, zip(*lTags))  # Transpose list
    #     dMapCoords = {}
    #
    #     for x, tag in enumerate(lTags):
    #         index = 0
    #         for y, td in enumerate(tag):
    #             if x == 0:
    #                 if td.text.strip().isdigit():
    #                     dMapCoords[(x_club + 1, y)] = (0, int(td.text.strip())-1)
    #             elif x_club and x == x_club:
    #                 club_names = td.stripped_strings
    #                 tournament_player_site_ids = Helper._get_tournament_player_site_ids(lTags[x + 1][y])
    #                 # Helper.manage_new_entry(td, lTags[x + 1][y], draw)
    #                 # TODO replace td.attr('class')[2] with a re:
    #                 Helper.manage_new_entry(club_names,
    #                                         tournament_player_site_ids,
    #                                         td.attr('class')[2],
    #                                         draw)
    #             elif x > x_club:
    #                 if 'drawrulercell' in td.attrs['class']:
    #                     # dMapCoords.setdefault((x - x_club - 1, index), (x, y))
    #                     dMapCoords.setdefault((x, y), (x - x_club - 1, index))
    #                     tournament_player_site_ids = Helper._get_tournament_player_site_ids(td)
    #                     # entryPosition = Helper.get_entryPosition(draw, td.attr('class')[2])
    #                     # TODO replace td.attr('class')[2] with a re:
    #                     # noinspection PyPep8Naming
    #                     entryPosition = EntryPosition(draw, td.attr('class')[2])
    #                     entryPosition.round = dMapCoords[(x, y)][0]
    #                     entryPosition.index = dMapCoords[(x, y)][1]
    #                     entries = []
    #                     # for tag_a in td.find_all(Helper.is_player):
    #                     for tournament_player_site_id in tournament_player_site_ids:
    #                         # entries.append(self.get_player(Player(int(tag_a['href'].split('entry=')[1]))))
    #                         entry = Helper.find_entry(draw, tournament_player_site_id)
    #                         entries.append(entry)
    #                     entryPosition.set_entry(*entries[:2])  # TODO Ensure that players contains 1 or 2 players MAX!
    #                     draw.add_entryPosition(entryPosition)
    #                     index += 1
    #                 elif 'score' in td.span.attrs['class']:
    #                     match = Match()
    #                     coords_previous_round = Helper._get_coord_previous(dMapCoords.get((x, y-1)))
    #                     match.entryPosition1 = draw.get_entryPosition(*coords_previous_round[0])
    #                     match.entryPosition2 = draw.get_entryPosition(*coords_previous_round[1])
    #                     # noinspection PyPep8Naming
    #                     entryPosition_winner = draw.get_entryPosition(dMapCoords.get((x, y-1)))
    #                     match.add_result(*[score.text for score in td.find('span', class_='score').find_all('span')],
    #                                      swap_result=entryPosition_winner == match.entryPosition2)
    #                     Helper.matchs.add(match)
    #     return draw

    # # noinspection PyPep8Naming
    # @staticmethod
    # def get_entryPosition(draw, site_drc_id):
    #     return None

    # # noinspection PyShadowingBuiltins
    # @staticmethod
    # def _get_coord_previous(round, index):
    #     if round == 0:
    #         return None
    #     return ((round - 1, index*2),
    #             (round - 1, index*2 + 1))

    # # noinspection PyShadowingBuiltins
    # @staticmethod
    # def _get_coord_next(round, index):
    #     # noinspection PyRedundantParentheses
    #     return (round + 1, index//2)

    # @staticmethod
    # def _get_tournament_player_site_ids(tag_td_team):
    #     tournament_player_site_ids = []
    #     for player_tag_a in tag_td_team.find_all(Helper.is_player):
    #         tournament_player_site_ids.append(int(player_tag_a['href'].split('entry=')[1]))
    #     return tournament_player_site_ids[:]

    # noinspection PyPep8Naming
    @staticmethod
    def manage_new_entry(team_clubNames, tournament_player_site_ids, entry_site_drc_id, draw):
        #  TODO Move to draw.py?
        # team_clubNames = tag_td_club.stripped_strings
        # entries_tag_a = tag_td_team.find_all(Helper.is_player)
        entries_ = []
        if len(team_clubNames) != len(tournament_player_site_ids) or len(team_clubNames) < 1 or len(team_clubNames) > 2:
            raise Exception()
        for club_name, tournament_player_site_id in zip(team_clubNames, tournament_player_site_ids):
            # add club in list of clubs

            player = models.PlayerHelper.add_player(models.Player(tournament_player_site_id))
            # old way: player = self.get_player(Player(int(player_tag_a['href'].split('entry=')[1])))
            club = models.ClubHelper.add_club(models.Club(club_name))
            # old way: club = self.get_club(Club(club_name))
            # club.add_player(player)
            # EntryHelper.add_entry(EntryHelper.add_entry(Entry(player, club, draw, entry_site_drc_id)))
            entry = models.Entry(player, club, draw, entry_site_drc_id)
            Helper._entries.add(models.EntryHelper.add_entry(entry))
            entries_.append(models.EntryHelper.add_entry(entry))
            # Helper.players.add(player)
            # Helper.clubs.add(club)
            # Helper._entries.add(entry)
        return entries_

    @staticmethod
    def find_entry(draw, tournament_player_site_id):
        for entry in Helper._entries:
            if entry.draw == draw and entry.tournament_player_site_id == tournament_player_site_id:
                return entry
        return None

    @staticmethod
    def is_player(tag):
        # return tag.a.has_attr('href') and 'player=' in tag.a['href']
        return tag.name == 'a' and tag.has_attr('href') and 'player=' in tag['href']
