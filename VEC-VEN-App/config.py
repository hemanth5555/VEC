class Config(object):
    DEBUG = False
    TESTING = False

    # DATABASE_NAME = 'localaidb'
    # DB_USERNAME = 'root'
    # DB_PASSWORD = 'rootroot'
    # DB_CONFIG = 'localhost'

    DATABASE_NAME = 'localaidb'
    DB_USERNAME = 'admin'
    DB_PASSWORD = 'LuckyYou5*'
    DB_CONFIG = 'brainerd.cagp06uyemwc.us-east-1.rds.amazonaws.com'

    RABBITMQ_HOST = 'localhost'


class ProductionConfig(Config):
    pass



class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

