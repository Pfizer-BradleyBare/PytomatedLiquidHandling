class Response:
    def __init__(self, State: bool, Message: str, Extra: dict[str, any]):  # type:ignore
        self.State: bool = State
        self.Message: str = Message
        self.Extra: dict[str, any] = Extra  # type:ignore

    def GetState(self) -> bool:
        return self.State

    def GetMessage(self) -> str:
        return self.Message

    def GetExtra(self) -> dict[str, any]:  # type: ignore
        return self.Extra
