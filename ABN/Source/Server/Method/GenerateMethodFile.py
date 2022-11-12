import web
from ..Tools.Parser import Parser
from .AvailableMethods import MethodsPath, TemplateMethodSuffix, TempFolder
import os
import shutil
import stat
import xlwings
import pythoncom


urls = (
    "/Method/GenerateMethodFile",
    "ABN.Source.Server.Method.GenerateMethodFile.GenerateMethodFile",
)


class GenerateMethodFile:
    def POST(self):
        ParserObject = Parser("Method GenerateMethodFile", web.data())

        if not ParserObject.IsValid(
            ["Method", "Project", "Desired Filename", "Sample Number"]
        ):
            Response = ParserObject.GetHTTPResponse()
            return Response

        MethodFolder = ParserObject.GetAPIData()["Method"]
        ProjectFolder = ParserObject.GetAPIData()["Project"]

        TemplateMethodFile = (
            TemplateMethodSuffix + "_" + MethodFolder + "_" + ProjectFolder + ".xlsm"
        )

        TemplateMethodFilePath = os.path.join(
            MethodsPath, MethodFolder, ProjectFolder, TemplateMethodFile
        )

        try:
            os.mkdir(
                os.path.join(
                    MethodsPath,
                    MethodFolder,
                    ProjectFolder,
                    TempFolder,
                ),
            )
        except FileExistsError:
            pass

        DesiredMethodFilePath = os.path.join(
            MethodsPath,
            MethodFolder,
            ProjectFolder,
            TempFolder,
            ParserObject.GetAPIData()["Desired Filename"] + ".xlsm",
        )

        shutil.copy(TemplateMethodFilePath, DesiredMethodFilePath)
        os.chmod(DesiredMethodFilePath, stat.S_IWRITE)

        pythoncom.CoInitialize()
        with xlwings.App(visible=True, add_book=False) as XLApp:

            Book = XLApp.books.open(DesiredMethodFilePath)

            Sheet: xlwings.Sheet
            Sheet = Book.sheets["Worklist"]

            CopyFormula = Sheet.range((2, 1), (2, 100)).formula

            for Index in range(1, int(ParserObject.GetAPIData()["Sample Number"])):
                Sheet.range((2 + Index, 1), (2 + Index, 100)).formula = CopyFormula

            Book.save()

        ParserObject.SetAPIState(True)
        ParserObject.SetAPIReturn("Message", "Method file created successfully")

        Response = ParserObject.GetHTTPResponse()
        return Response
