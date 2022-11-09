import web
from ..Tools.Parser import Parser
import os

MethodsPath = "C:\\___MethodsTest"

urls = (
    "/Method/AvailableMethods",
    "ABN.Source.Server.Method.AvailableMethods.AvailableMethods",
)


class AvailableMethods:
    def GET(self):
        ParserObject = Parser("Method AvailableMethods", web.data())

        if not ParserObject.IsValid([]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        MethodProjects = dict()

        Methods = [
            Item
            for Item in os.listdir(MethodsPath)
            if os.path.isdir(os.path.join(MethodsPath, Item))
        ]

        print(Methods)

        for Method in Methods:

            MethodProjects[Method] = [
                Dir
                for Dir in os.listdir(os.path.join(MethodsPath, Method))
                if Dir != "Archive"
            ]

        ParserObject.SetAPIState(True)
        ParserObject.SetAPIReturn("Methods", Methods)
        ParserObject.SetAPIReturn("Method Projects", MethodProjects)
        ParserObject.SetAPIReturn("Test", {"Test1": {"Test2": 1}})
        ParserObject.SetAPIReturn("Message", "Possible methods returned as dict")

        Response = ParserObject.GetHTTPResponse()
        return Response
