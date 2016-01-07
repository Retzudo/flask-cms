from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.cache import Cache
from manufactorum import tags
from manufactorum import users

app = Flask(__name__)

app.config.from_pyfile('default_settings.cfg')
app.config.from_pyfile('settings.cfg', silent=True)

app.context_processor(tags.custom_tags)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.user_loader(users.get_user)

if not app.config['CACHING_DISABLED']:
    cache_config = {
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_PORT': app.config['REDIS_PORT'],
        'CACHE_REDIS_HOST': app.config['REDIS_HOST'],
        'CACHE_DEFAULT_TIMEOUT': 60*60,  # in seconds
    }
else:
    cache_config = {'CACHE_TYPE': 'null'}

cache = Cache(app, config=cache_config)

import manufactorum.views
