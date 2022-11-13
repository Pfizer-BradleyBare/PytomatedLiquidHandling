import web
from ..Tools.Parser import Parser
from .AvailableMethods import MethodsPath, TemplateMethodSuffix, TempFolder
import os
import shutil
import stat
from ...Tools import Excel, ExcelHandle
from typing import cast

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

        DesiredMethodFilePath = os.path.join(
            MethodsPath,
            MethodFolder,
            ProjectFolder,
            TempFolder,
            ParserObject.GetAPIData()["Desired Filename"] + ".xlsm",
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
        print("Pre-attach")
        with ExcelHandle(False) as ExcelHandleInstance:
            print("Pre-attach")
            ExcelInstance.AttachHandle(ExcelHandleInstance)
            print("Post")

            ExcelInstance.SelectSheet("Worklist")
            CopyFormula = cast(
                tuple[tuple[any]], ExcelInstance.ReadRangeFormulas(2, 1, 2, 3)  # type: ignore
            )

            CopyFormula = CopyFormula * int(ParserObject.GetAPIData()["Sample Number"])
            ExcelInstance.WriteRangeFormulas(2, 1, CopyFormula)

            ExcelInstance.Save()

        ParserObject.SetAPIState(True)
        ParserObject.SetAPIReturn("Message", "Method file created successfully")
        ParserObject.SetAPIReturn("Method File Path", DesiredMethodFilePath)

        Response = ParserObject.GetHTTPResponse()
        return Response
