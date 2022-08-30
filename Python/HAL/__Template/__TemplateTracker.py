from ..BaseConfiguration import BaseConfigurationTracker
from .__Template import __Template


class __TemplateTracker(BaseConfigurationTracker):
    def __init__(self):
        self.Collection: dict[__Template] = dict()

    def LoadManual(self, __TemplateInstance: __Template):
        Name = __TemplateInstance.GetName()

        if Name in self.Collection:
            raise Exception("__Template Device Already Exists")

        self.Collection[Name] = __TemplateInstance

    def GetLoadedObjectsAsDictionary(self) -> dict[__Template]:
        return self.Collection

    def GetLoadedObjectsAsList(self) -> list[__Template]:
        return [self.Collection[key] for key in self.Collection]

    def GetObjectByName(self, Name: str) -> __Template:
        return self.Collection[Name]
