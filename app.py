import settings
from flask import Flask, render_template, abort, redirect, request
from flask.ext.login import LoginManager
from flask.ext.login import current_user
from flask.ext.login import login_user
from flask.ext.login import login_required
from jinja2.exceptions import TemplateNotFound
from util import tags
from util import cache
from util import users
from util import forms
from util import content

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY
app.context_processor(tags.custom_tags)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.user_loader(users.get_user)


def is_logged_in():
    return current_user.is_authenticated


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = users.get_user(form.data['username'])
        if user:
            if user.check_password(form.data['password']):
                print('passwords match')
                login_user(user)
                return redirect('/')

    return render_template('admin.html', form=form)


@app.route('/update-text', methods=['POST'])
@login_required
def update_text():
    form = forms.UpdateTextForm(csrf_enabled=False)
    if form.validate_on_submit():
        content.update_file(form.data['file_name'], form.data['content'])

    return ''


@app.route('/', defaults={'path': '_index'}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def index(path):
    cached = cache.get_path(path)
    if cached is not None and not is_logged_in() and not app.debug:
        return cached
    else:
        try:
            if path == '_index':
                rendered = render_template('index.html')
            else:
                rendered = render_template('_{}.html'.format(path))
            cache.cache_path(path, rendered)
            return rendered
        except TemplateNotFound:
            abort(404)


if __name__ == '__main__':
    app.run(debug=True)
