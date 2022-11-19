import os

import web

import ABN.Source.Server.BackEnd.Request as Request
import ABN.Source.Server.BackEnd.Respond as Respond
import ABN.Source.Server.FrontEnd.AvailableMethods as AvailableMethods
import ABN.Source.Server.FrontEnd.CleanupMethodProject as CleanupMethodProject
import ABN.Source.Server.FrontEnd.Close as Close
import ABN.Source.Server.FrontEnd.Dequeue as Dequeue
import ABN.Source.Server.FrontEnd.GenerateMethodFile as GenerateMethodFile
import ABN.Source.Server.FrontEnd.ListQueue as ListQueue
import ABN.Source.Server.FrontEnd.Open as Open
import ABN.Source.Server.FrontEnd.Queue as Queue
import ABN.Source.Server.FrontEnd.Status as Status
import ABN.Source.Server.Globals.Logger as Logger
import ABN.Source.Server.State.IsActive as IsActive
import ABN.Source.Server.State.Kill as Kill

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
    urls += ListQueue.urls
    urls += CleanupMethodProject.urls

    app = web.application(urls, globals())
    app.run()
