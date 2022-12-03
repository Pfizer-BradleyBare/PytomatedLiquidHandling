Data = "-100[01,00,00,0, 0.0,washstation_1_standardneedle_0001,1[02,00,00,0, 0.0,washstation_1_standardneedle_0002,2[03,00,00,0, 0.0,washstation_1_standardneedle_0003,3[04,00,00,0, 0.0,washstation_1_standardneedle_0004,4[05,00,00,0, 0.0,washstation_1_standardneedle_0001,5[06,00,00,0, 0.0,washstation_1_standardneedle_0001,6[07,00,00,0, 0.0,washstation_1_standardneedle_0001,7[08,00,00,0, 0.0,washstation_1_standardneedle_0001,8"


def ConvertToArrays(StepReturn: str):
    return [Item.split(",") for Item in StepReturn.split("[")]


def GetErrorCode(StepReturn: str):
    return ConvertToArrays(StepReturn)[0][0]


def GetNumberOfPositions(StepReturn: str):
    return StepReturn.count("[")


def GetPosition(StepReturn: str, Position: int):
    if GetNumberOfPositions(StepReturn) != 0:
        return ConvertToArrays(StepReturn)[Position][0]


def GetMainError(StepReturn: str, Position: int):
    if GetNumberOfPositions(StepReturn) != 0:
        return ConvertToArrays(StepReturn)[Position][1]


def GetSlaveError(StepReturn: str, Position: int):
    if GetNumberOfPositions(StepReturn) != 0:
        return ConvertToArrays(StepReturn)[Position][2]


def GetRecoveryButton(StepReturn: str, Position: int):
    if GetNumberOfPositions(StepReturn) != 0:
        return ConvertToArrays(StepReturn)[Position][3]


def GetBarcode(StepReturn: str, Position: int):
    if GetNumberOfPositions(StepReturn) != 0:
        return ConvertToArrays(StepReturn)[Position][4]


def GetBarcodeMask(StepReturn: str, Position: int):
    if GetNumberOfPositions(StepReturn) != 0:
        return ConvertToArrays(StepReturn)[Position][1]


def GetBarcodePosition(StepReturn: str, Position: int):
    if GetNumberOfPositions(StepReturn) != 0:
        return ConvertToArrays(StepReturn)[Position][1]


def GetLastLiquidLevel(StepReturn: str, Position: int):
    if GetNumberOfPositions(StepReturn) != 0:
        return ConvertToArrays(StepReturn)[Position][4]


def GetLabwareID(StepReturn: str, Position: int):
    if GetNumberOfPositions(StepReturn) != 0:
        return ConvertToArrays(StepReturn)[Position][5]


def GetPositionID(StepReturn: str, Position: int):
    if GetNumberOfPositions(StepReturn) != 0:
        return ConvertToArrays(StepReturn)[Position][6]


print(GetLabwareID(Data, 3))
