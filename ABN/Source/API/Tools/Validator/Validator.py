def ValidateInput(
    Input: object,
    Types: list[type] = list(),
    Vals: list[object] = list(),
) -> bool:
    ValidState = False

    if not (Types or Vals):
        return True

    if Types:
        TestState = False
        for Type in Types:
            if type(Input) == Type:
                TestState = True
                break

        ValidState = ValidState or TestState

    if Vals:
        TestState = False
        for Val in Vals:
            if Input == Val:
                TestState = True
                break

        ValidState = ValidState or TestState

    return ValidState


def ValidateListInput(
    Inputs: list[object],
    Types: list[type] = list(),
    Vals: list[object] = list(),
) -> bool:

    if not (Types or Vals):
        return True

    ValidState = True

    for Input in Inputs:
        ValidState = ValidState and ValidateInput(Input, Types, Vals)

    return ValidState
