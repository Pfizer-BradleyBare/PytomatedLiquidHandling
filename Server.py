import os

import web

# import ABN.Source.API.Endpoints.AvailableMethods as AvailableMethods
# import ABN.Source.API.Endpoints.CleanupMethodProject as CleanupMethodProject
# import ABN.Source.API.Endpoints.Close as Close
# import ABN.Source.API.Endpoints.Dequeue as Dequeue
# import ABN.Source.API.Endpoints.GenerateMethodFile as GenerateMethodFile
# import ABN.Source.API.Endpoints.ListQueue as ListQueue
# import ABN.Source.API.Endpoints.Open as Open
# import ABN.Source.API.Endpoints.Queue as Queue
# import ABN.Source.API.Endpoints.Status as Status
import ABN.Source.Driver.Endpoints.Request as Request
import ABN.Source.Driver.Endpoints.Respond as Respond
import ABN.Source.Driver.Endpoints.IsReady as IsReady
import ABN.Source.Server.Endpoints.IsActive as IsActive
import ABN.Source.Server.Endpoints.Kill as Kill
import ABN.Source.Server.Globals.Logger as Logger

if __name__ == "__main__":

    os.environ["PORT"] = "255"
    # Set port

    Logger.LOG.info("Starting Server")

    urls = ()
    urls += IsReady.urls
    urls += Respond.urls
    urls += Request.urls
    urls += IsActive.urls
    urls += Kill.urls
    #    urls += Status.urls
    #    urls += Queue.urls
    #    urls += Dequeue.urls
    #    urls += AvailableMethods.urls
    #    urls += GenerateMethodFile.urls
    #    urls += Open.urls
    #    urls += Close.urls
    #    urls += ListQueue.urls
    #    urls += CleanupMethodProject.urls

    app = web.application(urls, globals())
    app.run()
