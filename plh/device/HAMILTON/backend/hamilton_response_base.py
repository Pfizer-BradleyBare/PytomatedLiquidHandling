from __future__ import annotations

import dataclasses
from enum import Enum

from plh.device.tools import ResponseBase

from .exceptions import error_code_description_map, error_code_map


class ButtonIDs(Enum):
    """The possible buttons that can be pressed by the user when backend error handling is true and an error occurs."""

    no_error = 0
    """No button was pressed."""

    abort = 1
    """Run aborted."""

    cancel = 2
    """Run canceled. Note: If programmed, the backend error handling was executed."""

    initialize = 3
    """Instrument initialized again."""

    repeat = 4
    """Command repeated."""

    exclude = 5
    """Channel or position excluded until the next tip pick up."""

    waste = 6
    """Tip ejected to the default waste."""

    air = 7
    """Rest of missing volume filled up with air."""

    bottom = 8
    """Aspiration repeated on container bottom."""

    continue_ = 9
    """Run continued without any change."""

    barcode = 10
    """Barcode assigned manually."""

    next = 11
    """Command repeated on next sequence position."""

    available = 12
    """Available volume used."""

    refill = 13
    """System reservoir of Nano Pipettor refilled."""


@dataclasses.dataclass(kw_only=True)
class HamiltonBlockData:
    """Channel grouping of block data."""

    num: int
    """Step dependant information (e.g. the channel number, a loading position etc.)."""

    main_err: int
    """Used to determine which exception to throw. See Exceptions to find the corresponding error codes."""

    slave_err: int
    """Slave error. Currently unused."""

    button_id: ButtonIDs
    """The button pressed by the user. See ButtonIDs enum which is an inner class."""

    step_data: int | float | str
    """Data associated with the step. Aspirated/dispensed volume, liquid height, barcode, etc."""

    labware_id: str
    """Labware ID to which block data applies."""

    position_id: str
    """Position ID to which block data applies."""


class ErrFlags(Enum):
    """Types of errors that can occur on the Hamilton."""

    no_error_with_block_data = 0
    """Step ends with ```OK```, no error occurred and no error handling was used. The block data contains the step-dependent information."""
    error_with_block_data = 1
    """Step ends with ```OK```, ```Abort``` or ```Cancel```. Error handling was necessary. The block data contains the step-dependent information.
    Note: The step data for this block are invalid if one of the following recoveries were used: Cancel, Abort, Continue, Exclude or Waste."""
    error_without_block_data = 2
    """Step ends with a fatal error. Caution: The block data part is invalid. Result values 4-n may have undefined data."""


@dataclasses.dataclass(kw_only=True)
class HamiltonBlockDataPackage:
    """General step result format of supported single steps."""

    err_flag: ErrFlags
    """Indicates whether an error occured or not and if block data is available. See ErrFlags enum which is an inner class."""

    block_data: list[HamiltonBlockData]
    """Contains BlockData if the ErrFlag indicates as such."""


@dataclasses.dataclass(kw_only=True)
class HamiltonResponseBase(ResponseBase):
    """Base class for all responses from Hamilton systems.
    - All ```HamiltonBlockData``` will be parsed and converted automatically if present as a response field.
    - If unhandled errors exists then an exception grouping of all unhandled errors that occrured will be raised.
    """

    error_id: int
    """Not used by captured for logging purposes"""
    error_vector_code: int
    """Not used by captured for logging purposes"""
    error_vector_major_id: int
    """Not used by captured for logging purposes"""
    error_vector_minor_id: int
    """Not used by captured for logging purposes"""

    error_description: str
    """There are, unfortunately, 2 cases here:
    - Case 1: Hamilton throws an error and the error is not handled by the user. Description is set, BlockData may or may not be available.
    We will use the description to throw the correct exception.
    - Case 2: Hamilton throws an error and the error is handled by the user. Description is not set, BlockData is available.
    We will use the MainErr to throw the correct exception."""

    @staticmethod
    def parse_block_data(block_data: str) -> HamiltonBlockDataPackage:
        if len(block_data) == 0:
            return HamiltonBlockDataPackage(
                err_flag=ErrFlags.error_without_block_data,
                block_data=[],
            )
        # NOTE: Not sure if this is required but putting it here for now.

        err_flag = int(block_data[:1])
        # ErrFlag is always the first digit

        block_data = block_data[1:]
        # Remove ErrFlag from string

        split_block_data = [i.split(",") for i in block_data.split("[")]
        # Split based on Hamilton special block separator then split based on data separator

        parsed_block_data = [
            HamiltonBlockData(
                num=int(data[0]),
                main_err=int(data[1]),
                slave_err=int(data[2]),
                button_id=ButtonIDs(int(data[3])),
                step_data=data[4],
                labware_id=data[5],
                position_id=data[6],
            )
            for data in split_block_data[1:]
        ]
        # Extract the block data

        return HamiltonBlockDataPackage(
            err_flag=ErrFlags(err_flag),
            block_data=sorted(parsed_block_data, key=lambda x: x.num),
        )

    # Only run on HamiltonBlockDataPackage types

    def __post_init__(self: HamiltonResponseBase) -> None:
        exceptions = []

        error_occurred = False

        for item in self.__dict__.values():
            if isinstance(item, HamiltonBlockDataPackage):
                error_occurred = error_occurred | item.err_flag.value

                if item.err_flag == ErrFlags.error_with_block_data:
                    exceptions += [
                        error_code_map[data.main_err](data)
                        for data in item.block_data
                        if data.button_id == ButtonIDs.cancel
                        and data.main_err in error_code_map
                    ]

        # This is the case where the Error does NOT have block data.
        if self.error_description != "":
            error_occurred = True

            for description in error_code_description_map:
                if all(
                    Text in self.error_description.lower()
                    for Text in description.lower().split(" ")
                ):
                    exceptions.append(
                        error_code_map[error_code_description_map[description]](
                            None,
                        ),
                    )
            # TODO make this faster...

        if error_occurred:
            if len(exceptions) > 0:
                msg = "Hamilton step produced errors."
                raise ExceptionGroup(msg, exceptions)

            msg = "No acceptable exception found for Hamilton error. See response data for more info."
            raise RuntimeError(msg)
