from ABN.Source.HAL.Transport import TransportLoader, TransportTracker
from ABN.Source.HAL.DeckLocation import (
    DeckLocationLoader,
    DeckLocationTracker,
)
from ABN.Source.HAL.Labware import LabwareLoader, LabwareTracker
from ABN.Source.HAL.Layout import LayoutLoader, LayoutTracker
from ABN.Source.HAL.Lid import LidLoader, LidTracker
from ABN.Source.HAL.TempControlDevice import (
    TempControlDeviceLoader,
    TempControlDeviceTracker,
)
from ABN.Source.HAL.Tip import TipLoader, TipTracker
from ABN.Source.HAL.Pipette import PipetteLoader, PipetteTracker
from ABN.Source.HAL.MagneticRack import (
    MagneticRackLoader,
    MagneticRackTracker,
)
from ABN.Source.HAL.Notify import NotifyLoader, NotifyTracker
from ABN.Source.HAL.FlipTube import FlipTubeLoader, FlipTubeTracker


print("Testing Labware...")

Labwares = LabwareTracker()
LabwareLoader.LoadYaml(
    Labwares,
    "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\ABN\\HamiltonVisualMethodEditorConfiguration\\HAL\\Labware\\Labware.yaml",
)
for Labware in Labwares.GetLoadedObjectsAsList():
    print(Labware)

print("Success! \n\n")


print("Testing Transport...")

TransportDevices = TransportTracker(Labwares)
TransportLoader.LoadYaml(
    TransportDevices,
    "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\ABN\\HamiltonVisualMethodEditorConfiguration\\HAL\\Transport\\Transport.yaml",
)
for TransportDevice in TransportDevices.GetLoadedObjectsAsList():
    print(TransportDevice)

print("Success! \n\n")


print("Testing DeckLocation...")

DeckLocations = DeckLocationTracker(TransportDevices)
DeckLocationLoader.LoadYaml(
    DeckLocations,
    "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\ABN\\HamiltonVisualMethodEditorConfiguration\\HAL\\DeckLocation\\DeckLocation.yaml",
)
for Location in DeckLocations.GetLoadedObjectsAsList():
    print(Location)

print("Success! \n\n")


print("Testing Layout...")

LayoutItems = LayoutTracker(DeckLocations, Labwares)
LayoutLoader.LoadYaml(
    LayoutItems,
    "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\ABN\\HamiltonVisualMethodEditorConfiguration\\HAL\\Layout\\Layout.yaml",
)
for Layout in LayoutItems.GetLoadedObjectsAsList():
    print(Layout)

print("Success! \n\n")


print("Testing Lid...")

Lids = LidTracker(Labwares, DeckLocations)
LidLoader.LoadYaml(
    Lids,
    "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\ABN\\HamiltonVisualMethodEditorConfiguration\\HAL\\Lid\\Lid.yaml",
)
for Lid in Lids.GetLoadedObjectsAsList():
    print(Lid)

print("Success! \n\n")


print("Testing TempControlDevice...")

TempControlDevices = TempControlDeviceTracker(Labwares, DeckLocations)
TempControlDeviceLoader.LoadYaml(
    TempControlDevices,
    "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\ABN\\HamiltonVisualMethodEditorConfiguration\\HAL\\TempControlDevice\\TempControlDevice.yaml",
)
for TempControlDevice in TempControlDevices.GetLoadedObjectsAsList():
    print(TempControlDevice)

print("Success! \n\n")


print("Testing Tip...")

Tips = TipTracker()
TipLoader.LoadYaml(
    Tips,
    "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\ABN\\HamiltonVisualMethodEditorConfiguration\\HAL\\Tip\\Tip.yaml",
)
for Tip in Tips.GetLoadedObjectsAsList():
    print(Tip)

print("Success! \n\n")


print("Testing Pipette...")

Pipettes = PipetteTracker(Tips)
PipetteLoader.LoadYaml(
    Pipettes,
    "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\ABN\\HamiltonVisualMethodEditorConfiguration\\HAL\\Pipette\\Pipette.yaml",
)
for Pipette in Pipettes.GetLoadedObjectsAsList():
    print(Pipette)

print("Success! \n\n")


print("Testing Magnetic Rack...")

MagneticRacks = MagneticRackTracker(Labwares, DeckLocations, Pipettes, Tips)
MagneticRackLoader.LoadYaml(
    MagneticRacks,
    "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\ABN\\HamiltonVisualMethodEditorConfiguration\\HAL\\MagneticRack\\MagneticRack.yaml",
)
for MagneticRack in MagneticRacks.GetLoadedObjectsAsList():
    print(MagneticRack)

print("Success! \n\n")


print("Testing Notify...")

NotifyDevices = NotifyTracker()
NotifyLoader.LoadYaml(
    NotifyDevices,
    "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\ABN\\HamiltonVisualMethodEditorConfiguration\\HAL\\Notify\\Notify.yaml",
)
for NotifyDevice in NotifyDevices.GetLoadedObjectsAsList():
    print(NotifyDevice)

print("Success! \n\n")


print("Testing FlipTube...")

FlipTubes = FlipTubeTracker(Labwares)
FlipTubeLoader.LoadYaml(
    FlipTubes,
    "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\ABN\\HamiltonVisualMethodEditorConfiguration\\HAL\\FlipTube\\FlipTube.yaml",
)
for FlipTube in FlipTubes.GetLoadedObjectsAsList():
    print(FlipTube)

print("Success! \n\n")
