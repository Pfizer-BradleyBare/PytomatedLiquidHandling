from pydantic import field_validator

from ..Backend import UnchainedLabsResponseABC



class Response(UnchainedLabsResponseABC):
    Results: list[dict]
    ResultsPath: str

    @field_validator("Results",mode="before")
    def __ResultsValidate(cls,v):
        v = v.replace("\r","")
        return [dict(zip([Item.split(",") for Item in v.split("\n")[:1]][0], List)) for List in [Item.split(",") for Item in v.split("\n")[1:]] ]
