from ....AbstractClasses.Object import ObjectABC
from abc import abstractmethod
from ...Workbook.Block import Block
from ...Workbook.Solution import Solution
from enum import Enum


class ContainerTypes(Enum):
    Plate = "Plate"
    Reagent = "Reagent"


class Container(ObjectABC):
    def __init__(self, Name: str, Type: ContainerTypes, SolutionInstance: Solution):
        self.Name: str = Name
        self.Type: ContainerTypes = Type
        self.SolutionInstance: Solution = SolutionInstance

        # Block Instances: These are the blocks that have used this container. Either for aspirate or dispense.
        self.AspirateBlockInstances: list[Block] = list()
        self.DispenseBlockInstances: list[Block] = list()

    def GetName(self) -> str:
        return self.Name

    def GetType(self) -> ContainerTypes:
        return self.Type

    def GetAspirateBlockInstances(self) -> list[Block]:
        return self.AspirateBlockInstances

    def GetDispenseBlockInstances(self) -> list[Block]:
        return self.DispenseBlockInstances
