import os
import shutil

import definitions
root = definitions.ROOT_DIR+"\\tests"
directory = root + "\\test_folder"
genres_path = directory + "\\Music"
songs_path = directory+"\\songs_folder"
dummies_folder = root + "\\dummies"
dummy_song = dummies_folder + "\\dummy_song.mp3"


def setUp():
    try:
        os.mkdir(directory)
        os.mkdir(songs_path)
        os.mkdir(genres_path)
    except:
        shutil.rmtree(directory)
        setUp()

def tearDown():
    shutil.rmtree(directory)
