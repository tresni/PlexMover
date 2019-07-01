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
        with cls.OpenKey() as reg:
            for k, v in settings.items():
                if isinstance(v, str):
                    type = winreg.REG_SZ
                    value = str(v)
                elif isinstance(v, (int, bool, float)):
                    type = winreg.REG_DWORD
                    value = int(v)
                else:
                    raise Exception('Unable to determine type for setting '
                                    '"%s"' % k)
                winreg.SetValueEx(reg, k, 0, type, value)

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
        # this can be in the registry too... Need to check that...
        # LocalAppDataPath is the Value
        try:
            with Windows.OpenKey() as reg:
                value, _ = winreg.QueryValueEx(reg, 'LocalAppDataPath')
                if value:
                    return value
        except OSError:
            pass
        return os.path.expandvars('%LOCALAPPDATA%\\Plex Media Server')
