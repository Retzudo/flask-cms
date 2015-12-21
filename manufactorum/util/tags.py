from flask import render_template
from flask.ext.login import current_user
from markdown import markdown
import os


def is_logged_in():
    return current_user.is_authenticated


def custom_tags():
    """
    Custom tag for injecting text into a template. If logged in, append
    the JavaScript for editing.
    """
    def text_content(file_name):
        """Read a file and return its content."""
        # The exception that might get thrown here is the one we want to show
        # the user if they specify a non-existing file so don't handle it.
        file_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(file_path, '../content/', file_name)
        with open(path) as f:
            file_content = f.read()

        if is_logged_in():
            return render_template(
                'text_content.html',
                file_name=file_name,
                html=file_content
            )
        else:
            return file_content

    def markdown_content(file_name):
        """Read a file and parse it as GitHub Markdown."""
        with open('content/{}'.format(file_name)) as f:
            file_content = f.read()

        return markdown(file_content, ['gfm'])

    return dict(text_content=text_content, markdown_content=markdown_content)
