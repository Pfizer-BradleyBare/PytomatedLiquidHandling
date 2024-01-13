from abc import abstractmethod
from dataclasses import field
from typing import Type, TypeVar

from pydantic import dataclasses

from ..Command import CommandABC
from ..Response import ResponseABC

ResponseABCType = TypeVar("ResponseABCType", bound=ResponseABC)


@dataclasses.dataclass(kw_only=True)
class BackendABC:
    """A base class for all backends."""

    Identifier: str
    """A name given to the backend. Creates compatibility with the HAL layer."""

    IsRunning: bool = field(init=False, default=False)
    """Is the backend running?"""

    @abstractmethod
    def StartBackend(self):
        """Should start the system software then establish communication. You should only call the method once."""
        if self.IsRunning == True:
            raise RuntimeError(f"{type(self).__name__} backend is already running")
        self.IsRunning = True

    @abstractmethod
    def StopBackend(self):
        """Should close the communication layer then kill the system software."""
        if self.IsRunning == False:
            raise RuntimeError(f"{type(self).__name__} backend is not running")
        self.IsRunning = False

    @abstractmethod
    def ExecuteCommand(self, Command: CommandABC):
        """Delivers the ```Command``` to the system to be executed."""
        if self.IsRunning == False:
            raise RuntimeError(f"{type(self).__name__} backend is not running")

    @abstractmethod
    def WaitForResponseBlocking(self, Command: CommandABC):
        """Waits for execution of ```Command``` to complete."""
        if self.IsRunning == False:
            raise RuntimeError(f"{type(self).__name__} backend is not running")

    @abstractmethod
    def GetResponse(
        self, Command: CommandABC, ResponseType: Type[ResponseABCType]
    ) -> ResponseABCType:
        """Returns a response described by ```ResponseType``` for the executed ```Command```.
        Response data is parsed by pydantic into the type specified. You may discard the response.
        NOTE: Exceptions may be raised upon execution. See the specific backend for exception details.
        """
        if self.IsRunning == False:
            raise RuntimeError(f"{type(self).__name__} backend is not running")
