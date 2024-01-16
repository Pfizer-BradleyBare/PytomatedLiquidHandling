from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable

from pydantic import dataclasses


class InvalidpositionError(ValueError):
    ...


class LayoutSorting(Enum):
    Columnwise = "Columnwise"
    Rowwise = "Rowwise"


@dataclasses.dataclass(kw_only=True)
class Layout(ABC):
    rows: int
    columns: int
    direction: LayoutSorting

    def get_position_id(self: Layout, position: str | int) -> str:
        if isinstance(position, int):
            position = str(position)

        fail = False
        if (
            not position.isalnum() and position.isalpha() and position.isdigit()
        ) or not position.isdigit():
            fail = True

        if fail is True:
            msg = "position can be either alphanumeric or numeric.\nAlphanumeric must contain both numbers and letters. Ex: A1, B12, 10H.\nNumeric must only contain digits. Ex: 1 13 95"
            raise InvalidpositionError(msg)

        if self.direction == LayoutSorting.Columnwise:
            return self._get_columnwise_position_id(position)

        return self._get_rowwise_position_id(position)

    @abstractmethod
    def sort_positions(
        self: Layout,
        positions: list[str | int],
        key: Callable = lambda x: x,
    ) -> list[str]:
        ...

    @abstractmethod
    def group_positions_columnwise(
        self: Layout,
        positions: list[str | int],
        key: Callable = lambda x: x,
    ) -> list[list[str]]:
        ...

    @abstractmethod
    def group_positions_rowwise(
        self: Layout,
        positions: list[str | int],
        key: Callable = lambda x: x,
    ) -> list[list[str]]:
        ...

    @abstractmethod
    def _get_columnwise_position_id(self: Layout, position: str) -> str:
        ...

    @abstractmethod
    def _get_rowwise_position_id(self: Layout, position: str) -> str:
        ...


@dataclasses.dataclass(kw_only=True)
class NumericLayout(Layout):
    def sort_positions(self: NumericLayout, positions: list[str | int]) -> list[str]:
        return sorted([self.get_position_id(pos) for pos in positions])

    def group_positions_columnwise(
        self: NumericLayout,
        positions: list[str | int],
    ) -> list[list[str]]:
        sorted_positions = self.sort_positions(positions)

        groups = [[] for _ in range(self.columns)]
        for pos in sorted_positions:
            groups[int((int(pos) - 1) / self.rows)].append(pos)

        return [Group for Group in groups if len(Group) != 0]

    def group_positions_rowwise(
        self: NumericLayout,
        positions: list[str | int],
    ) -> list[list[str]]:
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
class AlphaNumericLayout(Layout):
    def sort_positions(
        self: AlphaNumericLayout,
        positions: list[str | int],
    ) -> list[str]:
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
        self: AlphaNumericLayout,
        positions: list[str | int],
    ) -> list[list[str]]:
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
        self: AlphaNumericLayout,
        positions: list[str | int],
    ) -> list[list[str]]:
        numeric_addressing = NumericLayout(
            rows=self.rows,
            columns=self.columns,
            direction=self.direction,
        )

        return [
            [self.get_position_id(pos) for pos in Group]
            for Group in numeric_addressing.group_positions_rowwise(positions)
        ]

    def _get_columnwise_position_id(self: AlphaNumericLayout, position: str) -> str:
        if position.isalnum() and not position.isalpha() and not position.isdigit():
            return position

        pos = int(position)

        number_portion = str(((pos - 1) // self.rows) + 1)

        character_portion = chr(((pos - 1) % self.rows) + 65)

        return character_portion + number_portion

    def _get_rowwise_position_id(self: AlphaNumericLayout, position: str) -> str:
        if position.isalnum() and not position.isalpha() and not position.isdigit():
            return position

        pos = int(position)

        number_portion = str(pos % self.columns)

        character_portion = chr((pos // self.columns) + 65)

        return character_portion + number_portion
