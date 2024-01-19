from types import UnionType


def ValidateInput(
    Input: object,
    Types: type | UnionType,
    Vals: list[object] = [],
) -> bool:
    ValidState = True

    if not (Types or Vals):
        return True

    if Types:
        TestState = False
        if isinstance(Input, Types):
            TestState = True

        ValidState = ValidState and TestState

    if ValidState is False:
        return False
    # If we already failed we can return. No sense in continuing

    if Vals:
        TestState = False
        if Input in Vals:
            TestState = True

        ValidState = ValidState and TestState

    return ValidState


def ValidateListInput(
    Inputs: list[object],
    Types: type | UnionType,
    Vals: list[object] = [],
) -> bool:
    if not (Types or Vals):
        return True

    ValidState = True

    for Input in Inputs:
        ValidState = ValidState and ValidateInput(Input, Types, Vals)

        if ValidState is False:
            return False
        # If we already failed we can return. No sense in continuing

    return ValidState


print(
    ValidateListInput(
        ["Bradley", "Hannah", 3],
        int | str,
        ["Hannah", "Bradley", "Tipper", "Kuni", 1, 2, 3],
    ),
)
