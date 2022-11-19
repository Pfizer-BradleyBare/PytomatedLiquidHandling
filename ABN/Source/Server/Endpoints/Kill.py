# curl -X GET http://localhost:65535/State/Kill
import web

from ...API.Globals.WorkbookTrackerInstance import WorkbookTrackerInstance
from ..Globals import LOG, AliveStateFlag
from ..Tools.Parser import Parser

urls = ("/State/Kill", "ABN.Source.Server.State.Kill.Kill")


class Kill:
    def GET(self):

        ParserObject = Parser("State Kill", web.data())

        if not ParserObject.IsValid([]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        LOG.info("Starting Kill sequence...")

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

        LOG.info("Kill sequence complete! Goodbye!")

        quit()
