import os
import shutil
import stat
from typing import cast

import web

from PytomatedLiquidHandling.Server.Tools.Parser import Parser

from ...Tools.Excel import Excel
from .AvailableMethods import MethodsPath, TempFolder, TemplateMethodSuffix

urls = (
    "/App/GenerateMethodFile",
    "App.Handler.Endpoints.GenerateMethodFile.GenerateMethodFile",
)


class GenerateMethodFile:
    def POST(self):
        ParserObject = Parser("App GenerateMethodFile", web.data())

        if not ParserObject.IsValid(
            ["Method", "Project", "Desired Filename", "Sample Number"]
        ):
            Response = ParserObject.GetHTTPResponse()
            return Response

        MethodFolder = ParserObject.GetEndpointInputData()["Method"]
        ProjectFolder = ParserObject.GetEndpointInputData()["Project"]

        TemplateMethodFile = (
            TemplateMethodSuffix + "_" + MethodFolder + "_" + ProjectFolder + ".xlsm"
        )

        TemplateMethodFilePath = os.path.join(
            MethodsPath, MethodFolder, ProjectFolder, TemplateMethodFile
        )

        DesiredMethodFilePath = os.path.join(
            MethodsPath,
            MethodFolder,
            ProjectFolder,
            TempFolder,
            ParserObject.GetEndpointInputData()["Desired Filename"] + ".xlsm",
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

        shutil.copy(TemplateMethodFilePath, DesiredMethodFilePath)
        os.chmod(DesiredMethodFilePath, stat.S_IWRITE)

        ExcelInstance = Excel(DesiredMethodFilePath)
        ExcelInstance.OpenBook(False)

        CopyFormula = cast(
            tuple[tuple[any]], ExcelInstance.ReadRangeFormulas("Worklist", 2, 1, 2, 3)  # type: ignore
        )

        CopyFormula = CopyFormula * int(
            ParserObject.GetEndpointInputData()["Sample Number"]
        )
        ExcelInstance.WriteRangeFormulas("Worklist", 2, 1, CopyFormula)

        ExcelInstance.Save()
        ExcelInstance.CloseBook()

        ParserObject.SetEndpointState(True)
        ParserObject.SetEndpointOutputKey("Method File Path", DesiredMethodFilePath)

        Response = ParserObject.GetHTTPResponse()
        return Response
