Attribute VB_Name = "UserMacros"
Sub AddNewAction(ByVal Selection As Range)
    
    If GlobalBuildingBlockWorkingStatus = True Then
        'MsgBox ("Blocks are killin' it!")
    Else
        MsgBox ("Building Blocks sheets was not loaded correctly so this document is Read Only. Close and reopen the workbook with Macros enabled. Building Blocks will then be loaded automatically.")
        Exit Sub
    End If
    
    Set Selection = Range(Cells(Selection.Row, Selection.Column - 1), Cells(Selection.Row, Selection.Column - 1))

    Set GlobalClickLocation = Selection

    GlobalOldActionName = ""
    OldUnchangedActionName = GlobalOldActionName
    ReDim GlobalOldActionArgs(1)
    GlobalIsNewAction = True

    Action.UserForm_Initialize
    Action.CategoryChoice = ""
    Action.CategoryChoice = "None"
    Action.ActionChoice = "Plate"
    Action.ActionChoice = GlobalOldActionName
    Action.Show

End Sub

Sub UpdateAction(ByVal Selection As Range)

    If GlobalBuildingBlockWorkingStatus = True Then
        'MsgBox ("Blocks are killin' it!")
    Else
        MsgBox ("Building Blocks sheets was not loaded correctly so this document is Read Only. Close and reopen the workbook with Macros enabled. Building Blocks will then be loaded automatically.")
        Exit Sub
    End If

    Set GlobalClickLocation = Selection

    GlobalOldActionName = Left(Selection.Value, InStr(1, Selection.Value, " - ") - 1)
    
    If InStr(1, Selection.Value, "DISABLED:") <> 0 Then
        GlobalOldStepIsEnabled = "Disabled"
        GlobalOldActionName = Replace(GlobalOldActionName, "DISABLED:", "")
    Else
        GlobalOldStepIsEnabled = "Enabled"
    End If
    
    OldUnchangedActionName = GlobalOldActionName
    
    NumArgs = 0
    For Counter = 0 To 1000
       
        Value = ThisWorkbook.Worksheets("Method").Cells(Selection.Row + 1 + Counter, Selection.Column).Formula
       
        If Value <> "" Then
            NumArgs = NumArgs + 1
        Else
            Exit For
        End If
    Next Counter
    
    ReDim GlobalOldActionArgs(NumArgs)
    
    For Counter = 0 To NumArgs
        GlobalOldActionArgs(Counter) = ThisWorkbook.Worksheets("Method").Cells(Selection.Row + 1 + Counter, Selection.Column + 1).Formula
    Next Counter
    GlobalIsNewAction = True 'I have to do this so it ignores the previous split plate selection.
    Action.UserForm_Initialize
    
    On Error GoTo ExitUserUpdate
    Action.CategoryChoice = ""
    Action.CategoryChoice = "None"
    Action.CategoryChoice = GlobalBuildingBlocksPathway(FindInArray(GlobalBuildingBlocksSteps, GlobalOldActionName))
    GlobalIsNewAction = False 'switch to false before the final step so the user sees the modifying step text. This has to be here!
    Action.ActionChoice = GlobalOldActionName
    Action.Show
    Exit Sub

ExitUserUpdate:
    On Error GoTo 0
    Response = MsgBox("Unfortunately, this action is not supported on this system. Press OK to delete the action or Cancel to return.", vbOKCancel)
    If Response = vbOK Then
        Action.DeleteButton_Click
    End If
End Sub

Sub UpdateSolution(ByVal Selection As Range)

    If GlobalBuildingBlockWorkingStatus = True Then
        'MsgBox ("Blocks are killin' it!")
    Else
        MsgBox ("Building Blocks sheets was not loaded correctly so this document is Read Only. Close and reopen the workbook with Macros enabled. Building Blocks will then be loaded automatically.")
        Exit Sub
    End If

    Set GlobalClickLocation = Selection

    GlobalSolutionName = Left(Selection.Value, InStr(1, Selection.Value, " - ") - 1)

    Solution.UserForm_Initialize
    Solution.Show

End Sub
