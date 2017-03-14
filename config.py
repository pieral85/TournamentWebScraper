import os

# === site config ===
SITE_URL_ROOT = 'https://lfbb.tournamentsoftware.com/'
SITE_URL_ROOT_SPORT = 'sport/'
# SITE_URL_ROOT_PROFILE = 'profile/'
SITE_URL_PREFIXES = {
    'Tournament': {'single': 'tournament'},
    'Player': {'single': 'player',
               'all': 'players'},
    'Event': {'single': 'event',
              'all': 'events'},
    'Draw': {'single': 'draw'}
}
SITE_URL_SUFFIX = '.aspx?id='

# === html files config ===
READ_FROM_FILE = True
PATH_ROOT = os.path.join(os.getcwd(), 'data', 'files')
_FOLDER_TOURNAMENT_ID = '___'
PATH_PREFIXES = {
    'Tournament': ('tournaments', _FOLDER_TOURNAMENT_ID),
    'Player': ('players',),
    'Event': ('tournaments', _FOLDER_TOURNAMENT_ID, 'events'),
    'Draw': ('tournaments', _FOLDER_TOURNAMENT_ID, 'events', 'draws'),
    'EntryPosition': ('tournaments', _FOLDER_TOURNAMENT_ID, 'events', 'draws', 'entryPositions')
}

# === database config ===
DB_CREATE_TABLES = True
DB_FILE_PATH = os.path.join(os.getcwd(), 'tournament.db')
DB_USERNAME = 'admin'
DB_PASSWORD = 'default'


# noinspection PyUnusedLocal
# def init():
#     global tournament_site_id
#     tournament_site_id = ''
