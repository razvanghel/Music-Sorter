from handlers.PathCreator import PathCreator

class Artist:

    def __init__(self, genre, name=""):
        self.name = name
        self.genre = genre
        self.path = PathCreator.generatePath(genre.get_path(), name)

    def get_name(self):
        return self.name

    def get_path(self):
        return self.path

    def set_path(self, path):
        self.path = path

    def get_genre(self):
        return self.genre

    def set_genre(self, genre):
        self.genre = genre

    def change_genre(self, genre):
        self.set_path(PathCreator.generatePath(genre.get_path(), self.get_name()))
        self.set_genre(genre)

    def set_name(self, name):
        self.name = name

    def __eq__(self, other):
        try:
            if self.name != other.get_name():
                return False
            elif self.path != other.get_path():
                return False
            return True
        except:
            return False

    def __lt__(self, other):
        return self.name < other
    def __gt__(self, other):
        return self.name > other

    def is_null(self):
        return self.name == "" or self.path == ""

    def is_not_null(self):
        return not self.is_null()