class Response:
    def __init__(
        self,
        State: bool,
        ErrorDescription: str,
        Additional: dict[str, any],  # type:ignore
    ):
        self.State: bool = bool(State)
        self.ErrorDescription: str = ErrorDescription
        self.Additional: dict[str, any] = Additional  # type:ignore

    def GetState(self) -> bool:
        return self.State

    def GetErrorDescription(self) -> str:
        return self.ErrorDescription

    def GetAdditional(self) -> dict[str, any]:  # type: ignore
        return self.Additional


def ClampMax(Number, Max):
    while Number > Max:
        Number -= Max

    return Number


c = 7
s = 3

print(ClampMax(c, s))
