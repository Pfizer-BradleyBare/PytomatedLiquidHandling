from pydantic import Field

from ....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    HandleID: int
    ShakingSpeed: int = Field(ge=30, le=2500)
