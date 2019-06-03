import os
import plistlib

from PlexMover.oslibs import SettingsHandler


class Darwin(SettingsHandler):
    @staticmethod
    def plistPath():
        return os.path.expanduser(
            '~/Library/Preferences/com.plexapp.plexmediaserver.plist')

    @classmethod
    def importSettings(cls, settings):
        pass

    @classmethod
    def exportSettings(cls):
        path = cls.plistPath()
        if not os.path.exists(path):
            return None

        with open(path, 'rb') as fp:
            return plistlib.load(fp)

    @staticmethod
    def getDataPath():
        return os.path.expanduser(
            '~/Library/Application Support/Plex Media Server/')
