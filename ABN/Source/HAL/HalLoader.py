from .DeckLocation import (
    DeckLocationLoader,
    DeckLocationTracker,
)
from .FlipTube import FlipTubeLoader, FlipTubeTracker
from .Labware import LabwareLoader, LabwareTracker
from .Layout import LayoutLoader, LayoutTracker
from .Lid import LidLoader, LidTracker
from .MagneticRack import (
    MagneticRackLoader,
    MagneticRackTracker,
)
from .Notify import NotifyLoader, NotifyTracker
from .Pipette import PipetteLoader, PipetteTracker
from .TempControlDevice import (
    TempControlDeviceLoader,
    TempControlDeviceTracker,
)
from .Tip import TipLoader, TipTracker
from .Transport import TransportLoader, TransportTracker
from .Hal import Hal


def Load(HalInstance: Hal):
    print("Loading Labware...")

    Labwares = LabwareTracker()
    LabwareLoader.LoadYaml(
        Labwares,
        "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\ABN\\HamiltonVisualMethodEditorConfiguration\\HAL\\Labware\\Labware.yaml",
    )
    HalInstance.LabwareTrackerInstance = Labwares
    for Labware in Labwares.GetLoadedObjectsAsList():
        print(Labware)

    print("Success! \n\n")

    print("Loading Transport...")

    TransportDevices = TransportTracker(Labwares)
    TransportLoader.LoadYaml(
        TransportDevices,
        "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\ABN\\HamiltonVisualMethodEditorConfiguration\\HAL\\Transport\\Transport.yaml",
    )
    HalInstance.TransportTrackerInstance = TransportDevices
    for TransportDevice in TransportDevices.GetLoadedObjectsAsList():
        print(TransportDevice)

    print("Success! \n\n")

    print("Loading DeckLocation...")

    DeckLocations = DeckLocationTracker(TransportDevices)
    DeckLocationLoader.LoadYaml(
        DeckLocations,
        "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\ABN\\HamiltonVisualMethodEditorConfiguration\\HAL\\DeckLocation\\DeckLocation.yaml",
    )
    HalInstance.DeckLocationTrackerInstance = DeckLocations
    for Location in DeckLocations.GetLoadedObjectsAsList():
        print(Location)

    print("Success! \n\n")

    print("Loading Layout...")

    LayoutItems = LayoutTracker(DeckLocations, Labwares)
    LayoutLoader.LoadYaml(
        LayoutItems,
        "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\ABN\\HamiltonVisualMethodEditorConfiguration\\HAL\\Layout\\Layout.yaml",
    )
    HalInstance.LayoutTrackerInstance = LayoutItems
    for Layout in LayoutItems.GetLoadedObjectsAsList():
        print(Layout)

    print("Success! \n\n")

    print("Loading Lid...")

    Lids = LidTracker(Labwares, DeckLocations)
    LidLoader.LoadYaml(
        Lids,
        "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\ABN\\HamiltonVisualMethodEditorConfiguration\\HAL\\Lid\\Lid.yaml",
    )
    HalInstance.LidTrackerInstance = Lids
    for Lid in Lids.GetLoadedObjectsAsList():
        print(Lid)

    print("Success! \n\n")

    print("Loading TempControlDevice...")

    TempControlDevices = TempControlDeviceTracker(Labwares, DeckLocations)
    TempControlDeviceLoader.LoadYaml(
        TempControlDevices,
        "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\ABN\\HamiltonVisualMethodEditorConfiguration\\HAL\\TempControlDevice\\TempControlDevice.yaml",
    )
    HalInstance.TempControlDeviceTrackerInstance = TempControlDevices
    for TempControlDevice in TempControlDevices.GetLoadedObjectsAsList():
        print(TempControlDevice)

    print("Success! \n\n")

    print("Loading Tip...")

    Tips = TipTracker()
    TipLoader.LoadYaml(
        Tips,
        "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\ABN\\HamiltonVisualMethodEditorConfiguration\\HAL\\Tip\\Tip.yaml",
    )
    HalInstance.TipTrackerInstance = Tips
    for Tip in Tips.GetLoadedObjectsAsList():
        print(Tip)

    print("Success! \n\n")

    print("Loading Pipette...")

    Pipettes = PipetteTracker(Tips)
    PipetteLoader.LoadYaml(
        Pipettes,
        "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\ABN\\HamiltonVisualMethodEditorConfiguration\\HAL\\Pipette\\Pipette.yaml",
    )
    HalInstance.PipetteTrackerInstance = Pipettes
    for Pipette in Pipettes.GetLoadedObjectsAsList():
        print(Pipette)

    print("Success! \n\n")

    print("Loading Magnetic Rack...")

    MagneticRacks = MagneticRackTracker(Labwares, DeckLocations, Pipettes, Tips)
    MagneticRackLoader.LoadYaml(
        MagneticRacks,
        "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\ABN\\HamiltonVisualMethodEditorConfiguration\\HAL\\MagneticRack\\MagneticRack.yaml",
    )
    HalInstance.MagneticRackTrackerInstance = MagneticRacks
    for MagneticRack in MagneticRacks.GetLoadedObjectsAsList():
        print(MagneticRack)

    print("Success! \n\n")

    print("Loading Notify...")

    NotifyDevices = NotifyTracker()
    NotifyLoader.LoadYaml(
        NotifyDevices,
        "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\ABN\\HamiltonVisualMethodEditorConfiguration\\HAL\\Notify\\Notify.yaml",
    )
    HalInstance.NotifyTrackerInstance = NotifyDevices
    for NotifyDevice in NotifyDevices.GetLoadedObjectsAsList():
        print(NotifyDevice)

    print("Success! \n\n")

    print("Loading FlipTube...")

    FlipTubes = FlipTubeTracker(Labwares)
    FlipTubeLoader.LoadYaml(
        FlipTubes,
        "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\ABN\\HamiltonVisualMethodEditorConfiguration\\HAL\\FlipTube\\FlipTube.yaml",
    )
    HalInstance.FlipTubeTrackerInstance = FlipTubes
    for FlipTube in FlipTubes.GetLoadedObjectsAsList():
        print(FlipTube)

    print("Success! \n\n")
