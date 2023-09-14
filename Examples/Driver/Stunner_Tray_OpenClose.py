from PytomatedLiquidHandling.Driver.UnchainedLabs import CloseTray, OpenTray
from PytomatedLiquidHandling.Driver.UnchainedLabs.Backend import StunnerBackend


Backend = StunnerBackend("Example Stunner", "10.37.145.113", 6300)

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
