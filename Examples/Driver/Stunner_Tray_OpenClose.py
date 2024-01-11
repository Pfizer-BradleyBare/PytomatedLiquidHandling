from PytomatedLiquidHandling.Driver.UnchainedLabs import (
    CloseTray,
    DefineExperiment,
    GetResults,
    GetStatus,
    OpenTray,
    Reset,
    StartMeasurement,
)
from PytomatedLiquidHandling.Driver.UnchainedLabs.Backend import StunnerBackend

Backend = StunnerBackend(
    Identifier="Example Stunner",
    InstrumentIPAddress="10.37.144.9",
    InstrumentPort=6300,
)

Backend.StartBackend()
# Creates the Backend so we can communicate with the Hamilton


Command = CloseTray.Command()
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Backend.GetResponse(Command, CloseTray.Response)

Command = DefineExperiment.Command(
    Options=DefineExperiment.ListedOptions(
        ExperimentName="Test",
        ApplicationName=DefineExperiment.ListedOptions.ApplicationNameOptions.ProteinSinglePoint,
    )
)
Command.Options.append(
    DefineExperiment.Options(
        SampleName="A", SamplePlateID="Plate 1", SamplePlatePosition="A1", SampleGroup=1
    )
)
Command.Options.append(
    DefineExperiment.Options(
        SampleName="B", SamplePlateID="Plate 1", SamplePlatePosition="B1", SampleGroup=1
    )
)
Command.Options.append(
    DefineExperiment.Options(
        SampleName="C", SamplePlateID="Plate 1", SamplePlatePosition="C1", SampleGroup=1
    )
)
Command.Options.append(
    DefineExperiment.Options(
        SampleName="D", SamplePlateID="Plate 1", SamplePlatePosition="D1", SampleGroup=1
    )
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response1 = Backend.GetResponse(Command, DefineExperiment.Response)
print(Response1.DefinedPlateIDs)

Command = GetStatus.Command()
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, GetStatus.Response)

Command = StartMeasurement.Command(
    Options=StartMeasurement.Options(PlateID=Response1.DefinedPlateIDs[0])
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Backend.GetResponse(Command, StartMeasurement.Response)


import time

try:
    while True:
        Command = GetStatus.Command()
        Backend.ExecuteCommand(Command)
        Backend.WaitForResponseBlocking(Command)
        Response = Backend.GetResponse(Command, GetStatus.Response)

        print(Response.StatusCodeParsed)
        print(Response.MeasurementInfo)
        print("Sleep")
        time.sleep(5)


except:
    print("LEAVING!")
    time.sleep(1)

Command = GetResults.Command(Options=GetResults.ListedOptions())
Command.Options += [
    GetResults.Options.SampleName,
    GetResults.Options.A280,
    GetResults.Options.PlatePosition,
]
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, GetResults.Response)

Command = CloseTray.Command()
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Backend.GetResponse(Command, CloseTray.Response)

print(Response.ResultsParsed[0][GetResults.Options.SampleName])
print(Response.ResultsPath)

Backend.StopBackend()
# Done!
