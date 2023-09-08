from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar

from PytomatedLiquidHandling.HAL import TransportDevice


@dataclass
class TransportConfig:
    TransportDevice: TransportDevice.Base.TransportDeviceABC
    HomePickupOptions: Options
    AwayPickupOptions: Options
    HomeDropoffOptions: Options
    AwayDropoffOptions: Options

    @dataclass(init=False)
    class Options:
        def __init__(self, Config: dict[str, Any]):
            self.Config: dict[str, Any] = Config

        def __eq__(self, __value: object) -> bool:
            if not isinstance(__value, self.__class__):
                return False

            return True
        
        @staticmethod
        def 


from dataclasses import dataclass, field, fields


@dataclass
class d:
    Config: dict = field(init=True, compare=False)

    def __post_init__(self):
        mean = {field.name: field.type for field in fields(self) if field.init == False}
        print(mean)

        for key in mean:
            self.__dict__[key] = mean[key](self.Config[key])


@dataclass
class a(d):
    e: str = field(init=False, compare=False)
    f: int = field(init=False, compare=True)


@dataclass
class c(d):
    b: float = field(init=False, compare=True)


aa = a({"e": "", "f": 1})

ab = a({"e": "a", "f": "1"})
print(aa == ab)