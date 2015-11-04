from flask import Flask, render_template, abort
from jinja2.exceptions import TemplateNotFound
import markdown
import redis

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

app = Flask(__name__)
rd = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


@app.context_processor
def custom_tags():
    """Custom tag for injecting text into a template.

    Read a file and return its content. If it is a markdown file,
    parse it.
    """
    def text_content(file_name):
        # The exception that might get thrown here is the one we want to show
        # the user if they specify a non-existing file so don't handle it.
        with open('content/{}'.format(file_name)) as f:
            file_content = f.read()

        if file_name.endswith('.md'):
            return markdown.markdown(file_content, output_format='html5')
        else:
            return file_content

    return dict(text_content=text_content)


def delete_cache(path=None):
    """
    Deletes the cache entries for all cached paths or a specific cached path.
    """
    if path is None:
        for p in rd.lrange('#cached_paths#', 0, -1):
            rd.delete(p)
        rd.delete('#cached_paths#')
    else:
        rd.delete(path)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    cached = rd.get(path)
    if cached is not None:
        return cached
    else:
        try:
            rendered = render_template('_{}.html'.format(path))
            rd.set(path, rendered)
            rd.lpush('#cached_paths#', path)
            return rendered
        except TemplateNotFound:
            abort(404)


if __name__ == '__main__':
    app.run(debug=True)
