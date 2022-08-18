Attribute VB_Name = "PythonAccessibleModules"
'Fun fact. With XLWINGS the write function has super low priorty. So, to get around that I have to create a macro for each Python function I'd like to perform. Silly.

Sub Python_GetMethodValidatedStatus()
'This saves the user. If a method is made on a local PC but is run on a Hamilton PC we need to confirm the method can run before we start. This does that. If it is invalid then
'the python method will kill the Hamilotn method.


    Application.ScreenUpdating = False
    
    Dim Active As Worksheet
    Set Active = ActiveSheet

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
    Application.EnableEvents = True
    
    Active.Activate

    Application.ScreenUpdating = True
    
    If GlobalBuildingBlockWorkingStatus = False Then
        ThisWorkbook.Worksheets("BuildingBlocks").Cells(1, 1).Value = "Blocks"
        Exit Sub
    End If
    If GlobalOrganizerActionsValidated = False Then
        ThisWorkbook.Worksheets("BuildingBlocks").Cells(1, 1).Value = "Actions"
        Exit Sub
    End If
    If GlobalSolutionsValidated = False Then
        ThisWorkbook.Worksheets("BuildingBlocks").Cells(1, 1).Value = "Solutions"
        Exit Sub
    End If
    ThisWorkbook.Worksheets("BuildingBlocks").Cells(1, 1).Value = ""
End Sub

Sub PYTHON_CreateCriticalMessageBox(Message As String, Title As String)
    MsgBox Message, vbOKOnly + vbCritical, Title
End Sub

Sub PYTHON_CreateInformationMessageBox(Message As String, Title As String)
    MsgBox Message, vbInformation + vbOKOnly, Title
End Sub

Sub PYTHON_WriteSheet(Sheet As String, Row As Integer, Col As Integer, TextArray As Variant)

    Application.ScreenUpdating = False
    
    Dim Active As Worksheet
    Set Active = ActiveSheet
    
    ThisWorkbook.Worksheets(Sheet).Activate
    ThisWorkbook.Worksheets(Sheet).Range(Cells(Row, Col), Cells(Row + UBound(TextArray, 1), Col + UBound(TextArray, 2))).Value = TextArray
    
    Active.Activate
    

    Application.ScreenUpdating = True
End Sub

Sub PYTHON_SelectCell(Sheet, RowStart, ColStart)

    ThisWorkbook.Worksheets(Sheet).Activate
    ThisWorkbook.Worksheets(Sheet).Cells(RowStart, ColStart).Activate

End Sub

Sub PYTHON_CreateBorder(Sheet As String, RowStart As Integer, ColStart As Integer, RowEnd As Integer, ColEnd As Integer)

    Application.ScreenUpdating = False
    
    Dim Active As Worksheet
    Set Active = ActiveSheet
    
    ThisWorkbook.Worksheets(Sheet).Activate
    With Range(Cells(RowStart, ColStart), Cells(RowEnd, ColEnd)).Borders(xlEdgeBottom)
     .LineStyle = xlContinuous
     .Weight = xlMedium
    End With

    With Range(Cells(RowStart, ColStart), Cells(RowEnd, ColEnd)).Borders(xlEdgeTop)
     .LineStyle = xlContinuous
     .Weight = xlMedium
    End With

    With Range(Cells(RowStart, ColStart), Cells(RowEnd, ColEnd)).Borders(xlEdgeLeft)
     .LineStyle = xlContinuous
     .Weight = xlMedium
    End With

    With Range(Cells(RowStart, ColStart), Cells(RowEnd, ColEnd)).Borders(xlEdgeRight)
     .LineStyle = xlContinuous
     .Weight = xlMedium
    End With
    
    Active.Activate


    Application.ScreenUpdating = True
End Sub

Sub PYTHON_Merge(Sheet, RowStart, ColStart, RowEnd, ColEnd)

    Application.ScreenUpdating = False
    
    Dim Active As Worksheet
    Set Active = ActiveSheet

    ThisWorkbook.Worksheets(Sheet).Activate
    ThisWorkbook.Worksheets(Sheet).Range(Cells(RowStart, ColStart), Cells(RowEnd, ColEnd)).Merge
    
    Active.Activate


    Application.ScreenUpdating = True
End Sub

Sub PYTHON_FontSize(Sheet, RowStart, ColStart, RowEnd, ColEnd, FontSize)

    Application.ScreenUpdating = False
    
    Dim Active As Worksheet
    Set Active = ActiveSheet

    ThisWorkbook.Worksheets(Sheet).Activate
    ThisWorkbook.Worksheets(Sheet).Range(Cells(RowStart, ColStart), Cells(RowEnd, ColEnd)).Font.Size = FontSize
    
    Active.Activate


    Application.ScreenUpdating = True
End Sub

Sub PYTHON_Center(Sheet, RowStart, ColStart, RowEnd, ColEnd)

    Application.ScreenUpdating = False
    
    Dim Active As Worksheet
    Set Active = ActiveSheet

    ThisWorkbook.Worksheets(Sheet).Activate
    ThisWorkbook.Worksheets(Sheet).Range(Cells(RowStart, ColStart), Cells(RowEnd, ColEnd)).HorizontalAlignment = xlCenter
    
    Active.Activate


    Application.ScreenUpdating = True
End Sub

Sub PYTHON_AutoFit(Sheet, ColumnNumber)

    Application.ScreenUpdating = False
    
    Dim Active As Worksheet
    Set Active = ActiveSheet

    ThisWorkbook.Worksheets(Sheet).Activate
    ThisWorkbook.Worksheets(Sheet).Columns(ColumnNumber).AutoFit
    
    Active.Activate


    Application.ScreenUpdating = True
End Sub

Sub PYTHON_WrapText(Sheet, RowStart, ColStart, RowEnd, ColEnd)

    Application.ScreenUpdating = False
    
    Dim Active As Worksheet
    Set Active = ActiveSheet

    ThisWorkbook.Worksheets(Sheet).Activate
    ThisWorkbook.Worksheets(Sheet).Range(Cells(RowStart, ColStart), Cells(RowEnd, ColEnd)).WrapText = True
    
    Active.Activate

    Application.ScreenUpdating = True
End Sub

Sub PYTHON_CreateSheet(Sheet, AfterSheet)

    Application.ScreenUpdating = False
    
    Dim Active As Worksheet
    Set Active = ActiveSheet
    
    Application.DisplayAlerts = False
    On Error GoTo CreateSheet
    ThisWorkbook.Worksheets(Sheet).Activate
    On Error GoTo 0
    Application.DisplayAlerts = True
    Active.Activate
    Application.ScreenUpdating = True
    Exit Sub
CreateSheet:
    On Error GoTo 0
    Dim NewSheet As Worksheet
    Set NewSheet = ThisWorkbook.Worksheets.Add(After:=ThisWorkbook.Worksheets(AfterSheet))
    NewSheet.name = Sheet
    Application.DisplayAlerts = True
    
    Active.Activate


    Application.ScreenUpdating = True
End Sub

Sub PYTHON_DeleteSheet(Sheet)

    Application.ScreenUpdating = False

    Application.DisplayAlerts = False
    On Error Resume Next
    ThisWorkbook.Worksheets(Sheet).Delete
    On Error GoTo 0
    Application.DisplayAlerts = True

    Application.ScreenUpdating = True
End Sub
