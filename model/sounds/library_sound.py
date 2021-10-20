

class LibrarySound():

    def __init__(self, path, name, previous = ""):
        self._path = path
        self._name = f"{name} ({previous})".replace(" ()","")

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_path(self):
        return self._path

    def set_path(self, path):
        self._path = path