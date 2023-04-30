from .....Tools.AbstractClasses import NonUniqueObjectABC


class AdvancedOptions:
    def __init__(self):
        ...


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        *,
        TipSequence: str,
        NumPositions: int,
        AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions(),
    ):
        self.TipSequence: str = TipSequence
        self.NumPositions: int = NumPositions

        self.AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions()
        # These are the default advanced values

        self.AdvancedOptionsInstance.__dict__.update(
            {k: v for k, v in vars(AdvancedOptionsInstance) if v is not None}
        )
        # This is used to update the values from the user if the user decided to change any advanced settings
