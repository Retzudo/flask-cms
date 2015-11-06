Flask CMS
=========

A mix between a static site generator and a CMS. The general site layout and
design is made with code. Editing text is only possible in fixed placed but
assisted with WYSIWYG. This system is meant for websites that rarely need only
minor updates which need to be made by untrained people.


TODO
----

- Admin login
- Editing text


How?
----

The idea is that we have a catch-all route that loads templates based on the
path string. Templates that should be matched by routes have a leading underscore.
If `/test` is requested load the template `_test.html`. If a site was rendered
once, the resulting HTML is saved into a redis DB. Since this CMS/generator
thing is meant for pages that rarely change, we don't need to re-render the
template on every request.

We also have a special template tag which lets us embed HTML files
from the `content` directory. If an admin is logged in, these tags also render a
WYSIWYG editor that lets an end-user change the text on the go.


Files and directories
---------------------

### `templates/master.html`
Just a basic HTML 5 template. Make your own pages extend this template.

### `templates/index.html`
This site is always displayed when `/` is requested in the browser.

### `templates/admin.html`
This is the login form for admin users. Don't change it unless you know what you
are doing.

### `templates/text_content.html`
Contains the HTML and JavaScript that lets an admin edit text when logged in.
Don't change it.

### `templates/_*.html`
If you create a file `_my-site.html` the route `/my-site` becomes available.
These files are rendered with Jinja2 and should extend `master.html`. If you
don't extend `master.html` text editing won't work.

### `content/`
This is the directory where you store your editable HTML snippets that you can
include into pages.


Custom template tags
--------------------

### `text_content`
This tag lets you include a HTML snippet form `content/` that becomes editable
when logged in. Use it like this: `{{ text_content('contact_info.html')|safe }}`.


Reserved routes
---------------
There are some reserved routes that can't become custom pages. These are `/login`,
`/logout` and `/update-text`--a POST-only route that allows for text editing.


Utils
-----
There is an executable Python script `add_admin.py` that lets you do exactly that.
It prompts for a user name and a password. The user name and the salted and hashed
password are stored in a a file. `users.dat` (human readable).


Why?
----

Generally CMSs are too bloated for small sites that rarely change and static site
generators are not designed for end users in mind because you need to know how
to use the command line.
