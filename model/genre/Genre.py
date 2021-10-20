from handlers.PathCreator import PathCreator
class Genre:
    def __init__(self, path, name):
        self.path = PathCreator.generatePath(path, name)
        self.name = name

    def get_name(self):
        return self.name

    def setName(self,name):
        self.name= name

    def get_path(self):
        return self.path

    def setPath(self, path):
        self.path = path