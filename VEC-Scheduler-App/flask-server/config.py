from dotenv import load_dotenv
load_dotenv()
import os

class ApplicationConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ['SECRET_KEY']

    # DATABASE_NAME = 'localaidb'
    # DB_USERNAME = 'root'
    # DB_PASSWORD = 'rootroot'
    # DB_CONFIG = 'localhost'

    DATABASE_NAME = 'localaidb'
    DB_USERNAME = 'admin'
    DB_PASSWORD = 'LuckyYou5*'
    DB_CONFIG = 'brainerd.cagp06uyemwc.us-east-1.rds.amazonaws.com'
    SQL_Alchemy_URI = 'mysql+pymysql://'+ DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_CONFIG + '/' + DATABASE_NAME

    RABBITMQ_HOST = 'localhost'


