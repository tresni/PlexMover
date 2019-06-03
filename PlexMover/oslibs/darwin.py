import os
import plistlib

from PlexMover.oslibs import SettingsHandler


class Darwin(SettingsHandler):
    def importSettings(self, target):
        pass

    def exportSettings(self, target):
        path = os.path.expanduser(
            '~/Library/Preferences/com.plexapp.plexmediaserver.plist')
        if not os.path.exists(path):
            return None

        with open(path, 'rb') as fp:
            return plistlib.load(fp)

    def getDataPath(self):
        return os.path.expanduser(
            '~/Library/Application Support/Plex Media Server/')
