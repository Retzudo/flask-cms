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

We also have a special template tag which lets us embed HTML or markdown files
from the `content` directory. If an admin is logged in, these tags also render a
WYSIWYG editor that lets an end-user change the text on the go.


Why?
----

Generally CMSs are too bloated for small sites that rarely change and static site
generators are not designed for end users in mind because you need to know how
to use the command line.
