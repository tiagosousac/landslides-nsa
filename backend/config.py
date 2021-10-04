import os

class Config(object):
    LS_CSV_PATH = os.environ.get('LS_CSV_PATH')
    COUNTRY_CSV_PATH = os.environ.get('COUNTRY_CSV_PATH')