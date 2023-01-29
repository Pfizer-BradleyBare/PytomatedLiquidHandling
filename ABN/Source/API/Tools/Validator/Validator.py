def ValidateInput(
    Input: object,
    Types: list[type] = list(),
    Vals: list[object] = list(),
) -> bool:
    ValidState = True

    if not (Types or Vals):
        return True

    if Types:
        TestState = False
        if type(Input) in Types:
            TestState = True

        ValidState = ValidState and TestState

    if Vals:
        TestState = False
        if Input in Vals:
            TestState = True

        ValidState = ValidState and TestState

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


print(
    ValidateListInput(
        ["Bradley", "Hannah", 4],
        [int, str],
        ["Hannah", "Bradley", "Tipper", "Kuni", 1, 2, 3],
    )
)

print(type(1) == (int | float))
