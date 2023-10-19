from pydantic import BaseModel, field_validator

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import BackendABC
from PytomatedLiquidHandling.HAL import GetBackends


class Interface(BaseModel):
    Backend: BackendABC
    CustomErrorHandling: bool

    @field_validator("Backend")
    def __ValidateBackend(cls, v):
        if v not in GetBackends():
            raise ValueError(
                v + " not found in Backends. Did you disable or forget to add it?"
            )

        return GetBackends()[v]

    def Initialize(self):
        self.Backend.StartBackend()

    def Deinitialize(self):
        self.Backend.StopBackend()
