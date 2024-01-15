from pydantic import dataclasses, field_validator


@dataclasses.dataclass(kw_only=True)
class Interface:
    """Allows devices to abstract away functionality.

    Example: There are many systems which utilize pipette devices.
    Devices that inherit from interface will expose a set of abstract functions to simplify interaction across all systems.

    Attributes:
        Backend: The backend that will be used to execute physical actions. NOTE: devices are backend specific.
        BackendErrorHandling: Allows users to handle errors directly on the system or to return them to the HAL device. NOTE: some
        backends may not support error handling on the system.
    """

    Backend: BackendABC
    BackendErrorHandling: bool

    @field_validator("Backend", mode="before")
    def __ValidateBackend(cls, v):
        Objects = Backend.Devices
        Identifier = v

        if Identifier not in Objects:
            raise ValueError(
                Identifier
                + " is not found in "
                + Backend.Base.BackendABC.__name__
                + " objects.",
            )

        return Objects[Identifier]

    def Initialize(self):
        if self.Backend.IsRunning == False:
            self.Backend.StartBackend()

    def Deinitialize(self):
        if self.Backend.IsRunning == True:
            self.Backend.StopBackend()
