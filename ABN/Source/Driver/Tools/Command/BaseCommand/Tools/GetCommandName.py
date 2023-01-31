import os


def GetCommandName(__file__: str) -> str:
    return os.path.basename(os.path.dirname(__file__))
