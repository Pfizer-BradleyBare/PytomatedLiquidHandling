from ...Driver.Hamilton.ClosedContainer import FlipTube as FlipTubeDriver
from ..Labware import LabwareTracker
from .BaseClosedContainer import ClosedContainer, OpenCloseOptionsTracker
from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ..DeckLocation import DeckLocationTracker


class HamiltonFlipTubeSpecial(ClosedContainer):
    def __init__(
        self,
        UniqueIdentifier: str,
        BackendInstance: HamiltonBackendABC,
        CustomErrorHandling: bool,
        ToolSequence: str,
        SupportedDeckLocationTrackerInstance: DeckLocationTracker,
        SupportedLabwareTrackerInstance: LabwareTracker,
    ):
        ClosedContainer.__init__(
            self,
            UniqueIdentifier,
            BackendInstance,
            CustomErrorHandling,
            ToolSequence,
            SupportedDeckLocationTrackerInstance,
            SupportedLabwareTrackerInstance,
        )

    def Initialize(self):
        Command = FlipTubeDriver.Initialize.Command(
            CustomErrorHandling=self.GetErrorHandlingSetting(),
        )
        self.GetBackend().ExecuteCommand(Command)
        self.GetBackend().WaitForResponseBlocking(Command)
        self.GetBackend().GetResponse(Command, Command.Response)

    def Deinitialize(self):
        ...

    def Open(
        self,
        *,
        OpenCloseOptionsTrackerInstance: OpenCloseOptionsTracker,
    ):
        OptionsTrackerInstance = FlipTubeDriver.Open.OptionsTracker(
            ToolSequence=self.ToolSequence,
        )
        for OpenCloseOptions in OpenCloseOptionsTrackerInstance.GetObjectsAsList():
            if (
                OpenCloseOptions.LayoutItemInstance.LabwareInstance
                in self.SupportedLabwareTrackerInstance.GetObjectsAsList()
            ):
                OptionsTrackerInstance.LoadSingle(
                    FlipTubeDriver.Open.Options(
                        Sequence=OpenCloseOptions.LayoutItemInstance.Sequence,
                        SequencePosition=OpenCloseOptions.Position,
                    )
                )

        try:
            Command = FlipTubeDriver.Open.Command(
                OptionsTrackerInstance=OptionsTrackerInstance,
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )
            self.GetBackend().ExecuteCommand(Command)
            self.GetBackend().WaitForResponseBlocking(Command)
            self.GetBackend().GetResponse(Command, Command.Response)

        except:
            ...

    def Close(
        self,
        *,
        OpenCloseOptionsTrackerInstance: OpenCloseOptionsTracker,
    ):
        OptionsTrackerInstance = FlipTubeDriver.CloseSpecial.OptionsTracker(
            ToolSequence=self.ToolSequence,
        )
        for OpenCloseOptions in OpenCloseOptionsTrackerInstance.GetObjectsAsList():
            if (
                OpenCloseOptions.LayoutItemInstance.LabwareInstance
                in self.SupportedLabwareTrackerInstance.GetObjectsAsList()
            ):
                OptionsTrackerInstance.LoadSingle(
                    FlipTubeDriver.CloseSpecial.Options(
                        Sequence=OpenCloseOptions.LayoutItemInstance.Sequence,
                        SequencePosition=OpenCloseOptions.Position,
                    )
                )

        try:
            Command = FlipTubeDriver.CloseSpecial.Command(
                OptionsTrackerInstance=OptionsTrackerInstance,
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )
            self.GetBackend().ExecuteCommand(Command)
            self.GetBackend().WaitForResponseBlocking(Command)
            self.GetBackend().GetResponse(Command, Command.Response)

        except:
            ...
