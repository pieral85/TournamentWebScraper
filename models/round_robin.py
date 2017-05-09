from scraper import Scraper

# # from models.draw import Draw, Helper as DrawHelper
# import models.draw as d
# from models.entry_position import TeamPosition
# from models.match import Match
import models
# from models import draw as d, TeamPosition, Match


class RoundRobin(models.Draw):
    __mapper_args__ = {'polymorphic_identity': 'round_robin'}

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
        table = Scraper.get_BeautifulSoup(models.Draw.__name__, 'single', draw=roundRobin.site_id).find(id='poule').table
        # TODO Try to merge with code in knockout
        for x, td in enumerate(table.thead.tr.find_all(['td', 'th'])):
            if td.text.upper().strip() == 'CLUB':
                x_club = x
            elif td.text.isdigit() and int(td.text) == 1:
                x_firstTeam = x  # int(td.text)  # index_xs[x] = int(td.text)
        if not x_club or not x_firstTeam:
            raise Exception('Header not matching while trying to extract draw content.')

        team_index, lTags = None, []
        # TODO Put into Draw and merge with same code in knockout
        for y, tr in enumerate(table.tbody.find_all('tr')):
            lTags.append([])
            for x, td in enumerate(tr.find_all(['td', 'th'])):
                lTags[y].append(td)
        lTags = list(map(list, zip(*lTags)))  # Transpose list

        for x, tag in enumerate(lTags):
            for y, td in enumerate(tag):


                # if x == 0:
                #     team_index = int(td.text) - 1
                if x_club and x == x_club:
                    club_names = list(td.stripped_strings)
                    tournament_player_site_ids = Helper._get_tournament_player_site_ids(lTags[x+1][y])
                    models.DrawHelper.manage_new_team_and_entries(club_names,
                                                                  tournament_player_site_ids,
                                                                  lTags[x + 1][y].get('id'),
                                                                  roundRobin)
                    # teamPosition = models.TeamPosition(0, y)
                    # teamPosition.set_entry(*team_entries)
                # elif x_club < x < x_firstTeam:
                # if x > x_club:
                    # if 'entrycell' in td.attrs['class']:
                    #     tournament_player_site_ids = Helper._get_tournament_player_site_ids(td)
                    #     teamPosition = TeamPosition(0, y)
                    #     entries = []
                    #     for tournament_player_site_id in tournament_player_site_ids:
                    #         entry = DrawHelper.find_entry(roundRobin, tournament_player_site_id)
                    #         entries.append(entry)
                    #     teamPosition.set_entry(*entries[:2])

                # elif x == x_club + 1:
                #     # TODO Delete this entire block?
                #     teamPosition = models.TeamPosition(0, y)  # TODO Not sure 'y' is working fine!
                #     team = models.DrawHelper.find_team(roundRobin, lTags[x][y].get('id'))
                #     teamPosition.set_team(team)

                elif x >= x_firstTeam and x - x_firstTeam != y: # and (x - x_firstTeam) > y:
                    entry_site_drc_id = lTags[x_club + 1][y].get('id')
                    team = models.DrawHelper.find_team(roundRobin, entry_site_drc_id)
                    teamPosition = models.TeamPosition(x - x_firstTeam, y)
                    teamPosition.set_team(team)
                    if (x - x_firstTeam) > y and td.find('span', class_='score'): #TODO delete '(x - x_firstTeam) > y' part
                        match = models.Match(roundRobin.get_teamPosition(x - x_firstTeam, y),
                                             roundRobin.get_teamPosition(y, x - x_firstTeam))
                        # match = models.Match(roundRobin.get_teamPosition(0, y, entry_site_drc_id),
                        #                      roundRobin.get_teamPosition(0, x - x_firstTeam, entry_site_drc_id))
                        if match.teamPosition1.team.draw.name == 'SDA':
                            print(str(match.teamPosition1.team), str(match.teamPosition2.team), sep='+++')
                        span = td.find('span', class_='score')
                        if not span:    # TODO This part should be merged with the one in Knockout
                            pass
                        elif len(span.find_all('span')) >= 2:
                            match.add_result(*[score.text for score in span.find_all('span')],
                                             swap_result=False)
                        elif span.text.upper() in ('WALKOVER', 'PAS DE RENCONTRE'):
                            status = [st.upper().strip() for st in td.find_all(text=True)]
                            if 'GAGNÉ' in status:
                                team1won = True
                            elif 'PERDU' in status:
                                team1won = False
                            else:
                                raise Exception  # TODO
                            match.add_result('21-0', '21-0', swap_result=not team1won)
                        else:
                            raise Exception('Unknown match result for following html tag: "{}"'.format(td.text))

                            # index_y = int(td.text)
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
