import os

import web

import ABN.Source.API.Handler.APIHandler as APIH
import ABN.Source.App.Handler.AppHandler as AppH
import ABN.Source.Driver.Handler.DriverHandler as DriverH
import ABN.Source.Server.Globals.HandlerRegistry as HR
import ABN.Source.Server.Globals.Logger as Logger
import ABN.Source.Server.Handler.ServerHandler as ServerH

quit()

if __name__ == "__main__":

    os.environ["PORT"] = "255"
    # Set port

    Logger.LOG.info("Starting Server")

    ServerHandler = ServerH.ServerHandler()
    DriverHandler = DriverH.DriverHandler()
    APIHandler = APIH.APIHandler()
    AppHandler = AppH.AppHandler()
    # Create our handlers

    urls = ()
    urls += ServerHandler.GetEndpoints()
    urls += DriverHandler.GetEndpoints()
    urls += APIHandler.GetEndpoints()
    urls += AppHandler.GetEndpoints()
    # Add endpoints as addresses we can access over HTTP

    HR.RegisterServerHandler(ServerHandler)
    HR.RegisterDriverHandler(DriverHandler)
    HR.RegisterAPIHandler(APIHandler)
    HR.RegisterAppHandler(AppHandler)
    # Register each handler with our main server

    app = web.application(urls, globals())
    app.run()
