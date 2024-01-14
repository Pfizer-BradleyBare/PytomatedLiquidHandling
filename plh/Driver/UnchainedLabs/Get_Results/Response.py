import dataclasses

from plh.driver.UnchainedLabs.backend import UnchainedLabsResponseBase


@dataclasses.dataclass(kw_only=True)
class Response(UnchainedLabsResponseBase):
    ResultsRaw: dataclasses.InitVar[str]
    Results: list[dict] = dataclasses.field(init=False)
    ResultsPath: str

    def __post_init__(self, StatusCodeRaw, ResultsRaw: str):
        super().__post_init__(StatusCodeRaw)

        ResultsRaw = ResultsRaw.replace("\r", "")
        self.Results = [
            dict(zip([Item.split(",") for Item in ResultsRaw.split("\n")[:1]][0], List))
            for List in [Item.split(",") for Item in ResultsRaw.split("\n")[1:]]
        ]
