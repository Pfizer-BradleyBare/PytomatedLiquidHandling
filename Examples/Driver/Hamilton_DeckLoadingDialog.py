import os

from PytomatedLiquidHandling.Driver.Hamilton.Backend import MicrolabStarBackend
from PytomatedLiquidHandling.Driver.Hamilton.DeckLoadingDialog import Carrier5Position

Backend = MicrolabStarBackend(
    "Example Star",
    os.path.join(os.path.dirname(__file__), "Layout", "Example.lay"),
)
Backend.StartBackend()
# Creates the Backend so we can communicate with the Hamilton

ListedOptions = Carrier5Position.ListedOptions(
    Carrier3DImage=Carrier5Position.ListedOptions.Carrier3DImageOptions.Carrier5PositionPlate3D,
    Carrier2DImage=Carrier5Position.ListedOptions.Carrier2DImageOptions.Carrier5PositionPlate2D,
)
ListedOptions.append(
    Carrier5Position.Options(
        CarrierPosition=1,
        LabwareImage=Carrier5Position.Options.LabwareImageOptions.PlateThermo1200uL96Well,
        LabwareSupportingText="Hello!",
    )
)
ListedOptions.append(
    Carrier5Position.Options(
        CarrierPosition=4,
        LabwareImage=Carrier5Position.Options.LabwareImageOptions.PlateBiorad200uL96Well,
        LabwareSupportingText="Hello!",
    )
)
CommandInstance = Carrier5Position.Command(
    CustomErrorHandling=False, ListedOptions=ListedOptions
)

Backend.ExecuteCommand(CommandInstance)
Backend.WaitForResponseBlocking(CommandInstance)

# Show dialog
