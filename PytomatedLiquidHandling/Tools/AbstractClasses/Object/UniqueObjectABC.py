from abc import ABC, abstractmethod

# This is an abstract loader class for loading configuration files


class UniqueObjectABC(ABC):
    """This is a unique object abstract base class.
    This class enables compatibility with the unique tracker.
    """

    @abstractmethod
    def GetUniqueIdentifier(self) -> str | int:
        """This method guarentees a unique value as either a string or an int.
        This guarentee is required for the unique tracker.

        Returns:
            str | int: A unique value
        """
        ...  # this doesn't actually raise an error. This is an abstract method so python will complain
