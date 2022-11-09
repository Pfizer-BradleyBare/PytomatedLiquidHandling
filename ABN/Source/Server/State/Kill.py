# curl -X GET http://localhost:65535/State/Kill
from ..Globals import AliveStateFlag
from ..Globals.WorkbookTrackerInstance import WorkbookTrackerInstance
from ..Globals import LOG
from ..Tools.Parser import Parser

import web

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
            WorkbookInstance.GetProcessingLock().release()
            Thread.join()

        del ParserObject

        LOG.info("Kill sequence complete! Goodbye!")

        quit()
