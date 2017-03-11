from selenium import webdriver
from bs4 import BeautifulSoup
import os
import time

# noinspection PyProtectedMember
from config import SITE_URL_ROOT, SITE_URL_ROOT_SPORT, SITE_URL_PREFIXES, SITE_URL_SUFFIX,\
    READ_FROM_FILE, PATH_ROOT, PATH_PREFIXES, _FOLDER_TOURNAMENT_ID


# TODO This class should be a singleton
class Scraper(object):
    # def __init__(self, site_url_tournament_sid):
    #     self._driver = webdriver.PhantomJS(executable_path=os.getcwd() + '\\phantomjs')
    #     self._driver.set_window_size(100, 500)  # TODO Useful???
    #     self.site_url_tournament_sid = site_url_tournament_sid
    _driver = webdriver.PhantomJS(executable_path=os.path.join(os.getcwd(), 'phantomjs.exe'),
                                  service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
    _driver.set_window_size(100, 500)  # TODO Useful???
    _empty_page_source = ''
    max_scraping_attempts = 3
    site_url_tournament_sid = ''

    @staticmethod
    def _get_file_name(class_name, dic_file_name):
        if len(dic_file_name) > 1:
            raise Exception('Impossible to generate a file name with a dictionnary having more than 1 item ({})'
                            .format(dic_file_name))
        path = os.path.join(PATH_ROOT,
                            *[folder if folder != _FOLDER_TOURNAMENT_ID else Scraper.site_url_tournament_sid
                              for folder in PATH_PREFIXES.get(class_name, class_name)])
        file_name = (str(list(dic_file_name.values())[0]) if len(dic_file_name) == 1 else '_') + '.html'
        os.makedirs(path, exist_ok=True)
        file_path = os.path.join(path, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, 'w'):
                pass
        return file_path

    @staticmethod
    # def _get_path(class_name, file_name):  # class_name):
    def _read_file_content(class_name, dic_file_name):  # class_name):
        # full_file_name = Scraper._get_full_file_name(class_name, file_name)
        # if os.path.exists() ...
        with open(Scraper._get_file_name(class_name, dic_file_name), "r+") as f:  # TODO "a+"?
            return ''.join(f.readlines())

    @staticmethod
    def _write_file_content(class_name, dic_file_name, file_content):
        # full_file_name = Scraper._get_full_file_name(class_name, file_name)
        with open(Scraper._get_file_name(class_name, dic_file_name), "w") as f:
            return f.writelines(file_content)  # TODO use .write???

    # noinspection PyPep8Naming
    @staticmethod
    def get_BeautifulSoup(class_name, detail_level, **url_args):
        """

        :param class_name:
        :param detail_level: 'all' for all entities of class_name; 'single' for 1
        :param url_args:
        :return: BeautifulSoup object
        """
        try:
            url = SITE_URL_ROOT + \
                  SITE_URL_ROOT_SPORT + \
                  SITE_URL_PREFIXES.get(class_name, class_name)[detail_level] + \
                  SITE_URL_SUFFIX + str(Scraper.site_url_tournament_sid)
        except Exception as e:
            print(str(e))
        if not Scraper._empty_page_source:
            Scraper._empty_page_source = Scraper._driver.page_source
        # '<html><head></head><body></body></html>'
        for name, value in url_args.items():
            url += '&{0}={1}'.format(name, value)

        html_inner = Scraper._read_file_content(class_name, url_args) if READ_FROM_FILE else None
        if html_inner:
            return BeautifulSoup(html_inner, "html.parser")

        attempt = 1
        while True:
            # if attempt > 1:
            print('Attempt #{0} for scraping URL {1}'.format(attempt, url))

            Scraper._driver.get(url)
            if attempt > 1:
                time.sleep(5)
            if Scraper._driver.page_source != Scraper._empty_page_source:
                beautifulSoup = BeautifulSoup(Scraper._driver.page_source, "html.parser")
                if READ_FROM_FILE:
                    Scraper._write_file_content(class_name, url_args, Scraper._driver.page_source)  # TODO Try beautifulsoup instead of Scraper._driver.page_source
                return beautifulSoup
            elif attempt >= Scraper.max_scraping_attempts:
                Scraper._driver.quit()
                raise Exception('Not able to get html content from following URL: {}'.format(url))
            attempt += 1

    # def getBS_userProfile(self, url):
    #     link = SITE_URL_ROOT + SITE_URL_ROOT_PROFILE + overview + SITE_URL_SUFFIX
    #     return self._driver.get(url)

    def __del__(self):
        self._driver.quit()
