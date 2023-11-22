from pydantic import BaseModel, Field

from ....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    LabwareID: str


class ListedOptions(list[Options], BaseModel):
    TipCounter: str
    DialogTitle: str
    Timeout: int = Field(default=1000)
