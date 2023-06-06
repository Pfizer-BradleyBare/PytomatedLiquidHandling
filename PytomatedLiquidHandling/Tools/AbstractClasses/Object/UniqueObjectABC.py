from abc import ABC
from dataclasses import dataclass

# This is an abstract loader class for loading configuration files


@dataclass
class UniqueObjectABC(ABC):
    """This is a unique object abstract base class.
    This class enables compatibility with the unique tracker.
    """

    UniqueIdentifier: str | int
