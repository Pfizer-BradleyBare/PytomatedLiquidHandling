import os

import web

import ABN.Source.Driver.Handler.DriverHandler as DH
import ABN.Source.Server.Globals.Logger as Logger
import ABN.Source.Server.Handler.ServerHandler as SH

if __name__ == "__main__":

    os.environ["PORT"] = "255"
    # Set port

    Logger.LOG.info("Starting Server")

    ServerHandler = SH.ServerHandler()
    DriverHandler = DH.DriverHandler()

    urls = ()
    urls += ServerHandler.GetEndpoints()
    urls += DriverHandler.GetEndpoints()

    ServerHandler.RegisterServerHandler(DriverHandler)

    app = web.application(urls, globals())
    app.run()
