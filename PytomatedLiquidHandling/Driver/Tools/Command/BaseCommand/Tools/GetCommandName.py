import os


def GetCommandName(__file__: str) -> str:
    """Uses the path of the python module to extract a command name

    Args:
        __file__ (str): The path of the python module

    Returns:
        str: Command name
    """
    return os.path.basename(os.path.dirname(__file__))
