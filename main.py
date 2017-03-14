# TODO Rename methods starting with add_... by set_... when it is not for an iterable
# TODO Calling get_BeautifulSoup shoud be surrounded by a TRY CATCH
# TODO Manage eventual existing instance(s) of PhantomJS at startup of it
# TODO Manage multiple langages within config.py (surtout for html tags/values/...)

from models import TournamentHelper, PlayerHelper, EventHelper, DrawHelper
from config import DB_FILE_PATH, DB_CREATE_TABLES
from db import Base, session, engine
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

    @staticmethod
    def create_tables():
        # TournamentHelper.create_table()
        EventHelper.create_table()

    def scrape(self):
        if DB_CREATE_TABLES:
            Base.metadata.create_all(engine)  # TournamentScraper.create_tables()
        self.tournaments = TournamentHelper.scrape(self.tournament_site_id)
        # TournamentHelper.save()
        for tournament in self.tournaments:
            # PlayerHelper.scrape(tournament)
            # TODO: Here, should link player with tournament
            events = EventHelper.scrape(tournament)
        session.add_all(self.tournaments)#session.bulk_save_objects(self.tournaments) ###TournamentHelper.save()
        session.flush()
        session.commit()
            # EventHelper.save()
            # for event in events:
            #     for draw in DrawHelper.scrape(event):
            #         pass

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
    # TODO Try with a list/tupl/set of site_ids
    tournamentScraper.scrape()
    tournamentScraper.print_all()
