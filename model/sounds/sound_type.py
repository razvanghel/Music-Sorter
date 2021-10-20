
class SoundType:
    SONG = "SONG"
    SOUND = "SOUND"

    @staticmethod
    def other(type):
        if type == SoundType.SONG:
            return SoundType.SOUND
        else:
            return SoundType.SONG