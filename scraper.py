from selenium import webdriver
from bs4 import BeautifulSoup
import os
import time

from config import SITE_URL_ROOT, SITE_URL_ROOT_SPORT, SITE_URL_PREFIXES, SITE_URL_SUFFIX


# TODO This class should be a singleton
class Scraper(object):
    # def __init__(self, site_url_tournament_sid):
    #     self._driver = webdriver.PhantomJS(executable_path=os.getcwd() + '\\phantomjs')
    #     self._driver.set_window_size(100, 500)  # TODO Useful???
    #     self.site_url_tournament_sid = site_url_tournament_sid
    _driver = webdriver.PhantomJS(executable_path=os.getcwd() + '\\phantomjs',
                                  service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
    _driver.set_window_size(100, 500)  # TODO Useful???
    _empty_page_source = ''
    max_scraping_attempts = 3
    site_url_tournament_sid = ''

    # noinspection PyPep8Naming
    @staticmethod
    def get_BeautifulSoup(class_name, detail_level, url_args={}):
        """

        :param class_name:
        :param detail_level: 'all' for all entities of class_name; 'single' for 1
        :param url_args:
        :return: BeautifulSoup object
        """
        link = SITE_URL_ROOT + \
               SITE_URL_ROOT_SPORT + \
               SITE_URL_PREFIXES.get(class_name, class_name)[detail_level] + \
               SITE_URL_SUFFIX + Scraper.site_url_tournament_sid
        if not Scraper._empty_page_source:
            Scraper._empty_page_source = Scraper._driver.page_source
        # '<html><head></head><body></body></html>'
        for name, value in url_args.items():
            link += '&{0}={1}'.format(name, value)

        attempt = 1
        while True:
            # if attempt > 1:
            print('Attempt #{0} for scraping URL {1}'.format(attempt, link))
            Scraper._driver.get(link)
            if attempt > 1:
                time.sleep(5)
            if Scraper._driver.page_source != Scraper._empty_page_source:
                return BeautifulSoup(Scraper._driver.page_source, "html.parser")
            elif attempt >= Scraper.max_scraping_attempts:
                Scraper._driver.quit()
                raise Exception('Not able to get html content from following URL: {}'.format(link))
            attempt += 1

    # def getBS_userProfile(self, url):
    #     link = SITE_URL_ROOT + SITE_URL_ROOT_PROFILE + overview + SITE_URL_SUFFIX
    #     return self._driver.get(url)

    def __del__(self):
        self._driver.quit()
