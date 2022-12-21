from ...Tools.AbstractClasses import ServerHandlerABC
from ..Workbook import WorkbookTracker
from .Endpoints import (
    AvailableMethods,
    CleanupMethodProject,
    Close,
    Dequeue,
    GenerateMethodFile,
    ListQueue,
    Open,
    Queue,
    Status,
)


class AppHandler(ServerHandlerABC):
    def __init__(self):
        self.WorkbookTrackerInstance: WorkbookTracker = WorkbookTracker()

    def GetName(self) -> str:
        return "App"

    def GetEndpoints(self) -> tuple:
        urls = ()
        urls += AvailableMethods.urls
        urls += CleanupMethodProject.urls
        urls += Close.urls
        urls += Dequeue.urls
        urls += GenerateMethodFile.urls
        urls += ListQueue.urls
        urls += Open.urls
        urls += Queue.urls
        urls += Status.urls
        return urls

    def Kill(self):
        pass
