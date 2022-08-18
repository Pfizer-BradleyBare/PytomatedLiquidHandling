Attribute VB_Name = "RibbonModules"
'These are the macros that run the buttons in the Ribbon

Sub ResetMethod()

    If GlobalBuildingBlockWorkingStatus = True Then
        'MsgBox ("Blocks are killin' it!")
    Else
        MsgBox ("Building Blocks sheets was not loaded correctly so this function is disabled. Close and reopen the workbook with Macros enabled. Building Blocks will then be loaded automatically.")
        Exit Sub
    End If

        Application.ScreenUpdating = False

        ThisWorkbook.Worksheets("Method").Activate

        DeleteMethod
        
        ThisWorkbook.Worksheets("Method").Cells(2, 4).Value = "Plate - (Click Here to Update)"
        ThisWorkbook.Worksheets("Method").Cells(3, 4).Value = "Name"
        ThisWorkbook.Worksheets("Method").Cells(4, 4).Value = "Type"
        
        ThisWorkbook.Worksheets("Method").Cells(3, 5).Value = "Sample"
        ThisWorkbook.Worksheets("Method").Cells(4, 5).Value = "96 Well PCR Plate"
        
        ThisWorkbook.Worksheets("Method").Cells(2, 6).Value = "Comments"

    ThisWorkbook.Worksheets("Method").Activate
    
    SaveSteps
    DeleteMethod
    PrintSteps
    
    'I do it twice because it helps with formatting
    SaveSteps
    DeleteMethod
    PrintSteps
    
    ThisWorkbook.Worksheets("Solutions").Activate
    FindSolutions
    SaveSolutions
    DeleteSolutions
    ValidateSolutions
    PrintSolutions
    
    ThisWorkbook.Worksheets("Method").Activate
    
        Application.ScreenUpdating = True

End Sub


Sub Ribbon_ControlResetMethod(control As IRibbonControl)

    ResetMethod
        
End Sub

Sub Ribbon_ControlResetWorklist(control As IRibbonControl)

        Application.ScreenUpdating = False

        ThisWorkbook.Worksheets("Worklist").Activate

        For Col = 1 To 100
            With ThisWorkbook.Worksheets("Worklist").Columns(Col)
                .ColumnWidth = 20
            End With
        Next Col

        ThisWorkbook.Worksheets("Worklist").Range(Cells(1, 1), Cells(10000, 1000)).Delete
        ThisWorkbook.Worksheets("Worklist").Range(Cells(1, 1), Cells(10000, 1000)).Columns().Hidden = False
        
        ThisWorkbook.Worksheets("Worklist").Cells(1, 1).Value = "Sample Number"
        ThisWorkbook.Worksheets("Worklist").Cells(1, 2).Value = "Sample Description"
        ThisWorkbook.Worksheets("Worklist").Cells(1, 3).Value = "Sample Concentration (mg/mL)"

        ThisWorkbook.Worksheets("Worklist").Cells(2, 1).Formula = "=Row() - 1"
        ThisWorkbook.Worksheets("Worklist").Cells(2, 2).Value = "Blank"
        ThisWorkbook.Worksheets("Worklist").Cells(2, 3).Value = "10"
        
        ThisWorkbook.Worksheets("Worklist").Columns("A:C").AutoFit
        
        ThisWorkbook.Worksheets("Worklist").Range("A1:AZ100").HorizontalAlignment = xlCenter

        Application.ScreenUpdating = True

End Sub

Sub Ribbon_ControlRemoveLogs(control As IRibbonControl)
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False
    
    On Error Resume Next
    ThisWorkbook.Worksheets("Test Log").Delete
    ThisWorkbook.Worksheets("Run Log").Delete
    ThisWorkbook.Worksheets("Preparation List").Delete
    ThisWorkbook.Worksheets("Final Plate Volumes").Delete
    On Error GoTo 0
    
    ThisWorkbook.Worksheets("Method").Activate
    
    Application.DisplayAlerts = True
    Application.ScreenUpdating = True
End Sub

Sub Ribbon_TestTestMethod(control As IRibbonControl)

Ribbon_ControlRemoveLogs control

If Dir("C:\Program Files (x86)\HAMILTON\BAREB\Script\HamiltonVisualMethodEditor\MethodMaker.py") = "" Then
    MsgBox ("Automation Bare Necessities scripts are not available on this system. Please use an ABN PC or install on your pc")
Else
    If Dir("C:\Program Files (x86)\HAMILTON\BAREB\Script\HamiltonVisualMethodEditor\HamiltonVisualMethodEditorMethod\THIS IS NOT A METHOD___READ ME.txt") = "C:\Program Files (x86)\HAMILTON\BAREB\Script\HamiltonVisualMethodEditor\HamiltonVisualMethodEditorMethod\THIS IS NOT A METHOD___READ ME.txt" Then
        MsgBox ("No method library is selected. Please select a method library and try again")
    Else
        If Dir("C:\Program Files (x86)\HAMILTON\BAREB\Script\HamiltonVisualMethodEditor\HamiltonVisualMethodEditorConfiguration\THIS IS NOT A CORRECT CONFIGURATION BRANCH___READ ME.gitignore") = "C:\Program Files (x86)\HAMILTON\BAREB\Script\HamiltonVisualMethodEditor\HamiltonVisualMethodEditorConfiguration\THIS IS NOT A CORRECT CONFIGURATION BRANCH___READ ME.gitignore" Then
            MsgBox ("No instrument configuration is selected. Please select a configuration and try again")
        Else
            Dim Command As String
            Command = "python " & """C:\Program Files (x86)\HAMILTON\BAREB\Script\HamiltonVisualMethodEditor\MethodMaker.py""" & " " & """" & Application.ActiveWorkbook.FullName & """" & " " & "1 " & "Test"

            ThisWorkbook.Worksheets("Method").Activate

            RetVal = Shell(Command, vbNormalFocus)
        End If
    End If
End If

End Sub

Sub Ribbon_TestGeneratePrepList(control As IRibbonControl)

Ribbon_ControlRemoveLogs control

If Dir("C:\Program Files (x86)\HAMILTON\BAREB\Script\HamiltonVisualMethodEditor\MethodMaker.py") = "" Then
    MsgBox ("Automation Bare Necessities scripts are not available on this system. Please use an ABN PC or install on your pc")
Else
    If Dir("C:\Program Files (x86)\HAMILTON\BAREB\Script\HamiltonVisualMethodEditor\HamiltonVisualMethodEditorMethod\THIS IS NOT A METHOD___READ ME.txt") = "C:\Program Files (x86)\HAMILTON\BAREB\Script\HamiltonVisualMethodEditor\HamiltonVisualMethodEditorMethod\THIS IS NOT A METHOD___READ ME.txt" Then
        MsgBox ("No method library is selected. Please select a method library and try again")
    Else
        If Dir("C:\Program Files (x86)\HAMILTON\BAREB\Script\HamiltonVisualMethodEditor\HamiltonVisualMethodEditorConfiguration\THIS IS NOT A CORRECT CONFIGURATION BRANCH___READ ME.gitignore") = "C:\Program Files (x86)\HAMILTON\BAREB\Script\HamiltonVisualMethodEditor\HamiltonVisualMethodEditorConfiguration\THIS IS NOT A CORRECT CONFIGURATION BRANCH___READ ME.gitignore" Then
            MsgBox ("No instrument configuration is selected. Please select a configuration and try again")
        Else
            Dim Command As String
            Command = "python " & """C:\Program Files (x86)\HAMILTON\BAREB\Script\HamiltonVisualMethodEditor\MethodMaker.py""" & " " & """" & Application.ActiveWorkbook.FullName & """" & " " & "1 " & "PrepList"

            ThisWorkbook.Worksheets("Worklist").Activate
            MessageReturn = MsgBox("Preparing to generate a prep sheet for your run. Please ensure all samples are added to the worklist before proceeding...", vbQuestion + vbDefaultButton1 + vbOKCancel, "Ready?")

            If MessageReturn = vbOK Then
                RetVal = Shell(Command, vbNormalFocus)
            End If
        End If
    End If
End If

End Sub

Sub Ribbon_HelpOpenDocument(control As IRibbonControl)
    OpenWordDocument
    GotoBookmark ("Purpose")
End Sub

Sub Ribbon_HelpRunMethod(control As IRibbonControl)
    OpenWordDocument
    GotoBookmark ("MethodRun")
End Sub

Sub Ribbon_HelpTroubleshooting(control As IRibbonControl)
    OpenWordDocument
    GotoBookmark ("MethodTroubleshooting")
End Sub

Sub Ribbon_HelpWorkbookOverview(control As IRibbonControl)
    OpenWordDocument
    GotoBookmark ("WorkbookOverview")
End Sub

Sub Ribbon_HelpWorklistInterface(control As IRibbonControl)
    OpenWordDocument
    GotoBookmark ("MethodCreationBlocksInterface")
End Sub

Sub Ribbon_HelpBlocksOverview(control As IRibbonControl)
    OpenWordDocument
    GotoBookmark ("MethodCreationBlocks")
End Sub

Sub Ribbon_HelpBlocksDescriptions(control As IRibbonControl)
    OpenWordDocument
    GotoBookmark ("BlockDescriptions")
End Sub

Sub Ribbon_HelpSolutionsOverview(control As IRibbonControl)
    OpenWordDocument
    GotoBookmark ("MethodCreationSolutions")
End Sub

Sub Ribbon_HelpBuildOverview(control As IRibbonControl)
    OpenWordDocument
    GotoBookmark ("MethodBuilding")
End Sub

Sub Ribbon_HelpTestOverview(control As IRibbonControl)
    OpenWordDocument
    GotoBookmark ("MethodCreationMethodTesting")
End Sub

Sub Ribbon_HelpLogsOverview(control As IRibbonControl)
    OpenWordDocument
    GotoBookmark ("MethodLogs")
End Sub

Sub GetABNFiles()

Dim Command As String

Command = "POWERSHELL.exe -noexit " & """mkdir """ & """""$home\OneDrive - Pfizer\Documents\_ABN\BuildingBlocks"""""
X = Shell(Command, vbHide)

Command = "POWERSHELL.exe -noexit " & """curl """ & """""https://github.com/Pfizer-BradleyBare/HamiltonVisualMethodEditorConfiguration/raw/HAMILTON_STL_PPL2_MAM/BuildingBlocks/BuildingBlocks.xlsx""""" & """ -o """ & """""$home\OneDrive - Pfizer\Documents\_ABN\BuildingBlocks\BuildingBlocks.xlsx"""""""""
X = Shell(Command, vbHide)

Command = "POWERSHELL.exe -noexit " & """mkdir """ & """""$home\OneDrive - Pfizer\Documents\_ABN\HelpDocuments"""""
X = Shell(Command, vbHide)

Command = "POWERSHELL.exe -noexit " & """curl """ & """""https://github.com/Pfizer-BradleyBare/HamiltonVisualMethodEditor/raw/master/Help%20Documents/Methods%20Help%20Document.docx""""" & """ -o """ & """""$home\OneDrive - Pfizer\Documents\_ABN\HelpDocuments\Methods Help Document.docx"""""""""
X = Shell(Command, vbHide)

End Sub

Sub Ribbon_InstallInstallABN(control As IRibbonControl)

BuildingBlocksPath = Environ("USERPROFILE") & "\OneDrive - Pfizer\Documents\_ABN\BuildingBlocks\BuildingBlocks.xlsx"
ScriptPath = "C:\Program Files (x86)\HAMILTON\BAREB\Script\HamiltonVisualMethodEditor\HamiltonVisualMethodEditorConfiguration\BuildingBlocks\BuildingBlocks.xlsx"

If Dir(ScriptPath) <> "" Then
    MsgBox ("ABN Scripts are installed. You cannot install or update with this excel sheet. To update please contact an ABN SME")
    
ElseIf Dir(BuildingBlocksPath) <> "" Then
        MsgBox ("Building Blocks are already installed. If you want to update click the update button.")
Else
    Choice = MsgBox("This will only install the bare minimum to enable method building on your person PC. Click Ok to continue", vbOKCancel)
    If Choice = vbOK Then
        GetABNFiles
        MsgBox ("ABN blocks have been installed. Please close and reopen this workbook to load the blocks.")
    End If
End If

End Sub

Sub Ribbon_InstallUpdateABN(control As IRibbonControl)

BuildingBlocksPath = Environ("USERPROFILE") & "\OneDrive - Pfizer\Documents\_ABN\BuildingBlocks\BuildingBlocks.xlsx"
ScriptPath = "C:\Program Files (x86)\HAMILTON\BAREB\Script\HamiltonVisualMethodEditor\HamiltonVisualMethodEditorConfiguration\BuildingBlocks\BuildingBlocks.xlsx"

If Dir(ScriptPath) <> "" Then
    MsgBox ("ABN Scripts are installed. You cannot install or update with this excel sheet. To update please contact an ABN SME")
    
ElseIf Dir(BuildingBlocksPath) <> "" Then
    GetABNFiles
    MsgBox ("ABN blocks have been updated. Please close and reopen this workbook to load the updated blocks.")
Else
    MsgBox ("Building blocks are not installed yet. Please install first.")

End If

End Sub
