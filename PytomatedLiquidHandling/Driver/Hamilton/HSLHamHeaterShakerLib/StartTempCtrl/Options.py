from pydantic import Field, dataclasses

from ....Tools.BaseClasses import OptionsABC


@dataclasses.dataclass(kw_only=True)
class Options(OptionsABC):
    HandleID: int
    Temperature: float = Field(ge=0, le=100)
