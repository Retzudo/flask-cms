from flask import render_template
from flask.ext.login import current_user


def is_logged_in():
    return current_user.is_authenticated


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

        print('##########', is_logged_in())
        if is_logged_in():
            return render_template(
                'text_content.html',
                file_name=file_name,
                html=file_content
            )
        else:
            return file_content

    return dict(text_content=text_content)
