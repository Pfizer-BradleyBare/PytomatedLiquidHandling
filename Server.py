import ABN.Source.Server.Tools.Logger as Logger

import ABN.Source.Server.Command.Respond as Respond
import ABN.Source.Server.Command.Request as Request
import ABN.Source.Server.State.IsActive as IsActive
import ABN.Source.Server.State.Kill as Kill
import ABN.Source.Server.Method.Status as Status
import ABN.Source.Server.Method.Queue as Queue
import ABN.Source.Server.Method.Dequeue as Dequeue

import web

if __name__ == "__main__":

    Logger.LOG.info("Starting Server")

    urls = ()
    urls += Respond.urls
    urls += Request.urls
    urls += IsActive.urls
    urls += Kill.urls
    urls += Status.urls
    urls += Queue.urls
    urls += Dequeue.urls

    app = web.application(urls, globals())
    app.run()
