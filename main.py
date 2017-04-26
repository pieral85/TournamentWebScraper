# TODO Rename methods starting with add_... by set_... when it is not for an iterable
# TODO Calling get_BeautifulSoup shoud be surrounded by a TRY CATCH
# TODO Manage eventual existing instance(s) of PhantomJS at startup of it
# TODO Manage multiple langages within config.py (surtout for html tags/values/...)

from models import TournamentHelper, PlayerHelper, EventHelper, DrawHelper, \
    Player, Tournament, Event, Draw, Entry, TeamPosition, Match
from config import DB_FILE_PATH, DB_CREATE_TABLES
from db import Base, session, engine, IntegrityError, select, join, Table, mapper
from sqlalchemy import or_
# link = 'https://lfbb.tournamentsoftware.com/sport/tournament.aspx?id=D5D2E3E4-1C1C-4CD1-9661-1C6D8FDD3731'
# url_root = 'https://lfbb.tournamentsoftware.com/sport/'


class TournamentScraper(object):
    def __init__(self, tournament_site_id):
        # phantomjs-2.1.1-windows\\phantomjs-2.1.1-windows\\bin\\phantomjs')
        # TODO check that file exists (to be secured):
        # self.driver = webdriver.PhantomJS(executable_path=os.getcwd() + '\\phantomjs')
        # self.driver.set_window_size(100, 500)  # TODO Useful???
        self.tournament_site_id = tournament_site_id
# Scraper.site_url_tournament_sid = tournament_site_id
        # self.tournament = Tournament(tournament_site_id)

        self.tournaments = set()
        self.players = set()

        if DB_CREATE_TABLES:
            Base.metadata.create_all(engine)  # TournamentScraper.create_tables()

        # users = Player.__table__
        # s = users.select()  # users.c.name_last == 'Kenny')
        # TournamentScraper._run(s)

    @staticmethod
    def _run(stmt):
        rs = stmt.execute()
        for row in rs:
            print(row)

    def get_tournament(self):
        tournaments = Tournament.__table__
        events = Event.__table__
        # mapper(Tournament, tournaments)
        # mary = session.query(Tournament).selectfirst(tournaments.c.name == 'BC Namur B1-B2-C1-C2 2016')

        tournaments = session.query(Tournament).\
            filter(Tournament.name == 'BC Namur B1-B2-C1-C2 2016')#.first()
        # event_mapper = mapper(Event, events)
        # s = select([tournaments, events])
        # s = join(tournaments, events).select()

        # for tournement in tournaments:
        #     print(tournement)
        #     for event in tournement.events:
        #         print(event)
        # self.scrape()
        # p = session.query(Player).filter(Player.name_first == 'Alaime').first()
        # p = session.query(Entry).join(EntryPosition).join(Match).first()#.filter(Player.name_first == 'Alaime').first()

        # session.query(Match).join(EntryPosition, or_(EntryPosition==Match.entryPosition1)).\
        # matchs = session.query(Match).join(Match.entryPosition1).\
        # join(EntryPosition.entry). \
        matchs = session.query(Match).join(TeamPosition, or_(Match.entryPosition1_id == TeamPosition.entryPosition_id, Match.entryPosition2_id == TeamPosition.entryPosition_id)).\
            join(Entry, or_(TeamPosition.entry_id == Entry.entry_id, TeamPosition.co_entry_id == Entry.entry_id)).\
            join(Entry.player).\
            join(Entry.club).join(Entry.draw).\
            join(Draw.event).join(Event.tournament).\
            filter(Player.name_first == 'Reinquin').\
            order_by(Player.site_sid, Event.event_id, Draw.round, TeamPosition.round).all()#.join(Match)#.filter(Player.name_first == 'Alaime').first()

        for match in matchs:
            print(match, match.point_assignment)

        # events = session.query(Event).\
        #     order_by(Player.site_sid, Event.event_id, Draw.round, EntryPosition.round).all()
        players = session.query(Player).all()
        for player in players:
            entryPositions = session.query(TeamPosition). \
                join(Entry, or_(TeamPosition.entry_id == Entry.entry_id, TeamPosition.co_entry_id == Entry.entry_id)). \
                join(Entry.player). \
                join(Entry.club).join(Entry.draw). \
                join(Draw.event).join(Event.tournament). \
                filter(Player == player). \
                order_by(Player.site_sid, Event.event_id, Draw.round, TeamPosition.round).all()

            factor = 0
            for entryPosition in entryPositions:
                # print(entryPosition)
                if entryPosition.match:
                    entryPosition.factor = factor
                    factor += 1
                else:
                    print("merde!!!")
                    # for event in events:
                    #     for draw in event.draws:
                    #         entryPosition = event.draws ep.factor

                    # filter(p.name_last == 'Alaime'). \
                    # filter(t.site_id == 'EF23-1346-...')
        session.commit()

                    # print(str(p))

    @staticmethod
    def create_tables():
        # TournamentHelper.create_table()
        EventHelper.create_table()

    def scrape(self):
        self.tournaments = TournamentHelper.scrape(self.tournament_site_id)
        # TournamentHelper.save()
        for tournament in self.tournaments:
            # PlayerHelper.scrape(tournament)
            # TODO: Here, should link player with tournament
            events = EventHelper.scrape(tournament)

            # EventHelper.save()
            for event in events:
                for draw in DrawHelper.scrape(event):
                    pass
        try:
            session.add_all(self.tournaments)#session.bulk_save_objects(self.tournaments) ###TournamentHelper.save()
            session.flush()
        except IntegrityError:
            for tournament in self.tournaments:
                session.delete(tournament)
            session.flush()
            # session.merge()
        session.commit()

    def print_all(self):
        for tournament in self.tournaments:
            tournament.print_('')
        for player in self.players:
            player.print_('')


if __name__ == '__main__':
    # tournamentScraper = TournamentScraper('D5D2E3E4-1C1C-4CD1-9661-1C6D8FDD3731')  # Bertrix 2017
        # Club id: http://lfbb.tournamentsoftware.com/default.aspx?id=2&cb=55127840-BDE8-4FF4-94C9-E5393A176E16
    tournamentScraper = TournamentScraper('9E9A83F7-77CE-4B60-B0BA-F5041F45DE19')  # Namur 2016
        # Club id: http://lfbb.tournamentsoftware.com/default.aspx?id=2&cb=C43F3CA1-811C-44EE-B218-4C6AE8A2173D
    # tournamentScraper.get_tournament()
    # TODO Try with a list/tupl/set of site_ids
    tournamentScraper.scrape()
    # tournamentScraper.print_all()
