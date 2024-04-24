from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, Literal

from pydantic import dataclasses


class LayoutSorting(Enum):
    """How the positions of a labware are sorted in the automation software."""

    Columnwise = "Columnwise"
    """Positions procede top-down then left-right."""

    Rowwise = "Rowwise"
    """Positions procede left-right then top-down."""


@dataclasses.dataclass(kw_only=True)
class Layout(ABC):
    """Full description of a labware position layout."""

    rows: int
    """Number of rows in the labware."""

    columns: int
    """Number of columns in the labware."""

    direction: LayoutSorting
    """Sorting object."""

    def total_positions(self: Layout) -> int:
        """Total positions = rows * columns"""
        return self.rows * self.columns

    def get_position_id(self: Layout, position: str | int) -> str:
        """Dependent on sorting object the correct position id will be returned given a str or an integer. Position ID returned depends on layout subclass (Numeric vs Alphanumeric)."""
        if isinstance(position, int):
            position = str(position)

        fail = True
        if (
            position.isalnum() and not position.isalpha() and not position.isdigit()
        ) or position.isdigit():
            fail = False

        if fail is True:
            msg = "position can be either alphanumeric or numeric.\nAlphanumeric must contain both numbers and letters. Ex: A1, B12, 10H.\nNumeric must only contain digits. Ex: 1 13 95"
            raise ValueError(msg)

        if self.direction == LayoutSorting.Columnwise:
            return self._get_columnwise_position_id(position)

        return self._get_rowwise_position_id(position)

    @abstractmethod
    def sort_positions(
        self: Layout,
        positions: list[str | int],
        key: Callable = lambda x: x,
    ) -> list[str]:
        """Simply sorts positions according to sorting object."""
        ...

    @abstractmethod
    def group_positions_columnwise(
        self: Layout,
        positions: list[str | int],
        key: Callable = lambda x: x,
    ) -> list[list[str]]:
        """Groups positions according to sorting object. Each columnwise group will be a separate list."""
        ...

    @abstractmethod
    def group_positions_rowwise(
        self: Layout,
        positions: list[str | int],
        key: Callable = lambda x: x,
    ) -> list[list[str]]:
        """Groups positions according to sorting object. Each rowwise group will be a separate list."""
        ...

    @abstractmethod
    def _get_columnwise_position_id(self: Layout, position: str) -> str:
        ...

    @abstractmethod
    def _get_rowwise_position_id(self: Layout, position: str) -> str:
        ...


@dataclasses.dataclass(kw_only=True)
class NumericLayout(Layout):
    """A numeric representation of a container layout."""

    type: Literal["Numeric"] = "Numeric"
    """Pydantic requirement. Never used except for input validation."""

    def sort_positions(self: NumericLayout, positions: list[str | int]) -> list[str]:
        """Sorts by number."""
        return [
            str(pos)
            for pos in sorted([int(self.get_position_id(pos)) for pos in positions])
        ]

    def group_positions_columnwise(
        self: NumericLayout,
        positions: list[str | int],
    ) -> list[list[str]]:
        """Groups positions according to sorting object. Each columnwise group will be a separate list."""
        sorted_positions = self.sort_positions(positions)

        groups = [[] for _ in range(self.columns)]
        for pos in sorted_positions:
            groups[int((int(pos) - 1) / self.rows)].append(pos)

        return [Group for Group in groups if len(Group) != 0]

    def group_positions_rowwise(
        self: NumericLayout,
        positions: list[str | int],
    ) -> list[list[str]]:
        """Groups positions according to sorting object. Each rowwise group will be a separate list."""
        sorted_positions = self.sort_positions(positions)

        groups = [[] for _ in range(self.rows)]
        for pos in sorted_positions:
            groups[int((int(pos) - 1) / self.columns)].append(pos)

        return [Group for Group in groups if len(Group) != 0]

    def _get_columnwise_position_id(self: NumericLayout, position: str) -> str:
        if position.isnumeric():
            return position

        number_portion = "".join([c for c in position if c.isdigit()])
        character_portion = "".join([c for c in position if c.isalpha()])

        pos = (int(number_portion) - 1) * self.rows

        pos += ord(character_portion) + 1 - 65  # ascii A

        return str(pos)

    def _get_rowwise_position_id(self: NumericLayout, position: str) -> str:
        if position.isnumeric():
            return position

        number_portion = "".join([c for c in position if c.isdigit()])
        character_portion = "".join([c for c in position if c.isalpha()])

        pos = int(number_portion)

        pos += (ord(character_portion) - 65) * self.columns  # ascii A

        return str(pos)


@dataclasses.dataclass(kw_only=True)
class AlphanumericLayout(Layout):
    """An Alphanumeric representation of a container layout."""

    type: Literal["Alphanumeric"] = "Alphanumeric"
    """Pydantic requirement. Never used except for input validation."""

    def sort_positions(
        self: AlphanumericLayout,
        positions: list[str | int],
    ) -> list[str]:
        """Converts alphanumeric id to number, sorts by number, then converts back to alphanumeric."""
        numeric_addressing = NumericLayout(
            rows=self.rows,
            columns=self.columns,
            direction=self.direction,
        )

        return [
            self.get_position_id(pos)
            for pos in numeric_addressing.sort_positions(positions)
        ]

    def group_positions_columnwise(
        self: AlphanumericLayout,
        positions: list[str | int],
    ) -> list[list[str]]:
        """Uses numeric addressing to group positions then converts back to alphanumeric."""
        numeric_addressing = NumericLayout(
            rows=self.rows,
            columns=self.columns,
            direction=self.direction,
        )

        return [
            [self.get_position_id(pos) for pos in Group]
            for Group in numeric_addressing.group_positions_columnwise(positions)
        ]

    def group_positions_rowwise(
        self: AlphanumericLayout,
        positions: list[str | int],
    ) -> list[list[str]]:
        """Uses numeric addressing to group positions then converts back to alphanumeric."""
        numeric_addressing = NumericLayout(
            rows=self.rows,
            columns=self.columns,
            direction=self.direction,
        )

        return [
            [self.get_position_id(pos) for pos in Group]
            for Group in numeric_addressing.group_positions_rowwise(positions)
        ]

    def _get_columnwise_position_id(self: AlphanumericLayout, position: str) -> str:
        if position.isalnum() and not position.isalpha() and not position.isdigit():
            return position

        pos = int(position)

        number_portion = str(((pos - 1) // self.rows) + 1)

        character_portion = chr(((pos - 1) % self.rows) + 65)

        return character_portion + number_portion

    def _get_rowwise_position_id(self: AlphanumericLayout, position: str) -> str:
        if position.isalnum() and not position.isalpha() and not position.isdigit():
            return position

        pos = int(position)

        number_portion = str(pos % self.columns)

        character_portion = chr((pos // self.columns) + 65)

        return character_portion + number_portion
