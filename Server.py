import ABN.Source.Server.Globals.Logger as Logger

import ABN.Source.Server.Command.Respond as Respond
import ABN.Source.Server.Command.Request as Request
import ABN.Source.Server.State.IsActive as IsActive
import ABN.Source.Server.State.Kill as Kill
import ABN.Source.Server.Method.Status as Status
import ABN.Source.Server.Method.Queue as Queue
import ABN.Source.Server.Method.Dequeue as Dequeue
import ABN.Source.Server.Method.AvailableMethods as AvailableMethods
import ABN.Source.Server.Method.GenerateMethodFile as GenerateMethodFile
import ABN.Source.Server.Method.Open as Open
import ABN.Source.Server.Method.Close as Close

import web
import os


if __name__ == "__main__":

    os.environ["PORT"] = "255"
    # Set port

    Logger.LOG.info("Starting Server")

    urls = ()
    urls += Respond.urls
    urls += Request.urls
    urls += IsActive.urls
    urls += Kill.urls
    urls += Status.urls
    urls += Queue.urls
    urls += Dequeue.urls
    urls += AvailableMethods.urls
    urls += GenerateMethodFile.urls
    urls += Open.urls
    urls += Close.urls

    app = web.application(urls, globals())
    app.run()
