import yaml
from .BackendTracker import BackendTracker
from ...Driver.Hamilton.Backend import VantageBackend, MicrolabStarBackend


def LoadYaml(FilePath: str) -> BackendTracker:
    ...
