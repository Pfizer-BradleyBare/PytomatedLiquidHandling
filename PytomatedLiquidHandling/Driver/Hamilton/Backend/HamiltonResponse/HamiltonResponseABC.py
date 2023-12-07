from enum import Enum
from typing import Any, Literal, cast

from pydantic import BaseModel, ValidationInfo, field_validator

from PytomatedLiquidHandling.Driver.Tools.BaseClasses import ResponseABC

from ..Exceptions import ErrorCodeDescriptionMap, ExceptionErrorCodeMap


class HamiltonBlockData(BaseModel):
    """
    Num = Step depended information (e.g. the channel number, a loading position etc.).
    MainErr = Used to determine which exception to throw. See Exceptions to find the corresponding error codes
    SlaveErr = Slave error. Currently unused
    ButtonID = The button pressed by the user. See ButtonIDs enum which is an inner class
    LabwareIDs: list[str]
    PositionIDs: list[str]
    """

    class ButtonIDs(Enum):
        """
        NoError = No button was pressed.

        Abort = Run aborted.

        Cancel = Run canceled. Note: If programmed, the user-defined error handling was executed.

        Initialize = Instrument initialized again.

        Repeat = Command repeated.

        Exclude = Channel or position excluded until the next tip pick up.

        Waste = Tip ejected to the default waste.

        Air = Rest of missing volume filled up with air.

        Bottom = Aspiration repeated on container bottom.

        Continue = Run continued without any change.

        Barcode = Barcode assigned manually.

        Next = Command repeated on next sequence position.

        Available = Available volume used.

        Refill = System reservoir of Nano Pipettor refilled.
        """

        NoError = 0
        Abort = 1
        Cancel = 2
        Initialize = 3
        Repeat = 4
        Exclude = 5
        Waste = 6
        Air = 7
        Bottom = 8
        Continue = 9
        Barcode = 10
        Next = 11
        Available = 12
        Refill = 13

    Num: int
    MainErr: int
    SlaveErr: int
    ButtonID: ButtonIDs
    StepData: int | float | str
    LabwareID: str
    PositionID: str


class HamiltonBlockDataPackage(BaseModel):
    """
    ErrFlag = Indicates whether an error occured or not and if block data is available. See ErrFlags enum which is an inner class
    BlockData = Contains BlockData if the ErrFlag indicates as such
    """

    class ErrFlags(Enum):
        """
        NoErrorWithBlockData = Step ends with OK, no error occurred and no error handling was used. The block data contains the step-dependent information.

        ErrorWithBlockData = Step ends with OK, Abort or Cancel. Error handling was necessary. The block data contains the step-dependent information. Note: The step data for this block are invalid if one of the following recoveries were used: Cancel, Abort, Continue, Exclude or Waste.

        ErrorWithoutBlockData = Step ends with a fatal error. Caution: The block data part is invalid. Result values 4-n may have undefined data.
        """

        NoErrorWithBlockData = 0  # Step ends with OK, no error occurred and no error handling was used. The block data contains the step-dependent information.
        ErrorWithBlockData = 1  # Step ends with OK, Abort or Cancel. Error handling was necessary. The block data contains the step-dependent information. Note: The step data for this block are invalid if one of the following recoveries were used: Cancel, Abort, Continue, Exclude or Waste.
        ErrorWithoutBlockData = 2  # Step ends with a fatal error. Caution: The block data part is invalid. Result values 4-n may have undefined data.

    ErrFlag: ErrFlags
    BlockData: list[HamiltonBlockData]


class HamiltonResponseABC(ResponseABC):
    ErrorDescription: str | Literal[""]
    # There are, unfortunately, 2 cases here:
    # Case 1: Hamilton throws an error and the error is not handled by the user. Description is set, BlockData may or may not be available.
    # We will use the description to throw the correct exception.
    # Case 2: Hamilton throws an error and the error is handled by the user. Description is not set, BlockData is available.
    # We will use the MainErr to throw the correct exception.

    @field_validator("*", mode="before")
    # NOTE: This will attempt to validate all data but will only validate HamiltonBlockDataPackage types internally
    def __HamiltonBlockDataValidate(cls, v, Info: ValidationInfo):
        if cls.model_fields[
            cast(str, Info.field_name)
        ].annotation == HamiltonBlockDataPackage and not isinstance(
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

    def model_post_init(self, __context: Any) -> None:
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

        # This is the cae where the Error does NOT have block data.
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
