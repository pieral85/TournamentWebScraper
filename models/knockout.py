from scraper import Scraper
# from .club import Club, Helper as ClubHelper
# from .player import Player, Helper as PlayerHelper
# from .entry import Entry, Helper as EntryHelper
# from models.draw import D

# from .draw import Draw as Draw, Helper as DrawHelper
# import models.draw

# import models.draw
# from .entry_position import TeamPosition
# from .match import Match

# from models import Draw, DrawHelper, TeamPosition, Match
import models
# from abc import ABCMeta, abstractmethod
#
# class MyABC(object):
#     __metaclass__ = ABCMeta
#
# MyABC.register(tuple)

# Using inheritance:
# class Knockout(object, Draw):
    # def __init__(self):
    #     super(Draw, self).__init__()  # Draw.__init__()
    #
    # def eat_draw(self, draw):
    #     super(Knockout, self).event = draw.event
    #     ???self.event = draw.event
    #     self.site_id = draw.site_id
    #     self.name = draw.name
    #     self.round = 0
    #     self.index = draw.index
    #     self.type_ = draw.type_
    #     self.qualifying = draw.qualifying
    #     self.teamPositions = draw.teamPositions
# print(dir(models.draw))


class Knockout(models.Draw):
    __mapper_args__ = {'polymorphic_identity': 'knockout'}
                       # 'inherit_condition': id == Employee.id}

    def __init__(self):
        super(Knockout, self).__init__()
        self.type_ = 'KO'

    # def __init__(self, draw):
    #     self.draw = draw
    #     self.draw.type_ = 'KO'
    def test_abstract_method(self):
        pass


class Helper(object):
    @staticmethod
    def scrape(knockout):
        # draw = Draw
        x_club = None

        table = Scraper.get_BeautifulSoup(models.Draw.__name__, 'single', draw=knockout.site_id)\
            .find('div', class_='draw').table
        # table = self._get_bs('draw', {'draw', draw_id}).find('div', class_='draw').table
        # equivalent to: table = self._get_bs('draw', {'draw', draw_id}).find('div', class_='draw').find('table')
        knockout.name = table.caption.text
        for x, td in enumerate(table.thead.tr.find_all('td')):
            if td.text.upper().strip() == 'CLUB':
                x_club = x
                break
        if not x_club:
            raise Exception('Header not matching while trying to extract draw content.')

        # noinspection PyPep8Naming
        lTags = []  # List of Tag #NavigableString
        # noinspection PyPep8Naming
        # dTags = {}  # Dictionary of Tag TODO Use lTags or dTags but not both of them
        for y, tr in enumerate(table.tbody.find_all('tr')):
            lTags.append([])
            for x, td in enumerate(tr.find_all('td')):
                lTags[y].append(td)
                # dTags[(x, y)] = td
        lTags = list(map(list, zip(*lTags)))  # Transpose list
        dMapCoords = {}

        for x, tag in enumerate(lTags):
            index_team = 0
            for y, td in enumerate(tag):
                if knockout.event.name == 'SDB2' and y == 29 and x == x_club + 1:
                    print("SDB2", x, y)
                if knockout.event.name == 'SMC2' and (x == 5 and y == 9):  # if (x, y) in ((5, 8), (6, 8)):
                    print("SMC2", x, y)
                if x == 0:
                    if td.text.strip().isdigit():
                        dMapCoords[(x_club + 1, y)] = (0, int(td.text.strip()) - 1)
                elif x_club and x == x_club:
                    club_names = list(td.stripped_strings)
                    if club_names:
                        tournament_player_site_ids = Helper._get_tournament_player_site_ids(lTags[x + 1][y])
                        # Helper.manage_new_team_and_entries(td, lTags[x + 1][y], draw)
                        # TODO replace td.attr('class')[2] with a re:
                        models.DrawHelper.manage_new_team_and_entries(club_names,
                                                           tournament_player_site_ids,
                                                           lTags[x + 1][y].attrs['class'][2],
                                                           knockout)
                elif x > x_club:
                    if 'drawrulercell' in td.attrs.get('class', []):
                        # dMapCoords.setdefault((x - x_club - 1, index_team), (x, y))

                        dMapCoords.setdefault((x, y), (x - x_club - 1, index_team))
                        # tournament_player_site_ids = Helper._get_tournament_player_site_ids(td)
                        entry_site_drc_id = td.attrs['class'][2]  # lTags[x + 1][y].attrs['class'][2]
                        # teamPosition = Helper.get_teamPosition(knockout, td.attr('class')[2])
                        # TODO replace td.attr('class')[2] with a re:
                        # noinspection PyPep8Naming
                        teamPosition = models.TeamPosition(*dMapCoords[(x, y)])
                        team = models.DrawHelper.find_team(knockout, entry_site_drc_id)

                        # entries = []
                        # # for tag_a in td.find_all(Helper.is_player):
                        # for i_team, tournament_player_site_id in enumerate(tournament_player_site_ids):
                        #     # entries.append(self.get_player(Player(int(tag_a['href'].split('entry=')[1]))))
                        #     entry = models.DrawHelper.find_entry(knockout, tournament_player_site_id)
                        #     entries.append(entry)
                        #     if knockout.event.name == 'SMC2' and entry.player.name_first == 'Alaime':
                        #         print((x, y))
                        # teamPosition.set_entry(*entries[:2])  # TODO Ensure that players contains 1 or 2 players MAX!

                        teamPosition.set_team(team)
                        # knockout.add_teamPosition(teamPosition)
                        index_team += 1
                    elif td.span and 'score' in td.span.get('class', []):
                        coords_previous_round = Helper._get_coord_previous(*dMapCoords.get((x, y - 1)))
                        match = models.Match(knockout.get_teamPosition(*coords_previous_round[0]),
                                             knockout.get_teamPosition(*coords_previous_round[1]))
                        if knockout.get_teamPosition(*coords_previous_round[0]) == \
                                knockout.get_teamPosition(*coords_previous_round[1]):
                            print(coords_previous_round)  # TODO This should never happen...
                        # match.teamPosition1 = knockout.get_teamPosition(*coords_previous_round[0])
                        # match.teamPosition2 = knockout.get_teamPosition(*coords_previous_round[1])
                        # noinspection PyPep8Naming
                        teamPosition_winner = knockout.get_teamPosition(*dMapCoords.get((x, y - 1)))
                        span = td.find('span', class_='score')
                        if not span:
                            pass
                        elif len(span.find_all('span')) >= 2:
                            match.add_result(*[score.text for score in span.find_all('span')],
                                             swap_result=teamPosition_winner == match.teamPosition2)
                            if match and (match.result_set1 == (21, 18) or match.result_set1 == (18, 21)) and (
                                    match.result_set2 == (26, 24) or match.result_set2 == (24, 26)):
                                print(match.result_set1)
                        elif span.text.upper() == 'WALKOVER':
                            match.add_result('21-0', '21-0',
                                             swap_result=teamPosition_winner == match.teamPosition2)
                        else:
                            raise Exception('Unknown match result for following html tag: "{}"'.format(td.text))


                            # match.add_result(*[score.text for score in td.find('span', class_='score').find_all('span')],
                            #              swap_result=teamPosition_winner == match.teamPosition2)
                        # Helper.matchs.add(match)
        knockout.remove_teamPositions_withouh_match()
        return knockout

    # noinspection PyShadowingBuiltins
    @staticmethod
    def _get_coord_previous(round, index):
        if round == 0:
            return None
        return ((round - 1, index * 2),
                (round - 1, index * 2 + 1))

    # noinspection PyShadowingBuiltins
    @staticmethod
    def _get_coord_next(round, index):
        # noinspection PyRedundantParentheses
        return (round + 1, index//2)

    @staticmethod
    def _get_tournament_player_site_ids(tag_td_team):
        tournament_player_site_ids = []
        for player_tag_a in tag_td_team.find_all(models.DrawHelper.is_player):
            tournament_player_site_ids.append(int(player_tag_a['href'].split('player=')[1]))
        return tournament_player_site_ids[:]
