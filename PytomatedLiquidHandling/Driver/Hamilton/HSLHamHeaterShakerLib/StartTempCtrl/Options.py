from pydantic import Field

from ....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    HandleID: int
    Temperature: float = Field(ge=0, le=100)
