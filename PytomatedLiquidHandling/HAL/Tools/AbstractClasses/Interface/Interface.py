from pydantic import BaseModel, field_validator

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import BackendABC
from PytomatedLiquidHandling.HAL import Backend


class Interface(BaseModel):
    Backend: BackendABC
    CustomErrorHandling: bool

    @field_validator("Backend", mode="before")
    def __ValidateBackend(cls, v):
        Objects = Backend.GetObjects()
        Identifier = v

        if Identifier not in Objects:
            raise ValueError(
                Identifier
                + " is not found in "
                + Backend.Base.BackendABC.__name__
                + " objects."
            )

        return Objects[Identifier]

    def Initialize(self):
        self.Backend.StartBackend()

    def Deinitialize(self):
        self.Backend.StopBackend()
