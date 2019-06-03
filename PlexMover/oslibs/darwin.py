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
        path = cls.plistPath()
        for key in ('NSStatusItem Preferred Position Item-0',
                    'PubSubServerPing'):
            if key in settings:
                settings[key] = float(settings[key])
        for key in ('AcceptedEULA',
                    'ButlerTaskUpdateScheduled',
                    'CinemaTrailersFromBluRay',
                    'CinemaTrailersFromTheater',
                    'CloudSyncNeedsUpdate',
                    'DisplayNotifications',
                    'DlnaEnabled',
                    'FSEventLibraryPartialScanEnabled'
                    'FSEventLibraryUpdatesEnabled',
                    'FirstRun',
                    'HardwareAcceleratedCodecs',
                    'LanguageInCloud',
                    'LogVerbose',
                    'ManualPortMappingMode',
                    'PlexOnlineHome',
                    'PublishServerOnPlexOnlineKey',
                    'ScheduledLibraryUpdatesEnabled',
                    'TreatWanIpAsLocal',
                    'agentAutoEnabled.com.plexapp.agents.lastfm.Albums.com.plexapp.agents.lyricfind',
                    'agentAutoEnabled.com.plexapp.agents.lastfm.Artists.com.plexapp.agents.vevo',
                    'agentAutoEnabled.com.plexapp.agents.plexmusic.Albums.com.plexapp.agents.lyricfind',
                    'autoEmptyTrash',
                    'logDebug',
                    'showDockIcon'):
            if key in settings:
                settings[key] = bool(settings[key])
        for key in ('CertificateVersion',
                    'LastAutomaticMappedPort',
                    'ManualPortMappingPort',
                    'MetricsEpoch',
                    'ScheduledLibraryUpdateInterval',
                    'TranscoderQuality',
                    'WanPerStreamMaxUploadRate',
                    'WanTotalMaxUploadRate'):
            if key in settings:
                settings[key] = int(settings[key])
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(path)
        with open(path, 'wb') as fp:
            plistlib.dump(settings, fp, fmt=plistlib.FMT_BINARY)

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
