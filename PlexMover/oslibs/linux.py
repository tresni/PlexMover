# /var/lib/plexmediaserver/Library/Application Support/Plex Media Server/

from PlexMover.oslibs import SettingsHandler


class Linux(SettingsHandler):
    def importSettings(cls, settings):
        pass

    def exportSettings(cls):
        pass

    def getDataPath():
        return '/var/lib/plexmediaserver/' \
               'Library/Application Support/Plex Media Server/'
