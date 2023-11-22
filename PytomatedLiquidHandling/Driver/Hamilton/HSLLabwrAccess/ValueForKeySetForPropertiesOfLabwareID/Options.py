from pydantic import BaseModel

from ....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    LabwareID: str


class ListedOptions(list[Options], BaseModel):
    PropertyKey: str
    PropertyValue: str | int
