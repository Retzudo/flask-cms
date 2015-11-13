class temp_file():
    def __init__(self, filename, content):
        self.filename = filename
        self.content = content

    def _remove_file(self):
        import os
        try:
            os.remove(self.filename)
        except FileNotFoundError:
            pass

    def __enter__(self):
        self._remove_file()
        with open(self.filename, 'w') as f:
            f.write(self.content)

    def __exit__(self, type, value, traceback):
        self._remove_file()
