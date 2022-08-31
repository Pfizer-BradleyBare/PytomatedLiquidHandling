from Python.Modules.Transport import TransportConfigFileLoader, TransportTracker
from Python.Modules.DeckLocation import (
    DeckLocationConfigFileLoader,
    DeckLocationTracker,
)
from Python.Modules.Labware import LabwareConfigFileLoader, LabwareTracker
from Python.Modules.Layout import LayoutConfigFileLoader, LayoutTracker
from Python.Modules.Lid import LidConfigFileLoader, LidTracker
from Python.Modules.TempControlDevice import (
    TempControlDeviceConfigFileLoader,
    TempControlDeviceTracker,
)
from Python.Modules.Tip import TipConfigFileLoader, TipTracker
from Python.Modules.Pipette import PipetteConfigFileLoader, PipetteTracker
from Python.Modules.MagneticRack import (
    MagneticRackConfigFileLoader,
    MagneticRackTracker,
)
from Python.Modules.Notify import NotifyConfigFileLoader, NotifyTracker
from Python.Modules.FlipTube import FlipTubeConfigFileLoader, FlipTubeTracker


print("Testing Labware...")

Labwares = LabwareTracker()
LabwareConfigFileLoader.LoadYaml(
    Labwares,
    "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\HamiltonVisualMethodEditorConfiguration\\HAL\\Labware\\Labware.yaml",
)
for Labware in Labwares.GetLoadedObjectsAsList():
    print(Labware)

print("Success! \n\n")


print("Testing Transport...")

TransportDevices = TransportTracker(Labwares)
TransportConfigFileLoader.LoadYaml(
    TransportDevices,
    "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\HamiltonVisualMethodEditorConfiguration\\HAL\\Transport\\Transport.yaml",
)
for TransportDevice in TransportDevices.GetLoadedObjectsAsList():
    print(TransportDevice)

print("Success! \n\n")


print("Testing DeckLocation...")

DeckLocations = DeckLocationTracker(TransportDevices)
DeckLocationConfigFileLoader.LoadYaml(
    DeckLocations,
    "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\HamiltonVisualMethodEditorConfiguration\\HAL\\DeckLocation\\DeckLocation.yaml",
)
for Location in DeckLocations.GetLoadedObjectsAsList():
    print(Location)

print("Success! \n\n")


print("Testing Layout...")

LayoutItems = LayoutTracker(DeckLocations, Labwares)
LayoutConfigFileLoader.LoadYaml(
    LayoutItems,
    "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\HamiltonVisualMethodEditorConfiguration\\HAL\\Layout\\Layout.yaml",
)
for Layout in LayoutItems.GetLoadedObjectsAsList():
    print(Layout)

print("Success! \n\n")


print("Testing Lid...")

Lids = LidTracker(Labwares, DeckLocations)
LidConfigFileLoader.LoadYaml(
    Lids,
    "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\HamiltonVisualMethodEditorConfiguration\\HAL\\Lid\\Lid.yaml",
)
for Lid in Lids.GetLoadedObjectsAsList():
    print(Lid)

print("Success! \n\n")


print("Testing TempControlDevice...")

TempControlDevices = TempControlDeviceTracker(Labwares, DeckLocations)
TempControlDeviceConfigFileLoader.LoadYaml(
    TempControlDevices,
    "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\HamiltonVisualMethodEditorConfiguration\\HAL\\TempControlDevice\\TempControlDevice.yaml",
)
for TempControlDevice in TempControlDevices.GetLoadedObjectsAsList():
    print(TempControlDevice)

print("Success! \n\n")


print("Testing Tip...")

Tips = TipTracker()
TipConfigFileLoader.LoadYaml(
    Tips,
    "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\HamiltonVisualMethodEditorConfiguration\\HAL\\Tip\\Tip.yaml",
)
for Tip in Tips.GetLoadedObjectsAsList():
    print(Tip)

print("Success! \n\n")


print("Testing Pipette...")

Pipettes = PipetteTracker(Tips)
PipetteConfigFileLoader.LoadYaml(
    Pipettes,
    "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\HamiltonVisualMethodEditorConfiguration\\HAL\\Pipette\\Pipette.yaml",
)
for Pipette in Pipettes.GetLoadedObjectsAsList():
    print(Pipette)

print("Success! \n\n")


print("Testing Magnetic Rack...")

MagneticRacks = MagneticRackTracker(Labwares, DeckLocations, Pipettes, Tips)
MagneticRackConfigFileLoader.LoadYaml(
    MagneticRacks,
    "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\HamiltonVisualMethodEditorConfiguration\\HAL\\MagneticRack\\MagneticRack.yaml",
)
for MagneticRack in MagneticRacks.GetLoadedObjectsAsList():
    print(MagneticRack)

print("Success! \n\n")


print("Testing Notify...")

NotifyDevices = NotifyTracker()
NotifyConfigFileLoader.LoadYaml(
    NotifyDevices,
    "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\HamiltonVisualMethodEditorConfiguration\\HAL\\Notify\\Notify.yaml",
)
for NotifyDevice in NotifyDevices.GetLoadedObjectsAsList():
    print(NotifyDevice)

print("Success! \n\n")


print("Testing FlipTube...")

FlipTubes = FlipTubeTracker(Labwares)
FlipTubeConfigFileLoader.LoadYaml(
    FlipTubes,
    "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\HamiltonVisualMethodEditorConfiguration\\HAL\\FlipTube\\FlipTube.yaml",
)
for FlipTube in FlipTubes.GetLoadedObjectsAsList():
    print(FlipTube)

print("Success! \n\n")
