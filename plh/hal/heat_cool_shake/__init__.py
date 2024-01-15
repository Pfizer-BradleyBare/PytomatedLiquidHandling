from . import Base

identifier = str
devices: dict[identifier, Base.HeatCoolShakeABC] = dict()
