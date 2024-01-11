from enum import Enum
from typing import Any, Literal, cast

import dataclasses

from PytomatedLiquidHandling.Driver.Tools.BaseClasses import ResponseABC

from ..Exceptions import ErrorCodeDescriptionMap, ExceptionErrorCodeMap


@dataclasses.dataclass(kw_only=True)
class HamiltonBlockData:
    """Channel grouping of block data."""

    class ButtonIDs(Enum):
        """The possible buttons that can be pressed by the user when backend error handling is true and an error occurs."""

        NoError = 0
        """No button was pressed."""

        Abort = 1
        """Run aborted."""

        Cancel = 2
        """Run canceled. Note: If programmed, the backend error handling was executed."""

        Initialize = 3
        """Instrument initialized again."""

        Repeat = 4
        """Command repeated."""

        Exclude = 5
        """Channel or position excluded until the next tip pick up."""

        Waste = 6
        """Tip ejected to the default waste."""

        Air = 7
        """Rest of missing volume filled up with air."""

        Bottom = 8
        """Aspiration repeated on container bottom."""

        Continue = 9
        """Run continued without any change."""

        Barcode = 10
        """Barcode assigned manually."""

        Next = 11
        """Command repeated on next sequence position."""

        Available = 12
        """Available volume used."""

        Refill = 13
        """System reservoir of Nano Pipettor refilled."""

    Num: int
    """Step dependant information (e.g. the channel number, a loading position etc.)."""

    MainErr: int
    """Used to determine which exception to throw. See Exceptions to find the corresponding error codes."""

    SlaveErr: int
    """Slave error. Currently unused."""

    ButtonID: ButtonIDs
    """The button pressed by the user. See ButtonIDs enum which is an inner class."""

    StepData: int | float | str
    """Data associated with the step. Aspirated/dispensed volume, liquid height, barcode, etc."""

    LabwareID: str
    """Labware ID to which block data applies."""

    PositionID: str
    """Position ID to which block data applies."""


@dataclasses.dataclass(kw_only=True)
class HamiltonBlockDataPackage:
    """General step result format of supported single steps."""

    class ErrFlags(Enum):
        """Types of errors that can occur on the Hamilton."""

        NoErrorWithBlockData = 0
        """Step ends with ```OK```, no error occurred and no error handling was used. The block data contains the step-dependent information."""
        ErrorWithBlockData = 1
        """Step ends with ```OK```, ```Abort``` or ```Cancel```. Error handling was necessary. The block data contains the step-dependent information. 
        Note: The step data for this block are invalid if one of the following recoveries were used: Cancel, Abort, Continue, Exclude or Waste."""
        ErrorWithoutBlockData = 2
        """Step ends with a fatal error. Caution: The block data part is invalid. Result values 4-n may have undefined data."""

    ErrFlag: ErrFlags
    """Indicates whether an error occured or not and if block data is available. See ErrFlags enum which is an inner class."""

    BlockData: list[HamiltonBlockData]
    """Contains BlockData if the ErrFlag indicates as such."""


@dataclasses.dataclass(kw_only=True)
class HamiltonResponseABC(ResponseABC):
    """Base class for all responses from Hamilton systems.
    - All ```HamiltonBlockData``` will be parsed and converted automatically if present as a response field.
    - If unhandled errors exists then an exception grouping of all unhandled errors that occrured will be raised.
    """

    ErrorDescription: str | Literal[""]
    """There are, unfortunately, 2 cases here:
    - Case 1: Hamilton throws an error and the error is not handled by the user. Description is set, BlockData may or may not be available.
    We will use the description to throw the correct exception.
    - Case 2: Hamilton throws an error and the error is handled by the user. Description is not set, BlockData is available.
    We will use the MainErr to throw the correct exception."""

    # TODO

    # @field_validator("*", mode="before")
    # NOTE: This will attempt to validate all data but will only validate HamiltonBlockDataPackage types internally
    def __HamiltonBlockDataValidate(cls, v, Info):
        if cls.__dataclass_fields__[
            cast(str, Info.field_name)
        ].type == HamiltonBlockDataPackage and not isinstance(
            v, HamiltonBlockDataPackage
        ):
            v = cast(str, v)

            if len(v) == 0:
                return HamiltonBlockDataPackage(
                    ErrFlag=HamiltonBlockDataPackage.ErrFlags.ErrorWithoutBlockData,
                    BlockData=[],
                )
            # NOTE: Not sure if this is required but putting it here for now.

            ErrFlag = int(v[:1])
            # ErrFlag is always the first digit

            v = v[1:]
            # Remove ErrFlag from string

            v = [i.split(",") for i in v.split("[")]
            # Split based on Hamilton special block separator then split based on data separator

            BlockData = list()
            for i in range(
                1, len(v)
            ):  # Always start from 1 because the first set of block data is empty (Hamilton delimiter stuff)
                BlockData.append(
                    HamiltonBlockData(
                        **cast(
                            dict,
                            dict(
                                Num=v[i][0],
                                MainErr=v[i][1],
                                SlaveErr=v[i][2],
                                ButtonID=int(v[i][3]),
                                StepData=v[i][4],
                                LabwareID=v[i][5],
                                PositionID=v[i][6],
                            ),
                        )
                    )
                )
            # Extract the block data

            return HamiltonBlockDataPackage(
                **cast(
                    dict,
                    dict(
                        ErrFlag=ErrFlag,
                        BlockData=sorted(BlockData, key=lambda x: x.Num),
                    ),
                )
            )
        # Only run on HamiltonBlockDataPackage types

        return v

    def __post_init__(self) -> None:
        Exceptions = list()

        ErrorOccurred = False

        for Item in self.__dict__.values():
            if isinstance(Item, HamiltonBlockDataPackage):
                ErrorOccurred = ErrorOccurred | Item.ErrFlag.value

                if Item.ErrFlag == HamiltonBlockDataPackage.ErrFlags.ErrorWithBlockData:
                    for Data in Item.BlockData:
                        if (
                            Data.ButtonID == Data.ButtonIDs.Cancel
                        ):  # We only care about Cancel button because that means this error was NOT handled.
                            if Data.MainErr in ExceptionErrorCodeMap:
                                Exceptions.append(
                                    ExceptionErrorCodeMap[Data.MainErr](Data)
                                )

        # This is the case where the Error does NOT have block data.
        if self.ErrorDescription != "":
            ErrorOccurred = True

            for Description in ErrorCodeDescriptionMap:
                if all(
                    Text in self.ErrorDescription.lower()
                    for Text in Description.lower().split(" ")
                ):
                    Exceptions.append(
                        ExceptionErrorCodeMap[ErrorCodeDescriptionMap[Description]](
                            None
                        )
                    )
            # TODO make this faster...

        if ErrorOccurred:
            if len(Exceptions) > 0:
                raise ExceptionGroup("Hamilton step produced errors.", Exceptions)
            else:
                raise RuntimeError(
                    "No acceptable exception found for Hamilton error. See response data for more info."
                )
