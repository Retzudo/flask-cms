from flask.ext.login import current_user
import markdown


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
            html = markdown.markdown(file_content, output_format='html5')
        else:
            html = file_content

        if current_user.is_authenticated:
            script = """<script>
            (function () {
                tinymce.init({
                    selector: '.edit-text',
                    inline: true
                });
            })();
            </script>"""
            html = '<div class="edit-text">{}</div>{}'.format(html, script)

        return html

    return dict(text_content=text_content)
