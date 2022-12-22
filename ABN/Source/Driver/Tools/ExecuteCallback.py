from typing import Callable

from . import Command


def ExecuteCallback(
    CallbackFunction: Callable[[Command, tuple], None] | None,
    CommandInstance: Command,
    CallbackArgs: tuple,
):
    if CallbackFunction is not None:
        CallbackFunction(CommandInstance, CallbackArgs)
