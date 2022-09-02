# Test Command
# curl -H "Content-Type: application/json" -X POST -d '{\"name\":\"Joe\"}' http://localhost:8080/Comm
# curl -X GET http://localhost:8080/Comm

import sys
import os
import web
import datetime

import ABN.Source.Server.Command.Respond as Respond
import ABN.Source.Server.Command.Request as Request
import ABN.Source.Server.State.IsActive as IsActive
import ABN.Source.Server.State.Kill as Kill
import ABN.Source.Server.Method.Status as Status
import ABN.Source.Server.Method.Queue as Queue
import ABN.Source.Server.Method.Dequeue as Dequeue


DIRECTORY = "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\ABN\\Config\\LogFiles"
TIME = str(datetime.datetime.now().strftime("%d%b%Y-%H%M%S"))
BASE_LOGFILE_NAME = "Log.txt"
LOG_FILE_FULL_PATH = os.path.join(DIRECTORY, TIME + BASE_LOGFILE_NAME)


class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open(LOG_FILE_FULL_PATH, "w")

    def __del__(self):
        self.log.close()

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()

    def flush(self):
        pass


sys.stdout = Logger()


urls = ()
urls += Respond.urls
urls += Request.urls
urls += IsActive.urls
urls += Kill.urls
urls += Status.urls
urls += Queue.urls
urls += Dequeue.urls


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
