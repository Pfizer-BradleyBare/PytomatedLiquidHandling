from dataclasses import dataclass

from .Properties import Properties


@dataclass
class Liquid:
    Name: str
    Volume: float
    Properties: Properties
