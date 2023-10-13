from typing import Callable


def ExceptionToBool(ValidationFunction: Callable, *args) -> bool:
    try:
        ValidationFunction(*args)
        return True
    except:
        return False
