from model.artists.Artist import Artist
from model.genre.Genre import Genre
from handlers.Reader import Reader
from collections import Counter

class Artists:

    def __init__(self, path, dict=None):
        if dict is None:
            self.genres = {}
        else:
            self.genres = dict
        self._duplicate_check()
        self.path = path

    def get_dict(self):
        return self.genres

    def add_artist(self, artist):
        try:
            self.genres[artist.get_genre()].append(artist)
        except:
            self.genres[artist.get_genre()] = [artist]

    def get_artist_names(self):
        result = []
        for artist in self.get_all_artists():
            result.append(artist.get_name())
        return sorted(result)

    def get_genres(self):
        return self.genres.keys()

    def get_path(self):
        return self.path

    def get_artist_by_name(self, name):

        artists = self.get_all_artists()
        try:
            index = self._binary_search(artists, 0, len(artists) - 1, name)
            if index >= 0:
                return artists[index]
        except:
            pass
        return None

    def get_artists_of_genre(self, genre):
        return self.genres[genre]

    def get_all_artists(self):
        arrays = self.genres.values()
        artists = []
        for array in arrays:
            for artist in array:
                artists.append(artist)
        return sorted(artists)

    def _binary_search(self, array, low, high, name):

        # Check base case
        if high >= low:

            mid = (high + low) // 2
            array_name = array[mid].get_name().lower()
            # If element is present at the middle itself
            if array_name == name.lower():
                return mid

            # If element is smaller than mid, then it can only
            # be present in left subarray
            elif array_name > name.lower():
                return self._binary_search(array, low, mid - 1, name)

            # Else the element can only be present in right subarray
            else:
                return self._binary_search(array, mid + 1, high, name)

        else:
            # Element is not present in the array
            return -1

    def _duplicate_check(self):
        a = self.get_all_artists()
        names = []
        for artist in a:
            name = artist.get_name()
            assert name not in names, f"Duplicate artist found: {name}. Please "
            names.append(name)

