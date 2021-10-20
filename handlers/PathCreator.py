
class PathCreator:

    @staticmethod
    def generatePath(path, pathToAppend):
        try:
            return path+"\\"+pathToAppend
        except:
            return None
