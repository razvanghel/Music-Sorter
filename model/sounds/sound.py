
class Sound():

    def __init__(self, path = None, file_name = None):
        self._path = path
        self._file_name = file_name

    def get_path(self):
        return self._path

    def set_name(self, name):
        self._file_name = name

    def get_name(self):
        return self._file_name

    def set_path(self, path):
        self._path = path