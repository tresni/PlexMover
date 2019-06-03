import abc


class SettingsHandler(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def importSettings(self, settings):
        raise NotImplementedError()

    @abc.abstractclassmethod
    def exportSettings(self):
        raise NotImplementedError()

    @abc.abstractstaticmethod
    def getDataPath():
        raise NotImplementedError()
