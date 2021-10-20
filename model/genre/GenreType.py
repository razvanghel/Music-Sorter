from enum import Enum

class GenreType(Enum):

    MINIMAL = "Minimal"
    DEEP_HOUSE = "Deep House"

    @staticmethod
    def getAllGenres():
        return list(map(lambda c: c.value, GenreType))