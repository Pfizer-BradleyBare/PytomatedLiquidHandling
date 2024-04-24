from __future__ import annotations

import dataclasses

from plh.device.UnchainedLabs_Instruments.backend import UnchainedLabsResponseBase


@dataclasses.dataclass(kw_only=True)
class Response(UnchainedLabsResponseBase):
    ResultsRaw: dataclasses.InitVar[str]
    Results: list[dict] = dataclasses.field(init=False)
    ResultsPath: str

    def __post_init__(
        self: Response,
        status_code_raw: int | tuple,
        results_raw: str,
    ) -> None:
        super().__post_init__(status_code_raw)

        results_raw = results_raw.replace("\r", "")
        self.Results = [
            dict(
                zip([Item.split(",") for Item in results_raw.split("\n")[:1]][0], List),
            )
            for List in [Item.split(",") for Item in results_raw.split("\n")[1:]]
        ]
