from __future__ import print_function
import os
import plistlib


class Darwin(object):
    def importSettings(self, target):
        pass

    def exportSettings(self, target):
        path = os.path.expanduser('~/Library/Preferences/com.plexapp.plexmediaserver.plist')
        if not os.path.exists(path):
            return None

        with open(path, 'rb') as fp:
            return plistlib.load(fp)
