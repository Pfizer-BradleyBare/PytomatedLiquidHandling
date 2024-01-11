import dataclasses

from ..Backend import UnchainedLabsResponseABC


@dataclasses.dataclass(kw_only=True)
class Response(UnchainedLabsResponseABC):
    ResultsRaw: dataclasses.InitVar[str]
    ResultsParsed: list[dict] = dataclasses.field(init=False)
    ResultsPath: str

    def __post_init__(self, StatusCodeRaw, ResultsRaw: str):
        super().__post_init__(StatusCodeRaw)

        ResultsRaw = ResultsRaw.replace("\r", "")
        self.ResultsParsed = [
            dict(zip([Item.split(",") for Item in ResultsRaw.split("\n")[:1]][0], List))
            for List in [Item.split(",") for Item in ResultsRaw.split("\n")[1:]]
        ]
