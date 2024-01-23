import dataclasses

from plh.driver.tools import OptionsBase


@dataclasses.dataclass(kw_only=True)
class Options(OptionsBase):
    CarrierPosition: int
    LabwareImageName: str
    LabwareSupportingText: int
    LabwareWellInformation: str


@dataclasses.dataclass(kw_only=True)
class OptionsList(list[Options]):
    DialogTitleText: str
    Step1Text: str
    Step2Text: str
    Carrier2DImageName: str
    Carrier3DImageName: str
