import os.path
import winreg

from PlexMover.oslibs import SettingsHandler


class Windows(SettingsHandler):
    @staticmethod
    def OpenKey():
        return winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                              'Software\\Plex, Inc.\\Plex Media Server',
                              access=winreg.KEY_ALL_ACCESS)

    @classmethod
    def importSettings(cls, settings):
        pass

    @classmethod
    def exportSettings(cls):
        settings = {}
        try:
            with cls.OpenKey() as reg:
                for index in range(winreg.QueryInfoKey(reg)[1]):
                    key, value, type = winreg.EnumValue(reg, index)
                    settings[key] = value
                return settings
        except OSError:
            return None

    @staticmethod
    def getDataPath():
        return os.path.expandvars('%LOCALAPPDATA%\\Plex Media Server')
