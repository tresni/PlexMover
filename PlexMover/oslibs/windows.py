import os.path
import winreg

from PlexMover.oslibs import SettingsHandler


class Windows(SettingsHandler):
    def importSettings(self, target):
        pass

    def exportSettings(self, target):
        settings = {}
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                'Software\\Plex, Inc.\\Plex Media Server',
                                access=winreg.KEY_ALL_ACCESS) as reg:
                for index in range(winreg.QueryInfoKey(reg)[1]):
                    key, value, type = winreg.EnumValue(reg, index)
                    settings[key] = value
                return settings
        except OSError:
            return None

    def getDataPath(self):
        return os.path.expandvars('%LOCALAPPDATA%\\Plex Media Server')
