from manufactorum import app
from flask import render_template, abort, redirect
from manufactorum import cache
from manufactorum.util import forms
from manufactorum.util import users
from manufactorum.util import content
from flask.ext.login import login_user
from flask.ext.login import logout_user
from flask.ext.login import login_required
from flask.ext.login import current_user
from jinja2.exceptions import TemplateNotFound


def is_logged_in():
    if current_user:
        return current_user.is_authenticated
    else:
        return False


def dont_cache():
    return is_logged_in() or app.debug


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = users.get_user(form.data['username'])
        if user:
            if user.check_password(form.data['password']):
                login_user(user)
                return redirect('/')

    return render_template('admin.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect('/')


@app.route('/update-text', methods=['POST'])
@login_required
def update_text():
    form = forms.UpdateTextForm(csrf_enabled=False)
    if form.validate_on_submit():
        content.update_file(form.data['file_name'], form.data['content'])
        cache.delete_all_paths()

    return ''


@app.route('/', defaults={'path': '_index'}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
@cache.cached(unless=dont_cache)
def index(path):
    try:
        if path == '_index':
            rendered = render_template('index.html')
        else:
            path = path.replace('/', '__')
            rendered = render_template('_{}.html'.format(path))
        return rendered
    except TemplateNotFound:
        abort(404)
