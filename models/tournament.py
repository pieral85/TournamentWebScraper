from scraper import Scraper


class Tournament(object):
    def __init__(self, site_sid):
        self.site_sid = str(site_sid)
        self.name = ''
        self.events = set()

    def add_event(self, event):
        if event not in self.events:
            self.events.add(event)
            event.set_tournament(self)

    # @classmethod
    def print_(self, until_class='Tournament'):
        print(str(self))
        # if not isinstance(self, until_class):
        if until_class != self.__class__.__name__:
            for event in self.events:
                event.print_(until_class, 1)

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.site_sid)

    def __eq__(self, other):
        return self.site_sid == other.site_id

    def __hash__(self):
        return hash(self.site_sid)


# TODO check if staticmethod is working for a class (and __init__ should not exist in a static class...)
# @staticmethod
class Helper(object):
    # def __init__(self):
    # scraper = Scraper()
    tournaments = set()
    until_class = Tournament  # ??? keep it???

    @staticmethod
    def scrape(site_sid):
        if isinstance(site_sid, (list, tuple, set)):
            for sid in site_sid:
                Helper.tournaments.add(Helper._scrape_tournament(sid))
        else:
            Helper.tournaments.add(Helper._scrape_tournament(site_sid))
        return Helper.tournaments

    @staticmethod
    def _scrape_tournament(site_sid):
        # TODO Scrape tournament
        t = Tournament(site_sid)
        Scraper.site_url_tournament_sid = site_sid
        # noinspection PyPep8Naming
        bsTournamentInfo = Scraper.get_BeautifulSoup(Tournament.__name__, 'single').find(id='divTournamentHeader')
        if not bsTournamentInfo:
            raise Exception('An issue appeared while trying to generate a '
                            'BeautifulSoup object in the _scrape_tournament method.')
        t.name = bsTournamentInfo.find('div', class_='title').h3.text
        return t

    # @staticmethod
    # def set_tournament(tournament):
    #     Helper.tournaments.add(tournament)

    @staticmethod
    def print_(until_class=Tournament):
        for t in Helper.tournaments:
            t.print_(until_class)
