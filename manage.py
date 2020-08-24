from app import create_app
from app import db
from flask_script import Manager
from config import config


config_class = config['development']
app = create_app(config_class)


if __name__ == '__main__':
	manager = Manager(app)

	manager.run()