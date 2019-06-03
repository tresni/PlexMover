from abc import ABCMeta, abstractmethod

class SettingsHandler(metaclass=ABCMeta):
    @abstractmethod
    def importSettings(self, target):
        raise NotImplementedError()

    @abstractmethod
    def exportSettings(self, target):
        raise NotImplementedError()
