from ...Tools.AbstractClasses import ServerHandlerABC, TrackerABC


class __HandlerRegistry__(TrackerABC[ServerHandlerABC]):
    pass


HandlerRegistry: __HandlerRegistry__ = __HandlerRegistry__()
