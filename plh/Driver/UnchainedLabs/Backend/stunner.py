from __future__ import annotations

import pathlib
import subprocess
import threading
from dataclasses import field
from typing import Any, cast

from pydantic import dataclasses

from plh.driver.tools import BackendSimpleBase

from .unchained_labs_command_base import UnchainedLabsCommandBase
from .unchained_labs_response_base import UnchainedLabsResponseBase


@dataclasses.dataclass(kw_only=True)
class Stunner(BackendSimpleBase):
    ip_address: str
    port: int
    stunner_dll_object: Any = field(init=False)

    def __post_init__(self) -> None:
        base_path = pathlib.Path(__file__).parent / "bin"

        args = f"{base_path / 'streams.exe'} -d \"{base_path / 'Stunner.dll'}\""

        subprocess.call(args)  # noqa:S603
        # The stunner API access uses a .DLL library. This step cleans the .dll.
        # Microsoft will not let you load a .dll without cleaning it first. Fun Fact!

        import clr

        clr.AddReference(base_path / "Stunner.dll")  # type: ignore
        from UnchainedLabs_Instruments import Stunner as Stun  # type: ignore

        # The stunner API access uses a .DLL library. This step loads the .dll as a module.
        # Namespace is "UnchainedLabs_Instruments" and class is Stunner (This is a C# dll)

        self.stunner_dll_object = Stun(self.ip_address, self.port)
        # The stunner API access uses a .DLL library. This step creates the stunner class present in the .dll.

    def execute_thread(self: Stunner) -> None:
        command = cast(UnchainedLabsCommandBase, self._command)
        self._response = command.execute_command_helper(self.stunner_dll_object)

    def start(self: Stunner) -> None:
        BackendSimpleBase.start(self)

        UnchainedLabsResponseBase(
            status_code_raw=self.stunner_dll_object.Request_Access(),
        )

    def stop(self: Stunner) -> None:
        BackendSimpleBase.stop(self)

        UnchainedLabsResponseBase(
            status_code_raw=self.stunner_dll_object.Release_Access(),
        )

    def execute(self: Stunner, command: UnchainedLabsCommandBase) -> None:
        BackendSimpleBase.execute(self, command)

        threading.Thread(
            target=Stunner.execute_thread,
            args=(self,),
        ).start()
        # We use a thread because actions like open and close can take a while. Better to free up processing time.
