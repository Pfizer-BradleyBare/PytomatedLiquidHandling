import os

import web

import ABN.Source.API.Handler.APIHandler as AH
import ABN.Source.Driver.Handler.DriverHandler as DH
import ABN.Source.Server.Globals.HandlerRegistry as HR
import ABN.Source.Server.Globals.Logger as Logger
import ABN.Source.Server.Handler.ServerHandler as SH

if __name__ == "__main__":

    os.environ["PORT"] = "255"
    # Set port

    Logger.LOG.info("Starting Server")

    ServerHandler = SH.ServerHandler()
    DriverHandler = DH.DriverHandler()
    APIHandler = AH.APIHandler()
    # Create our handlers

    urls = ()
    urls += ServerHandler.GetEndpoints()
    urls += DriverHandler.GetEndpoints()
    urls += APIHandler.GetEndpoints()
    # Add endpoints as addresses we can access over HTTP

    HR.HandlerRegistry.ManualLoad(ServerHandler)
    HR.HandlerRegistry.ManualLoad(DriverHandler)
    HR.HandlerRegistry.ManualLoad(APIHandler)
    # Register each handler with our main server

    app = web.application(urls, globals())
    app.run()
