class Response:
    def __init__(
        self,
        State: bool,
        Message: str,
        Additional: dict[str, any],  # type:ignore
    ):
        self.State: bool = bool(State)
        self.Message: str = Message
        self.Additional: dict[str, any] = Additional  # type:ignore

    def GetState(self) -> bool:
        return self.State

    def GetMessage(self) -> str:
        return self.Message

    def GetAdditional(self) -> dict[str, any]:  # type: ignore
        return self.Additional
