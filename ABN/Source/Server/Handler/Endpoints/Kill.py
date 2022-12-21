# curl -X GET http://localhost:65535/State/Kill
import web

from ...Globals import LOG
from ...Globals.HandlerRegistry import (
    GetAPIHandler,
    GetAppHandler,
    GetDriverHandler,
    GetHALHandler,
    GetServerHandler,
)
from ...Tools.Parser import Parser

urls = ("/State/Kill", "ABN.Source.Server.Handler.Endpoints.Kill.Kill")


class Kill:
    def GET(self):

        ParserObject = Parser("State Kill", web.data())

        if not ParserObject.IsValid([]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        LOG.info("Starting Kill sequence...")

        try:
            ServerHandler = GetServerHandler()
            ServerHandler.IsAliveFlag = False
            ServerHandler.Kill()
        except:
            pass

        try:
            DriverHandler = GetDriverHandler()
            DriverHandler.IsAliveFlag = False
            DriverHandler.Kill()
        except:
            pass

        try:
            HALHandler = GetHALHandler()
            HALHandler.IsAliveFlag = False
            HALHandler.Kill()
        except:
            pass

        try:
            APIHandler = GetAPIHandler()
            APIHandler.IsAliveFlag = False
            APIHandler.Kill()
        except:
            pass

        try:
            AppHandler = GetAppHandler()
            AppHandler.IsAliveFlag = False
            AppHandler.Kill()
        except:
            pass

        # We use try except because we cannot know which handlers are registered

        LOG.info("Kill sequence complete! Goodbye!")

        quit()

        LOG.debug("Setting state flag as false")
        AliveStateFlag.AliveStateFlag = False

        LOG.debug("Quit all workbook instances")
        for WorkbookInstance in WorkbookTrackerInstance.GetObjectsAsList():
            Thread = WorkbookInstance.GetWorkbookProcessorThread()

            LOG.debug("Killing thread: %s", Thread.name)
            if WorkbookInstance.GetProcessingLock().locked() is True:
                WorkbookInstance.GetProcessingLock().release()
            Thread.join()

        del ParserObject
