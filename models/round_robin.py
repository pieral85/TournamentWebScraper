from scraper import Scraper

# # from models.draw import Draw, Helper as DrawHelper
# import models.draw as d
# from models.entry_position import EntryPosition
# from models.match import Match
import models
# from models import draw as d, EntryPosition, Match


class RoundRobin(models.Draw):
    def __init__(self):
        super(RoundRobin, self).__init__()
        # self.draw.round = 0
        self.type_ = 'RR'

    def test_abstract_method(self):
        pass


class Helper(object):
    # noinspection PyPep8Naming
    @staticmethod
    def scrape(roundRobin):
        x_firstTeam, x_club = None, None
        table = Scraper.get_BeautifulSoup(models.Draw.__name__, 'single', {'draw': roundRobin.site}).find(id='poule').table
        # TODO Try to merge with code in knockout
        for x, td in enumerate(table.thead.tr.find_all('td')):
            if td.text.upper().strip() == 'CLUB':
                x_club = x
            elif td.text.isdigit() and int(td.text) == 1:
                x_firstTeam = int(td.text)  # index_xs[x] = int(td.text)
        if not x_club or not x_firstTeam:
            raise Exception('Header not matching while trying to extract draw content.')

        team_index, lTags = None, []
        # TODO Put into Draw and merge with same code in knockout
        for y, tr in enumerate(table.tbody.find_all('tr')):
            lTags.append([])
            for x, td in enumerate(tr.find_all('td')):
                lTags[y].append(td)
        lTags = map(list, zip(*lTags))  # Transpose list

        for x, tag in enumerate(lTags):
            for y, td in enumerate(tag):


                # if x == 0:
                #     team_index = int(td.text) - 1
                if x == x_club:
                    club_names = td.stripped_strings
                    tournament_player_site_ids = Helper._get_tournament_player_site_ids(lTags[x+1][y])
                    team_entries = models.Helper.manage_new_entry(club_names,
                                                               tournament_player_site_ids,
                                                               None,
                                                               roundRobin)
                    entryPosition = models.EntryPosition(0, y)
                    entryPosition.set_entry(*team_entries)
                # elif x_club < x < x_firstTeam:
                # if x > x_club:
                    # if 'entrycell' in td.attrs['class']:
                    #     tournament_player_site_ids = Helper._get_tournament_player_site_ids(td)
                    #     entryPosition = EntryPosition(0, y)
                    #     entries = []
                    #     for tournament_player_site_id in tournament_player_site_ids:
                    #         entry = DrawHelper.find_entry(roundRobin, tournament_player_site_id)
                    #         entries.append(entry)
                    #     entryPosition.set_entry(*entries[:2])
                elif x >= x_firstTeam and (x - x_firstTeam) > y:
                    # td.find('span', id='match').find('span').
                    if 'score' in td.span.attrs['class']:
                        match = models.Match(roundRobin.get_entryPosition(0, y),
                                      roundRobin.get_entryPosition(0, x - x_firstTeam))
                        match.add_result(*[score.text for score in td.find('span', class_='score').find_all('span')])

                    index_y = int(td.text)
                # elif x == 1:
                #     index_ys[y] =
# class_='entrycell'
#                     < a
#                     href = "player.aspx?id=D5D2E3E4-1C1C-4CD1-9661-1C6D8FDD3731&amp;player=7" > Tanguy
#                     Dussein[1] < / a >
#             team_index += 1
        return roundRobin

    @staticmethod
    def _get_tournament_player_site_ids(tag_td_team):
        tournament_player_site_ids = []
        for player_tag_a in tag_td_team.find_all(models.DrawHelper.is_player):
            tournament_player_site_ids.append(int(player_tag_a['href'].split('player=')[1]))
        return tournament_player_site_ids[:]
