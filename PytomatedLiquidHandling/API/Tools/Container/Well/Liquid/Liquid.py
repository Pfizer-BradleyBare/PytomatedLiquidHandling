from dataclasses import dataclass

from .Property import Properties


@dataclass
class Liquid:
    Name: str
    Volume: float
    Properties: Properties
