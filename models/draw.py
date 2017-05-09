from scraper import Scraper

import models
from db import Base, Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from custom_type import SetLike


class Draw(Base):
    temp = 0

    __tablename__ = 't_draw'
    draw_id = Column(Integer, primary_key=True)
    site_id = Column(Integer)
    name = Column(String(30))
    round = Column(Integer)
    index = Column(Integer)
    type_ = Column(String(2))
    qualifying = Column(Boolean)
    event_id = Column(Integer, ForeignKey('t_event.event_id'), nullable=False)
    event = relationship('Event', back_populates='draws')
    discriminator = Column('type', String(50))
    __mapper_args__ = {'polymorphic_on': discriminator}
    # entries = relationship('Entry',
    #                        back_populates='draw',
    #                        cascade='all, delete-orphan')
    teams = relationship('Team',
                         back_populates='draw',
                         cascade='all, delete-orphan')

    def __init__(self):  # , event , name):
        # TODO include site_sid and modify __eq__ and __hash__ with it
        self.event = None
        self.site_id = 0
        self.name = ''  # name
        self.round = None
        self.index = None
        self.type_ = ''  # TODO Add an enum with 'KO' and 'RR'
        self.qualifying = None
        # self.teamPositions = set()
        self.teams = SetLike()  # self.entries = SetLike()

        # self.set_event(event)

    def set_event(self, event):
        if self.event is not event:
            self.event = event
            self.event.add_draw(self)

    # def add_entry(self, entry):
    #     if entry not in self.entries:
    #         self.entries.append(entry)
    #         entry.set_draw(self)
    def add_team(self, team):
        if team not in self.teams:
            self.teams.append(team)  # TODO self.teams.ADD instead???
            team.set_draw(self)

    # noinspection PyPep8Naming
    # def get_last_teamPosition(self, entry):
    #     for ent in self.entries:
    #         if ent.player == entry.player and ent.club == entry.club:
    #             return entry.get_last_teamPosition()
    #     return None

    # noinspection PyPep8Naming
    def remove_teamPositions_withouh_match(self):
        for team in self.teams:
            for teamPosition in team.teamPositions:
                if not teamPosition.match:
                    team.teamPositions.remove(teamPosition)
        # for entry in self.entries:
        #     for teamPosition in entry._teamPositions:
        #         if not teamPosition.match:
        #             # print('TeamPosition removed:', teamPosition)
        #             Draw.temp += 1
        #             print("a", Draw.temp)
        #             entry.teamPositions.remove(teamPosition)
        #     for teamPosition in entry._co_teamPositions:
        #         if not teamPosition.match:
        #             # print('TeamPosition removed:', teamPosition)
        #             Draw.temp += 1
        #             print("b", Draw.temp)
        #             entry.teamPositions.remove(teamPosition)

    def test_abstract_method(self):
        raise NotImplementedError()

    # noinspection PyShadowingBuiltins,PyPep8Naming
    def get_teamPosition(self, round, index):#, entry_site_drc_id=None):
        # for teamPosition in self.teamPositions:
        #     if teamPosition.round == round and teamPosition.index == index:
        #         return teamPosition
        # return None

        # for entry in self.entries:
        #     # for teamPosition in entry.teamPositions:
        #     for teamPosition in entry.team.teamPositions:
        #         if teamPosition.round == round and teamPosition.index == index:
        #             return teamPosition

        for team in self.teams:
            # if not entry_site_drc_id or entry_site_drc_id == team.entry_site_drc_id:
            for teamPosition in team.teamPositions:
                if teamPosition.round == round and teamPosition.index == index:
                    return teamPosition
        return None

    def print_(self, until_class='Draw', offset=0):
        print('{0}Draw "{1}"'.format(' ' * offset, str(self)))
        if until_class != self.__class__.__name__:
            # print('{}Entries:"'.format(' ' * (offset + 1)))
            for entry in self.entries:
                if entry:
                    entry.print_(until_class, offset+1)
            # print('{}Matchs:"'.format(' ' * (offset + 1)))
            # for match in self.

    def __str__(self):
        return '{0} ({1}: round {2}, index {3}) (#{4})'\
            .format(self.name, self.type_, self.round, self.index, self.site_id)

    def __eq__(self, other):
        if not self.event or not self.site_id:
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
    # _entries = set()
    _teams = set()
    # matchs = set()


    # noinspection PyPep8Naming
    @staticmethod
    def scrape(event):
        x_draw, x_type, x_qualify = [None]*3
        table = Scraper.get_BeautifulSoup(event.__class__.__name__, 'single', event=event.site_sid)\
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

        index_draw = 0
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
                elif x == x_qualify:
                    qualify = td.text.upper().strip()
                    if qualify == 'OUI':
                        draw_child.qualifying = True  # TODO Is this attribute useful?
                        draw_child.round = 0
                        draw_child.index = index_draw
                        index_draw += 1
                    elif qualify == 'NON':
                        draw_child.qualifying = False
                        draw_child.round = 1  # TODO Should manage special cases (see https://lfbb.tournamentsoftware.com/sport/event.aspx?id=82B349B5-F02F-4CC9-A93F-51AB3E83016A&event=3)
                        draw_child.index = 0
                    else:
                        raise Exception('Unknown qualification while trying to exctract draws.')
            draw_child.set_event(event)
            scrape(draw_child)
            Helper.draws.add(draw_child)
        return Helper.draws

    # noinspection PyPep8Naming
    @staticmethod
    def manage_new_team_and_entries(team_clubNames, tournament_player_site_ids, entry_site_drc_id, draw):
        # team_clubNames = tag_td_club.stripped_strings
        # entries_tag_a = tag_td_team.find_all(Helper.is_player)
        # entries_ = []
        if len(team_clubNames) != len(tournament_player_site_ids) or len(team_clubNames) < 1 or len(team_clubNames) > 2:
            raise Exception()
        team = models.Team(entry_site_drc_id, draw)
        for i, (club_name, tournament_player_site_id) in enumerate(zip(team_clubNames, tournament_player_site_ids)):
            # add club in list of clubs

            player = models.PlayerHelper.add_player(draw.event.tournament, tournament_player_site_id)  # TODO: /!\ The ID given to Player constructor should not be related the tournament!!!
            # player = models.PlayerHelper.add_player(models.Player(tournament_player_site_id))
            # old way: player = self.get_player(Player(int(player_tag_a['href'].split('entry=')[1])))
            club = models.ClubHelper.add_club(models.Club(club_name))
            # old way: club = self.get_club(Club(club_name))
            # club.add_player(player)
            # EntryHelper.add_entry(EntryHelper.add_entry(Entry(player, club, draw, entry_site_drc_id)))
            entry = models.Entry(player, club, team, i + 1, tournament_player_site_id)
            # Helper._entries.add(models.EntryHelper.add_entry(entry))
            models.EntryHelper.add_entry(entry)  # entries_.append(models.EntryHelper.add_entry(entry))
        Helper._teams.add(team)
        models.TeamHelper.add_team(team)
            # return entries_

    # @staticmethod
    # def find_entry(draw, tournament_player_site_id):
    #     for entry in Helper._entries:
    #         if entry.draw == draw and entry.tournament_player_site_id == tournament_player_site_id:
    #             return entry
    #     return None

    @staticmethod
    def find_team(draw, entry_site_drc_id):
        for team in Helper._teams:
            if team.draw == draw and team.entry_site_drc_id == entry_site_drc_id:
                return team
        return None

    @staticmethod
    def is_player(tag):
        # return tag.a.has_attr('href') and 'player=' in tag.a['href']
        return tag.name == 'a' and tag.has_attr('href') and 'player=' in tag['href']
