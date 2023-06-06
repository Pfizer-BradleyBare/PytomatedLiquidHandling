from abc import ABC
from dataclasses import dataclass

# This is an abstract loader class for loading configuration files


@dataclass
class NonUniqueObjectABC(ABC):
    """This is a non-unique object abstract base class.
    This class enables compatibility with the non-unique tracker.
    """

    Identifier: str | int
