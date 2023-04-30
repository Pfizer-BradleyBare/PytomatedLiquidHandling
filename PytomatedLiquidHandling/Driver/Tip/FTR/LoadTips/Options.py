from .....Tools.AbstractClasses import NonUniqueObjectABC


class AdvancedOptions:
    def __init__(self, *, MinimumTips: int | None = None):
        self.MinimumTips: int | None = MinimumTips


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        *,
        TipSequence: str,
        AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions(),
    ):
        self.TipSequence: str = TipSequence

        self.LoadingText: str = "Load FTR Tips"

        self.AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions(MinimumTips=0)
        # These are the default advanced values

        self.AdvancedOptionsInstance.__dict__.update(
            {k: v for k, v in vars(AdvancedOptionsInstance) if v is not None}
        )
        # This is used to update the values from the user if the user decided to change any advanced settings
