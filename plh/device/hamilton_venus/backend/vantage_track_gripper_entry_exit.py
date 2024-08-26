import pathlib
from dataclasses import field

from pydantic import dataclasses

from .hamilton_backend_base import HamiltonBackendBase


@dataclasses.dataclass(kw_only=True)
class VantageTrackGripperEntryExit(HamiltonBackendBase):
    method: pathlib.Path = field(
        init=False,
        default=pathlib.Path(
            "C:\\Program Files (x86)\\HAMILTON\\Methods\\plh\\vantage\\BasicMethod.med",
        ),
    )
    deck_layout: pathlib.Path = pathlib.Path(
        "C:\\Program Files (x86)\\HAMILTON\\Methods\\plh\\vantage\\ExampleLayout.lay",
    )
