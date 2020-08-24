class Config:
	SECRET_KEY = 'Y-5K^ASk9MXqnC_WtCm2v&VzX27P6N95DPF5+u5c'


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/educcanal.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    ENV = 'development'
    TEST = True


class DevelopmentConfig(Config):
	DEBUG = True
	ENV = 'development'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///data/educcanal.sqlite3'
	SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
	DEBUG = False
	ENV = 'production'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///data/educcanal.sqlite3'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
	'production': ProductionConfig,
	'development': DevelopmentConfig,
	'test': TestConfig,
	'default': DevelopmentConfig
}
