from dataclasses import dataclass

from ...Driver.Hamilton.ClosedContainer import FlipTube as FlipTubeDriver
from .BaseClosedContainer import ClosedContainerABC


@dataclass
class HamiltonFlipTubeSpecial(ClosedContainerABC):
    class Initialize(ClosedContainerABC.Initialize):
        @staticmethod
        def Execute(InterfaceHandle) -> None:
            if not isinstance(InterfaceHandle, HamiltonFlipTubeSpecial):
                raise Exception("Should not happen")

            ClosedContainerABC.Initialize.Execute(InterfaceHandle)

            Command = FlipTubeDriver.Initialize.Command(
                CustomErrorHandling=InterfaceHandle.CustomErrorHandling,
            )
            InterfaceHandle.BackendInstance.ExecuteCommand(Command)
            InterfaceHandle.BackendInstance.WaitForResponseBlocking(Command)
            InterfaceHandle.BackendInstance.GetResponse(
                Command, FlipTubeDriver.Initialize.Response
            )

    class Open(ClosedContainerABC.Open):
        @staticmethod
        def Execute(InterfaceHandle, OptionsTrackerInstance) -> None:
            if not isinstance(InterfaceHandle, HamiltonFlipTubeSpecial):
                raise Exception("Should not happen")

            if not isinstance(
                OptionsTrackerInstance, ClosedContainerABC.Open.OptionsTracker
            ):
                raise Exception("Should not happen")

            OpenOptionsTrackerInstance = FlipTubeDriver.Open.OptionsTracker(
                ToolSequence=InterfaceHandle.ToolSequence
            )
            for OpenCloseOptions in OptionsTrackerInstance.GetObjectsAsList():
                if (
                    OpenCloseOptions.LayoutItemInstance.LabwareInstance
                    in InterfaceHandle.SupportedLabwareTrackerInstance.GetObjectsAsList()
                ):
                    OpenOptionsTrackerInstance.LoadSingle(
                        FlipTubeDriver.Open.Options(
                            Sequence=OpenCloseOptions.LayoutItemInstance.Sequence,
                            SequencePosition=OpenCloseOptions.Position,
                        )
                    )

            Command = FlipTubeDriver.Open.Command(
                OptionsTrackerInstance=OpenOptionsTrackerInstance,
                CustomErrorHandling=InterfaceHandle.CustomErrorHandling,
            )
            InterfaceHandle.BackendInstance.ExecuteCommand(Command)
            InterfaceHandle.BackendInstance.WaitForResponseBlocking(Command)
            InterfaceHandle.BackendInstance.GetResponse(
                Command, FlipTubeDriver.Open.Response
            )

        @staticmethod
        def ExecutionTime(OptionsTrackerInstance) -> float:
            return 0

    class Close(ClosedContainerABC.Close):
        @staticmethod
        def Execute(InterfaceHandle, OptionsTrackerInstance) -> None:
            if not isinstance(InterfaceHandle, HamiltonFlipTubeSpecial):
                raise Exception("Should not happen")

            if not isinstance(
                OptionsTrackerInstance, ClosedContainerABC.Close.OptionsTracker
            ):
                raise Exception("Should not happen")

            CloseOptionsTrackerInstance = FlipTubeDriver.CloseSpecial.OptionsTracker(
                ToolSequence=InterfaceHandle.ToolSequence
            )
            for OpenCloseOptions in OptionsTrackerInstance.GetObjectsAsList():
                if (
                    OpenCloseOptions.LayoutItemInstance.LabwareInstance
                    in InterfaceHandle.SupportedLabwareTrackerInstance.GetObjectsAsList()
                ):
                    CloseOptionsTrackerInstance.LoadSingle(
                        FlipTubeDriver.CloseSpecial.Options(
                            Sequence=OpenCloseOptions.LayoutItemInstance.Sequence,
                            SequencePosition=OpenCloseOptions.Position,
                        )
                    )

            Command = FlipTubeDriver.CloseSpecial.Command(
                OptionsTrackerInstance=CloseOptionsTrackerInstance,
                CustomErrorHandling=InterfaceHandle.CustomErrorHandling,
            )
            InterfaceHandle.BackendInstance.ExecuteCommand(Command)
            InterfaceHandle.BackendInstance.WaitForResponseBlocking(Command)
            InterfaceHandle.BackendInstance.GetResponse(
                Command, FlipTubeDriver.CloseSpecial.Response
            )

        @staticmethod
        def ExecutionTime(OptionsTrackerInstance) -> float:
            return 0
