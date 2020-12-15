import pymysql
import os,sys
base_dir=os.path.dirname(os.path.abspath(__file__))

class Config(object):
    DEBUG = False

class LogConfig(object):
    LOG_FILE = os.path.join(base_dir, 'log')



config = {
    "base":Config,
    'log':LogConfig
}
