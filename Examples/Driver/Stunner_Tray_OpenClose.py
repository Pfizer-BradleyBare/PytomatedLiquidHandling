from PytomatedLiquidHandling.Driver.UnchainedLabs import (
    CloseTray,
    DefineExperiment,
    OpenTray,
)
from PytomatedLiquidHandling.Driver.UnchainedLabs.Backend import StunnerBackend

Command = DefineExperiment.Command(
    Options=DefineExperiment.ListedOptions(
        ExperimentName="Test",
        ApplicationName=DefineExperiment.ListedOptions.ApplicationNameOptions.ProteinSinglePoint,
    )
)
Command.Options.append(
    DefineExperiment.Options(
        SampleName="A",
        SamplePlateID="Plate 1",
        SamplePlatePosition="A1",
        SampleGroup=1,
        BlankSampleName="A",
    )
)
Command.Options.append(
    DefineExperiment.Options(
        SampleName="B",
        SamplePlateID="Plate 1",
        SamplePlatePosition="B1",
        SampleGroup=1,
        BlankSampleName="A",
    )
)
Command.Options.append(
    DefineExperiment.Options(
        SampleName="C",
        SamplePlateID="Plate 1",
        SamplePlatePosition="C1",
        SampleGroup=1,
        BlankSampleName="C",
    )
)
Command.Options.append(
    DefineExperiment.Options(
        SampleName="D",
        SamplePlateID="Plate 1",
        SamplePlatePosition="D1",
        SampleGroup=1,
        BlankSampleName="C",
    )
)
Command._ExecuteCommandHelper("")
quit()

Backend = StunnerBackend(
    Identifier="Example Stunner",
    InstrumentIPAddress="10.37.145.113",
    InstrumentPort=6300,
)

Backend.StartBackend()
# Creates the Backend so we can communicate with the Hamilton

Command = OpenTray.Command()
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Backend.GetResponse(Command, OpenTray.Response)

Command = CloseTray.Command()
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Backend.GetResponse(Command, CloseTray.Response)

Backend.StopBackend()
# Done!
