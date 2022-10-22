# curl -X GET http://localhost:65535/State/Kill
from ..Tools import AliveStateFlag
from ..Tools.WorkbookTrackerInstance import WorkbookTrackerInstance
from ..Tools import LOG
from ..Parser import Parser

urls = ("/State/Kill", "ABN.Source.Server.State.Kill.Kill")


class Kill:
    def GET(self):

        ParserObject = Parser("State Kill", None)

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
