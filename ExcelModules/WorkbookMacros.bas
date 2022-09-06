Attribute VB_Name = "WorkbookMacros"
Public Sub WorkbookOnOpen()
 
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False
    
    On Error Resume Next
    ThisWorkbook.Worksheets("BuildingBlocks").Delete
    On Error GoTo 0
    
    If ABNInstallType = "Complete" Then
        
        BuildingBlocksPath = ABNPath & "ABN\HamiltonVisualMethodEditorConfig\BuildingBlocks\BuildingBlocks.xlsx"
        
    ElseIf ABNInstallType = "Editor" Then
    
        BuildingBlocksPath = ABNPath & "BuildingBlocks\BuildingBlocks.xlsx"
    
    End If
    'Create correct building blocks paths based on install type
    
    Set closedBook = Workbooks.Open(BuildingBlocksPath)
    closedBook.Sheets("BuildingBlocks").Copy Before:=ThisWorkbook.Sheets(1)
    closedBook.Close SaveChanges:=False
    ThisWorkbook.Worksheets("BuildingBlocks").Visible = xlSheetHidden
    ThisWorkbook.Worksheets("Method").Activate
    'Load the bluilding blocks excel file as a sheet in the background

    LoadBuildingBlocks
    
    If GlobalBuildingBlockWorkingStatus = True Then
        'MsgBox ("Blocks are killin' it!")
    Else
        MsgBox ("There were issues found with the Building Blocks. You can either view this document as Read Only or, if you wanted to run the method, close the workbook and contact an Automation Bare Necessities SME to correct the issue.")
        Exit Sub
    End If
    'Load blocks, which validates them. Check blocks are valid
    
    Dim Selection As Range
    Set Selection = ThisWorkbook.Worksheets("Method").Range("A1:AZ100").Find("Comments")
    If Selection Is Nothing Then
        MsgBox ("Your Method sheet was completely empty. Either Sharon is using this tool or a huge error occured. Resetting Method sheet...")
        ResetMethod
        ThisWorkbook.Worksheets("Solutions").Activate
        LoadSolutions
        FindSolutions
        SaveSolutions
        DeleteSolutions
        ValidateSolutions
        PrintSolutions
        ThisWorkbook.Worksheets("Method").Activate
        Exit Sub
    Else
        SaveSteps
        DeleteMethod
        PrintSteps
    End If
    'Check methd sheet is not empty. Handle it. If not empty then validate steps
    
    If GlobalOrganizerActionsValidated = True Then
        ThisWorkbook.Worksheets("Worklist").Activate
        'MsgBox ("Ready to go, Chief!")
    Else
        ThisWorkbook.Worksheets("Method").Activate
        MsgBox ("There were issues found with the method. Please check the method sheet for red highlighted cells. Click the effected step to update and correct the errors.")
        Exit Sub
    End If
    'Handle validation

    ThisWorkbook.Worksheets("Solutions").Activate
    LoadSolutions
    FindSolutions
    SaveSolutions
    DeleteSolutions
    ValidateSolutions
    PrintSolutions
    
    If GlobalSolutionsValidated = True Then
        ThisWorkbook.Worksheets("Worklist").Activate
        'MsgBox ("Ready to go, Chief!")
    Else
        ThisWorkbook.Worksheets("Solutions").Activate
        MsgBox ("There were issues found with the Solutions. Please check the Solutions sheet for red highlighted cells. Click the effected Solution to update and correct the errors.")
        Exit Sub
    End If
    'Validate Solutions

    Application.ScreenUpdating = True
    Application.DisplayAlerts = True
    
End Sub

Public Sub WorkbookBeforeClose(Cancel As Boolean)
    CloseWordDocument
    
End Sub

