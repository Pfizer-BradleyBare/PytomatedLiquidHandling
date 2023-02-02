from ...API.Tools.Timer import TimerTracker
from ...Tools.AbstractClasses import ServerHandlerABC
from ..Workbook import WorkbookTracker
from .Endpoints import (
    AvailableMethods,
    CleanupMethodProject,
    CloseExcel,
    Dequeue,
    FlexibleTest,
    GenerateMethodFile,
    GetPathwayStates,
    GetWorkbookInfo,
    ListQueue,
    OpenExcel,
    QueueMethod,
)


class Handler(ServerHandlerABC):
    def __init__(self):
        ServerHandlerABC.__init__(self)
        self.WorkbookTrackerInstance: WorkbookTracker = WorkbookTracker()
        self.TimerTrackerInstance: TimerTracker = TimerTracker()

    def GetName(self) -> str:
        return "App"

    def GetEndpoints(self) -> tuple:
        urls = ()
        urls += AvailableMethods.urls
        urls += CleanupMethodProject.urls
        urls += CloseExcel.urls
        urls += Dequeue.urls
        urls += GenerateMethodFile.urls
        urls += ListQueue.urls
        urls += OpenExcel.urls
        urls += QueueMethod.urls
        urls += FlexibleTest.urls
        urls += GetWorkbookInfo.urls
        urls += GetPathwayStates.urls
        return urls

    def Kill(self):
        pass
