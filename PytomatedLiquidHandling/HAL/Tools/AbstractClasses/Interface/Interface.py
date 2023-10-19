from pydantic import BaseModel, field_validator

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import BackendABC


class Interface(BaseModel):
    Backend: BackendABC
    CustomErrorHandling: bool

    def Initialize(self):
        self.Backend.StartBackend()

    def Deinitialize(self):
        self.Backend.StopBackend()
