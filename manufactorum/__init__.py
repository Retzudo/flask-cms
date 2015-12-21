from flask import Flask
from flask.ext.login import LoginManager
from manufactorum.util import tags
from manufactorum.util import users

app = Flask(__name__)

app.config.from_pyfile('default_settings.cfg')
app.config.from_pyfile('settings.cfg', silent=True)

app.context_processor(tags.custom_tags)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.user_loader(users.get_user)

import manufactorum.views
