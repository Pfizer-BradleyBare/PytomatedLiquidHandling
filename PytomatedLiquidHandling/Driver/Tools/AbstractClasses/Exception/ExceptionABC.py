from ...AbstractClasses import CommandABC


class ExceptionABC(Exception):
    def __init__(
        self, CommandInstance: CommandABC, ResponseInstance: CommandABC.Response
    ):
        ExceptionMessage = ""
        ExceptionMessage += CommandInstance.ModuleName
        ExceptionMessage += ": "
        ExceptionMessage += CommandInstance.CommandName
        ExceptionMessage += "-> "
        ExceptionMessage += ResponseInstance.GetDetails()
        Exception.__init__(self, ExceptionMessage)
