from pydantic import BaseModel

from ....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    LabwareID: str
    PositionID: str


class ListedOptions(list[Options], BaseModel):
    TipCounter: str
