import os
from logging import DEBUG

from PytomatedLiquidHandling.API.Handler import GetHandler as APIGetHandler
from PytomatedLiquidHandling.API.Handler import Handler as APIHandler
from PytomatedLiquidHandling.API.Tools.Timer import TimerTracker
from PytomatedLiquidHandling.Tools.AbstractClasses import ServerHandlerABC
from PytomatedLiquidHandling.Tools.Logger import Logger

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
    WorkbookTest,
)


class Handler(ServerHandlerABC):
    def __init__(self):
        LoggerInstance = Logger(
            "AppLogger",
            DEBUG,
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "Logging"),
        )

        ServerHandlerABC.__init__(self, LoggerInstance)

        global _HandlerInstance
        _HandlerInstance = self

        try:
            APIGetHandler()
        except:
            APIHandler(
                LoggerInstance,
                "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\AutomationBareNecessities\\App\\Configuration\\HAL",
            )

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
        urls += WorkbookTest.urls
        return urls

    def Kill(self):
        pass


_HandlerInstance: Handler | None = None


def GetHandler() -> Handler:

    if _HandlerInstance is None:
        raise Exception("Driver Handler not created. Please Create")

    else:
        return _HandlerInstance
