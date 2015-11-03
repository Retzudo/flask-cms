from flask import Flask, render_template, abort
from jinja2.exceptions import TemplateNotFound
import markdown

app = Flask(__name__)


@app.context_processor
def custom_tags():
    """Custom tag for injecting text into a template.

    Read a file and return its content. If it is a markdown file,
    parse it.
    """
    def text_content(file_name):
        try:
            with open('content/{}'.format(file_name)) as f:
                file_content = f.read()
        except IOError:
            raise Exception('File "{}" not found')

        if file_name.endswith('.md'):
            return markdown.markdown(file_content, output_format='html5')
        else:
            return file_content

    return dict(text_content=text_content)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    try:
        return render_template('_{}.html'.format(path))
    except TemplateNotFound:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True)
