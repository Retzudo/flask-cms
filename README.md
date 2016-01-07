[![Build Status](https://travis-ci.org/Retzudo/manufactorum.svg)](https://travis-ci.org/Retzudo/manufactorum)

Manufactorum
============

Ever wanted to make a simple website but with the ability to edit text on the
fly without SSHing to remote servers and editing files or doing something else
overly complicated just to fix a typo? If you are like me, you don't want to use
a full-blown CMS for just a bit of HTML, CSS and text that rarely changes
because they are huge and generally suck for small websites.


How?
----

Similar to ye olde days, paths of your website only exist if there is a file for
it. If you want a path `/about` to be available you need to create a file
`templates/_about.html` and fill it with content (note the preceding `_`).
Because Manufactorum is based on Flask we have all the features of Jinja2
available to us. Here's an example for `_about.html`:

```html+jinja
{% extends "master.html" %}

{% block content %}
    <h1>Oi!</h1>
{% endblock %}
```

This extends the basic HTML5 template `master.html` (which already exists) and
fills the `content` block. If you now start Manufactorum and navigate to
`/about`, you'll see your website shouting "Oi!" at you. Every other path except
for `/` will result in a 404 error message. Because `/` is special, there's a
special file for it: `templates/index.html`. You can of course modify it to suit
your needs.

There are also custom template tags which make blocks of text editable by
admins. More on that further down.


Custom template tags
--------------------

### `text_content`
This tag lets you include a HTML snippet form `content/` that becomes editable
when logged in. Use it like this: `{{ text_content('contact_info.html')|safe }}`.
Note the `|safe` filter.

This tag uses TinyMCE to make text editable. If you safe your changes, the
original file is overwritten.

### `markdown_content`
This tag includes a GitHub Markdown file and parses it. Works the same as
`text_content` but the text is not editable (for now).


Settings
--------

There are some settings you can modify. To do that, create a file
`settings.cfg`. You can look up values to change in `default_settings.cfg`. I
highly encourage you to change `SECRET_KEY` to a random string. If you don't do
this, your installation will be vulnerable to CSRF attacks. Your should treat
`default_settings.cfg` as a read-only file in case you want to look up the
defaults.


Caching
-------

Caching is enabled by default and requires a running version of redis. It
greatly improves rendering times because templates are not rendered every time a
request is made. To disable caching, add `CACHING_DISABLED = True` to your
`settings.cfg`.


Files and directories
---------------------

### `templates/master.html`
Just a basic HTML 5 template. Make your own pages extend this template.

### `templates/index.html`
This site is always rendered when `/` is requested by a client.

### `templates/admin.html`
This is the login form for admin users. Don't change it unless you know what you
are doing.

### `templates/text_content.html`
Contains the HTML and JavaScript that lets an admin edit text when logged in.
Don't change it either.

### `templates/_*.html`
If you create a file `_my-site.html` the route `/my-site` becomes available.
These files are rendered with Jinja2 and can extend `master.html`. If you don't
extend `master.html` text editing won't work because all the needed JavaScripts
are included there.

### `content/`
This is the directory where you store your Markdown or editable HTML snippets
that you can include in your `_*.html` pages.


Reserved routes
---------------
There are some reserved routes that can't become custom pages. These are
`/login`, `/logout` and `/update-text`--a POST-only route that allows for text
editing.


Utils
-----
There is an executable Python script `add_admin.py` that lets you do add an
admin user. It prompts for a user name and a password. The user name and the
salted and hashed password are stored in a a file. `users.dat` (human readable).


Proper tutorial
---------------
WIP
