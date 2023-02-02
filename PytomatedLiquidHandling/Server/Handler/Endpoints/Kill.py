# curl -X GET http://localhost:255/State/Kill
import web

from ...Tools.Parser import Parser

urls = ("/Server/Kill", "ABN.Source.Server.Handler.Endpoints.Kill.Kill")


class Kill:
    def GET(self):
        from ...Handler import GetHandler

        LoggerInstance = GetHandler().GetLogger()

        ParserObject = Parser("Server Kill", web.data())

        if not ParserObject.IsValid([]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        LoggerInstance.info("Starting Kill sequence...")

        GetHandler().KillServer()

        LoggerInstance.info("Kill sequence complete! Goodbye!")

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
