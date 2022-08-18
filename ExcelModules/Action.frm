VERSION 5.00
Begin {C62A69F0-16DC-11CE-9E98-00AA00574A4F} Action 
   Caption         =   "Action Creator"
   ClientHeight    =   12645
   ClientLeft      =   120
   ClientTop       =   465
   ClientWidth     =   6690
   OleObjectBlob   =   "Action.frx":0000
   ShowModal       =   0   'False
   StartUpPosition =   1  'CenterOwner
End
Attribute VB_Name = "Action"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Public Sub DeleteButton_Click()

    Me.Hide

    ThisWorkbook.Worksheets("Method").Activate

    Application.ScreenUpdating = False
    
    ClickRow = GlobalClickLocation.Row
    ClickCol = GlobalClickLocation.Column
    
    If InStr(1, ThisWorkbook.Worksheets("Method").Cells(ClickRow, ClickCol).Value, "Split Plate") <> 0 Then
        Answer = MsgBox("ATTENTION: Deleting a Split Plate Action will delete all actions that follow! Do you want to continue?", vbQuestion + vbYesNo + vbDefaultButton2)
        If Answer <> vbYes Then
            Exit Sub
        End If
    End If
    
    ThisWorkbook.Worksheets("Method").Cells(ClickRow, ClickCol).Value = ThisWorkbook.Worksheets("Method").Cells(ClickRow, ClickCol).Value & "DELETE"
    
    ActionOrganizer.SaveSteps
    ActionOrganizer.DeleteMethod
    ActionOrganizer.PrintSteps
    
    'I do it twice because it helps with formatting
    ActionOrganizer.SaveSteps
    ActionOrganizer.DeleteMethod
    ActionOrganizer.PrintSteps
    
    ThisWorkbook.Worksheets("Solutions").Activate
    SolutionOrganizer.FindSolutions
    SolutionOrganizer.SaveSolutions
    SolutionOrganizer.DeleteSolutions
    SolutionOrganizer.ValidateSolutions
    SolutionOrganizer.PrintSolutions
    
    ThisWorkbook.Worksheets("Method").Activate
        
    Application.ScreenUpdating = True

End Sub


Private Sub SaveButton_Click()
    
    Application.EnableEvents = True
    
    CheckFailed = False
    'First we want to check that all cells have a value.
    
    Counter = 0
    While Counter < UBound(GlobalNewActionArgs)
        Title = GlobalNewActionArgsTitles(Counter)
        Arg = GlobalNewActionArgs(Counter)
        
        'If step has an Step Enabled? param then we want to store it and remove it from the array
        If Title = "Step Enabled?" Then
            GlobalNewStepIsEnabled = Arg
            ReDim Preserve GlobalNewActionArgsTitles(UBound(GlobalNewActionArgs) - 1)
            ReDim Preserve GlobalNewActionArgs(UBound(GlobalNewActionArgs) - 1)
        Else
            If Arg = "" Then
                CheckFailed = True
            End If
        End If
        Counter = Counter + 1
    Wend
    
    'Now we need to tell the user they messed up
    If CheckFailed = True Then
        MsgBox ("All inputs must have a value. Please try again.")
        GlobalOldStepIsEnabled = GlobalNewStepIsEnabled
        GlobalOldActionName = GlobalNewActionName
        ReDim GlobalOldActionArgs(UBound(GlobalNewActionArgs))
        GlobalOldActionArgs = GlobalNewActionArgs
        Me.ActionChoice.Value = ""
        Me.ActionChoice.Value = GlobalOldActionName
        Application.EnableEvents = True
        Exit Sub
    End If
    
    If GlobalIsNewAction = True And GlobalNewActionName = "Split Plate" Then
        For Counter = 0 To 100
            If ThisWorkbook.Worksheets("Method").Cells(GlobalClickLocation.Row + Counter, GlobalClickLocation.Column).Value <> "" Then
                Me.ResetAll
                MsgBox ("You cannot insert a Split Plate step between two actions. Please add at the end of a step sequence.")
                Exit Sub
            End If
        Next Counter
    End If
        
    Me.Hide
    
    If GlobalNewStepIsEnabled = "Enabled" Then
    
    Else
        GlobalNewActionName = "DISABLED:" & GlobalNewActionName
    End If
    
    ThisWorkbook.Worksheets("Method").Activate
    
    Application.ScreenUpdating = False
    
    ClickRow = GlobalClickLocation.Row
    ClickCol = GlobalClickLocation.Column
    
    If GlobalIsNewAction = False Then
        ThisWorkbook.Worksheets("Method").Cells(ClickRow, ClickCol).Value = ThisWorkbook.Worksheets("Method").Cells(ClickRow, ClickCol).Value & "UPDATE"
    Else
        For Counter = 1 To 1000

            If InStr(1, ThisWorkbook.Worksheets("Method").Cells(ClickRow - Counter, ClickCol).Value, " - (Click Here to Update)") <> 0 Then
                ThisWorkbook.Worksheets("Method").Cells(ClickRow - Counter, ClickCol).Value = ThisWorkbook.Worksheets("Method").Cells(ClickRow - Counter, ClickCol).Value & "INSERT"
                Exit For
            End If
            
        Next Counter
        'were are finding the preceeding step so we can insert this step
    End If
    
    ThisWorkbook.Worksheets("Method").Activate
    
    ActionOrganizer.SaveSteps
    ActionOrganizer.DeleteMethod
    ActionOrganizer.PrintSteps
    
    'I do it twice because it helps with formatting
    ActionOrganizer.SaveSteps
    ActionOrganizer.DeleteMethod
    ActionOrganizer.PrintSteps
    
    ThisWorkbook.Worksheets("Solutions").Activate
    SolutionOrganizer.FindSolutions
    SolutionOrganizer.SaveSolutions
    SolutionOrganizer.DeleteSolutions
    SolutionOrganizer.ValidateSolutions
    SolutionOrganizer.PrintSolutions
    
    ThisWorkbook.Worksheets("Method").Activate
    Application.ScreenUpdating = True
    Application.EnableEvents = True
    

End Sub

Public Sub CancelButton_Click()

    Me.Hide
    ThisWorkbook.Worksheets("Method").Activate

End Sub

Private Sub ActionLabel_Click()
    Choice = Me.ActionChoice.Value
    If Choice = "" Then
        MsgBox ("Please choose an action before asking for help.")
    Else
        ChoiceIndex = Tools.FindInArray(GlobalBuildingBlocksSteps, Choice)
        BookmarkString = GlobalBuildingBlocksStepHelpBookmarks(ChoiceIndex)
        WordTools.OpenWordDocument
        WordTools.GotoBookmark (BookmarkString)
    End If
End Sub

Private Sub CategoryLabel_Click()
    Choice = Me.CategoryChoice.Value
    If Choice = "None" Then
        MsgBox ("Please choose a category before asking for help.")
    Else
        BookmarkString = "MethodCreationBlocks" & Choice
        WordTools.OpenWordDocument
        WordTools.GotoBookmark (BookmarkString)
    End If
End Sub

Public Sub CategoryChoice_Change()
    Action.ResetAll
    
    Dim ListArray() As String
    SupportedCounter = -1
    For Counter = 0 To UBound(GlobalBuildingBlocksSteps)
        If GlobalBuildingBlocksSupported(Counter) = True And GlobalBuildingBlocksPathway(Counter) = Me.CategoryChoice.Value Or Me.CategoryChoice.Value = "None" Or Me.CategoryChoice.Value = "" Then
            SupportedCounter = SupportedCounter + 1
            ReDim Preserve ListArray(SupportedCounter)
            ListArray(SupportedCounter) = GlobalBuildingBlocksSteps(Counter)
        End If
    Next Counter
    
    Me.ActionChoice.List = ListArray
    
    Me.ActionChoice.Value = ""
End Sub

Public Sub ActionChoice_Change()

    Action.ResetAll

    Choice = Me.ActionChoice.Value
    GlobalNewActionName = Choice

    If Choice = "" Then
        Exit Sub
    End If

    If GlobalIsNewAction = True Then
        Me.ActionCreatorLabel.Caption = "Adding New Action"
        StepEnabled = "Enabled"
    Else
        If Choice = GlobalOldActionName Then
            Me.ActionCreatorLabel.Caption = "Modifying " & Choice & " Action"
            StepEnabled = GlobalOldStepIsEnabled
        Else
            If GlobalOldActionName <> "Split Plate" And Choice = "Split Plate" Then
                MsgBox ("You cannot change any step to a Split Plate step. Please use Add Action funciton instead.")
                Me.ActionChoice.Value = GlobalOldActionName
                Exit Sub
            End If
            Me.ActionCreatorLabel.Caption = "Changing " & GlobalOldActionName & " Action to"
            StepEnabled = "Enabled"
        End If
    End If

    Application.ScreenUpdating = False
    
    Me.ButtonsVisibility (False)
    
    ChoiceIndex = Tools.FindInArray(GlobalBuildingBlocksSteps, Choice)
    NumParameters = GlobalBuildingBlocksNumParameters(ChoiceIndex)
    
    ReDim GlobalNewActionArgs(NumParameters)
    ReDim GlobalNewActionArgsTitles(NumParameters)
    
    For Counter = 0 To NumParameters - 1
    
        Me.Controls("AutoLabel" & Trim(Str(Counter))).Visible = True
        Title = GlobalBuildingBlocksParameters(Counter, ChoiceIndex)
        GlobalNewActionArgsTitles(Counter) = Title
        Me.Controls("AutoLabel" & Trim(Str(Counter))).Caption = Title
        
        InputType = GlobalBuildingBlocksParametersInputTypes(Counter, ChoiceIndex)

        If Choice <> GlobalOldActionName Then
            InitialValue = GlobalBuildingBlocksParametersInitialValues(Counter, ChoiceIndex)
        Else
            InitialValue = GlobalOldActionArgs(Counter)
        End If
        
            If InputType = "TextBox" Then
                Me.Controls("AutoTextBox" & Trim(Str(Counter))).Visible = True
                Me.Controls("AutoTextBox" & Trim(Str(Counter))).ShowDropButtonWhen = fmShowDropButtonWhenAlways
                Me.Controls("AutoTextBox" & Trim(Str(Counter))).Value = InitialValue
                Me.Controls("AutoTextBox" & Trim(Str(Counter))).ControlTipText = "Please enter a value manually, or use the button to add a cell reference."
            ElseIf InputType = "ComboBox" Then
                Me.Controls("AutoComboBox" & Trim(Str(Counter))).Visible = True
                Me.Controls("AutoComboBox" & Trim(Str(Counter))).List = Split(GlobalBuildingBlocksParametersComboBoxOptions(Counter, ChoiceIndex), ",")
                Me.Controls("AutoComboBox" & Trim(Str(Counter))).Style = fmStyleDropDownList
                Me.Controls("AutoComboBox" & Trim(Str(Counter))).Value = GlobalBuildingBlocksParametersInitialValues(Counter, ChoiceIndex)
                'Hacking the error handling to do what I need, Ahoy!!
                On Error Resume Next
                Me.Controls("AutoComboBox" & Trim(Str(Counter))).Value = InitialValue
                On Error GoTo 0
                Me.Controls("AutoComboBox" & Trim(Str(Counter))).ControlTipText = "Please choose a value from the dropdown"
            ElseIf InputType = "UserComboBox" Then
                Me.Controls("AutoComboBox" & Trim(Str(Counter))).Visible = True
                Me.Controls("AutoComboBox" & Trim(Str(Counter))).List = Split(GlobalBuildingBlocksParametersComboBoxOptions(Counter, ChoiceIndex), ",")
                Me.Controls("AutoComboBox" & Trim(Str(Counter))).Style = fmStyleDropDownCombo
                Me.Controls("AutoComboBox" & Trim(Str(Counter))).Value = InitialValue
                Me.Controls("AutoComboBox" & Trim(Str(Counter))).ControlTipText = "Please choose a value from the dropdown"
            Else
                Me.ResetAll
                MsgBox ("Input Type is incorrect for " & Choice & ". Please contact an SME to repair the building blocks source.")
                Exit Sub
            End If
        
    Next Counter
    
    If GlobalBuildingBlocksDisableable(ChoiceIndex) = True Then
        ReDim Preserve GlobalNewActionArgs(NumParameters + 1)
        ReDim Preserve GlobalNewActionArgsTitles(NumParameters + 1)
            
        Me.Controls("AutoLabel" & Trim(Str(NumParameters))).Visible = True
        Me.Controls("AutoLabel" & Trim(Str(NumParameters))).Caption = "Step Enabled?"
        GlobalNewActionArgsTitles(NumParameters) = "Step Enabled?"
    
        Me.Controls("AutoComboBox" & Trim(Str(NumParameters))).Visible = True
        Me.Controls("AutoComboBox" & Trim(Str(NumParameters))).List = Split("Enabled,Disabled", ",")
        Me.Controls("AutoComboBox" & Trim(Str(NumParameters))).Value = StepEnabled
        Me.Controls("AutoComboBox" & Trim(Str(NumParameters))).ControlTipText = "Please choose a value from the dropdown"
        NumParameters = NumParameters + 1
    Else
        GlobalNewStepIsEnabled = "Enabled"
    End If
    
    Me.ButtonsMoveTop (36 * (NumParameters))
    Me.FormIncreaseHeight (36 * (NumParameters))
    Me.ButtonsVisibility (True)
    
    Application.ScreenUpdating = True

End Sub

Public Sub UserForm_Initialize()
    
    Action.CategoryChoice.Value = ""
    
    Dim ListArray() As String
    ReDim ListArray(0)
    ListArray(0) = "ZZZZZZ" 'I need this to always be the last item.
    SupportedCounter = 0
    For Counter = 0 To UBound(GlobalBuildingBlocksPathway)
        If Tools.FindInArray(ListArray, GlobalBuildingBlocksPathway(Counter)) = -1 Then
            SupportedCounter = SupportedCounter + 1
            ReDim Preserve ListArray(SupportedCounter)
            ListArray(SupportedCounter) = GlobalBuildingBlocksPathway(Counter)
        End If
    Next Counter
    
    Call Tools.QuickSort(ListArray, 0, UBound(ListArray))
    
    Dim FinalArray()
    ReDim FinalArray(UBound(ListArray))

    For Counter = 0 To UBound(ListArray) - 1
        FinalArray(1 + Counter) = ListArray(Counter)
    Next Counter
    FinalArray(0) = "None"
    
    Me.CategoryChoice.List = FinalArray
    Me.CategoryChoice.Value = "None"
    
End Sub

Public Sub ResetAll()

    ReDim GlobalNewActionArgs(12)

    Me.AutoLabel0.Visible = False
    Me.AutoLabel1.Visible = False
    Me.AutoLabel2.Visible = False
    Me.AutoLabel3.Visible = False
    Me.AutoLabel4.Visible = False
    Me.AutoLabel5.Visible = False
    Me.AutoLabel6.Visible = False
    Me.AutoLabel7.Visible = False
    Me.AutoLabel8.Visible = False
    Me.AutoLabel9.Visible = False
    Me.AutoLabel10.Visible = False
    Me.AutoLabel11.Visible = False
    Me.AutoLabel12.Visible = False
    
    Me.AutoTextBox0.Visible = False
    Me.AutoTextBox1.Visible = False
    Me.AutoTextBox2.Visible = False
    Me.AutoTextBox3.Visible = False
    Me.AutoTextBox4.Visible = False
    Me.AutoTextBox5.Visible = False
    Me.AutoTextBox6.Visible = False
    Me.AutoTextBox7.Visible = False
    Me.AutoTextBox8.Visible = False
    Me.AutoTextBox9.Visible = False
    Me.AutoTextBox10.Visible = False
    Me.AutoTextBox11.Visible = False
    Me.AutoTextBox12.Visible = False
    
    Me.AutoTextBox0.Value = ""
    Me.AutoTextBox1.Value = ""
    Me.AutoTextBox2.Value = ""
    Me.AutoTextBox3.Value = ""
    Me.AutoTextBox4.Value = ""
    Me.AutoTextBox5.Value = ""
    Me.AutoTextBox6.Value = ""
    Me.AutoTextBox7.Value = ""
    Me.AutoTextBox8.Value = ""
    Me.AutoTextBox9.Value = ""
    Me.AutoTextBox10.Value = ""
    Me.AutoTextBox11.Value = ""
    Me.AutoTextBox12.Value = ""
    
    Me.AutoTextBox0.DropButtonStyle = fmDropButtonStyleReduce
    Me.AutoTextBox1.DropButtonStyle = fmDropButtonStyleReduce
    Me.AutoTextBox2.DropButtonStyle = fmDropButtonStyleReduce
    Me.AutoTextBox3.DropButtonStyle = fmDropButtonStyleReduce
    Me.AutoTextBox4.DropButtonStyle = fmDropButtonStyleReduce
    Me.AutoTextBox5.DropButtonStyle = fmDropButtonStyleReduce
    Me.AutoTextBox6.DropButtonStyle = fmDropButtonStyleReduce
    Me.AutoTextBox7.DropButtonStyle = fmDropButtonStyleReduce
    Me.AutoTextBox8.DropButtonStyle = fmDropButtonStyleReduce
    Me.AutoTextBox9.DropButtonStyle = fmDropButtonStyleReduce
    Me.AutoTextBox10.DropButtonStyle = fmDropButtonStyleReduce
    Me.AutoTextBox11.DropButtonStyle = fmDropButtonStyleReduce
    Me.AutoTextBox12.DropButtonStyle = fmDropButtonStyleReduce
    
    Me.AutoTextBox0.ShowDropButtonWhen = fmShowDropButtonWhenNever
    Me.AutoTextBox1.ShowDropButtonWhen = fmShowDropButtonWhenNever
    Me.AutoTextBox2.ShowDropButtonWhen = fmShowDropButtonWhenNever
    Me.AutoTextBox3.ShowDropButtonWhen = fmShowDropButtonWhenNever
    Me.AutoTextBox4.ShowDropButtonWhen = fmShowDropButtonWhenNever
    Me.AutoTextBox5.ShowDropButtonWhen = fmShowDropButtonWhenNever
    Me.AutoTextBox6.ShowDropButtonWhen = fmShowDropButtonWhenNever
    Me.AutoTextBox7.ShowDropButtonWhen = fmShowDropButtonWhenNever
    Me.AutoTextBox8.ShowDropButtonWhen = fmShowDropButtonWhenNever
    Me.AutoTextBox9.ShowDropButtonWhen = fmShowDropButtonWhenNever
    Me.AutoTextBox10.ShowDropButtonWhen = fmShowDropButtonWhenNever
    Me.AutoTextBox11.ShowDropButtonWhen = fmShowDropButtonWhenNever
    Me.AutoTextBox12.ShowDropButtonWhen = fmShowDropButtonWhenNever
    
    Me.AutoComboBox0.Visible = False
    Me.AutoComboBox1.Visible = False
    Me.AutoComboBox2.Visible = False
    Me.AutoComboBox3.Visible = False
    Me.AutoComboBox4.Visible = False
    Me.AutoComboBox5.Visible = False
    Me.AutoComboBox6.Visible = False
    Me.AutoComboBox7.Visible = False
    Me.AutoComboBox8.Visible = False
    Me.AutoComboBox9.Visible = False
    Me.AutoComboBox10.Visible = False
    Me.AutoComboBox11.Visible = False
    Me.AutoComboBox12.Visible = False
    
    Me.AutoComboBox0.Value = ""
    Me.AutoComboBox1.Value = ""
    Me.AutoComboBox2.Value = ""
    Me.AutoComboBox3.Value = ""
    Me.AutoComboBox4.Value = ""
    Me.AutoComboBox5.Value = ""
    Me.AutoComboBox6.Value = ""
    Me.AutoComboBox7.Value = ""
    Me.AutoComboBox8.Value = ""
    Me.AutoComboBox9.Value = ""
    Me.AutoComboBox10.Value = ""
    Me.AutoComboBox11.Value = ""
    Me.AutoComboBox12.Value = ""
    
    ButtonsMoveTop (0)
    FormIncreaseHeight (0)
    
    ButtonsVisibility (False)
    Me.CancelButton.Visible = True

End Sub

Public Sub ButtonsVisibility(Visibility As Boolean)
    
    Me.CancelButton.Visible = Visibility
    
    If GlobalIsNewAction = False Then
        Me.DeleteButton.Visible = Visibility
    Else
        Me.DeleteButton.Visible = False
    End If
    
    Me.SaveButton.Visible = Visibility

End Sub

Public Sub ButtonsMoveTop(NumPixels As Double)

    Me.CancelButton.Top = 91 + NumPixels
    Me.DeleteButton.Top = 91 + NumPixels
    Me.SaveButton.Top = 91 + NumPixels
End Sub

Public Sub FormIncreaseHeight(NumPixels As Double)

    Me.Height = 155 + NumPixels

End Sub

'When we click on a step or add step button, we want to do the following:
'1. The form should popup
'2. If it is an add step function, then the form is the default size, awaiting step selection
'2. Else it is an update step function, then the form is in the step state, with the parameters updated according to the current entries in the sheet


Private Sub AutoTextBox0_DropButtonClick()

    Me.Hide
    
    Output = Tools.AltRefEdit("Cell Reference Selector", "single cell")
    
    If Output = "" Then
    
    Else
    
        Me.AutoTextBox0.Value = Output
    
    End If
    
    Me.Show
    
End Sub

Private Sub AutoTextBox1_DropButtonClick()

    Me.Hide
    
    Output = Tools.AltRefEdit("Cell Reference Selector", "single cell")
    
    If Output = "" Then
    
    Else
    
        Me.AutoTextBox1.Value = Output
    
    End If
    
    Me.Show
    
End Sub

Private Sub AutoTextBox2_DropButtonClick()

    Me.Hide
    
    Output = Tools.AltRefEdit("Cell Reference Selector", "single cell")
    
    If Output = "" Then
    
    Else
    
        Me.AutoTextBox2.Value = Output
    
    End If
    
    Me.Show
    
End Sub

Private Sub AutoTextBox3_DropButtonClick()

    Me.Hide
    
    Output = Tools.AltRefEdit("Cell Reference Selector", "single cell")
    
    If Output = "" Then
    
    Else
    
        Me.AutoTextBox3.Value = Output
    
    End If
    
    Me.Show
    
End Sub

Private Sub AutoTextBox4_DropButtonClick()

    Me.Hide
    
    Output = Tools.AltRefEdit("Cell Reference Selector", "single cell")
    
    If Output = "" Then
    
    Else
    
        Me.AutoTextBox4.Value = Output
    
    End If
    
    Me.Show
    
End Sub

Private Sub AutoTextBox5_DropButtonClick()

    Me.Hide
    
    Output = Tools.AltRefEdit("Cell Reference Selector", "single cell")
    
    If Output = "" Then
    
    Else
    
        Me.AutoTextBox5.Value = Output
    
    End If
    
    Me.Show
    
End Sub

Private Sub AutoTextBox6_DropButtonClick()

    Me.Hide
    
    Output = Tools.AltRefEdit("Cell Reference Selector", "single cell")
    
    If Output = "" Then
    
    Else
    
        Me.AutoTextBox6.Value = Output
    
    End If
    
    Me.Show
    
End Sub

Private Sub AutoTextBox7_DropButtonClick()

    Me.Hide
    
    Output = Tools.AltRefEdit("Cell Reference Selector", "single cell")
    
    If Output = "" Then
    
    Else
    
        Me.AutoTextBox7.Value = Output
    
    End If
    
    Me.Show
    
End Sub

Private Sub AutoTextBox8_DropButtonClick()

    Me.Hide
    
    Output = Tools.AltRefEdit("Cell Reference Selector", "single cell")
    
    If Output = "" Then
    
    Else
    
        Me.AutoTextBox8.Value = Output
    
    End If
    
    Me.Show
    
End Sub

Private Sub AutoTextBox9_DropButtonClick()

    Me.Hide
    
    Output = Tools.AltRefEdit("Cell Reference Selector", "single cell")
    
    If Output = "" Then
    
    Else
    
        Me.AutoTextBox9.Value = Output
    
    End If
    
    Me.Show
    
End Sub

Private Sub AutoTextBox10_DropButtonClick()

    Me.Hide
    
    Output = Tools.AltRefEdit("Cell Reference Selector", "single cell")
    
    If Output = "" Then
    
    Else
    
        Me.AutoTextBox10.Value = Output
    
    End If
    
    Me.Show
    
End Sub

Private Sub AutoTextBox11_DropButtonClick()

    Me.Hide
    
    Output = Tools.AltRefEdit("Cell Reference Selector", "single cell")
    
    If Output = "" Then
    
    Else
    
        Me.AutoTextBox11.Value = Output
    
    End If
    
    Me.Show
    
End Sub

Private Sub AutoTextBox12_DropButtonClick()

    Me.Hide
    
    Output = Tools.AltRefEdit("Cell Reference Selector", "single cell")
    
    If Output = "" Then
    
    Else
    
        Me.AutoTextBox12.Value = Output
    
    End If
    
    Me.Show
    
End Sub

Private Sub AutoComboBox0_Change()
    Value = Me.AutoComboBox0.Value
    If InStr(1, Value, "Reference") <> 0 Then
        Me.Hide
        Value = Tools.AltRefEdit("Cell Reference Selector", "single cell")
        Me.Show
    End If
    Me.AutoComboBox0.Value = Value
    GlobalNewActionArgs(0) = Value

End Sub

Private Sub AutoComboBox1_Change()
    Value = Me.AutoComboBox1.Value
    If InStr(1, Value, "Reference") <> 0 Then
        Me.Hide
        Value = Tools.AltRefEdit("Cell Reference Selector", "single cell")
        Me.Show
    End If
    Me.AutoComboBox1.Value = Value
    GlobalNewActionArgs(1) = Value
End Sub

Private Sub AutoComboBox2_Change()
    Value = Me.AutoComboBox2.Value
    If InStr(1, Value, "Reference") <> 0 Then
        Me.Hide
        Value = Tools.AltRefEdit("Cell Reference Selector", "single cell")
        Me.Show
    End If
    Me.AutoComboBox2.Value = Value
    GlobalNewActionArgs(2) = Value
End Sub

Private Sub AutoComboBox3_Change()
    Value = Me.AutoComboBox3.Value
    If InStr(1, Value, "Reference") <> 0 Then
        Me.Hide
        Value = Tools.AltRefEdit("Cell Reference Selector", "single cell")
        Me.Show
    End If
    Me.AutoComboBox3.Value = Value
    GlobalNewActionArgs(3) = Value
End Sub

Private Sub AutoComboBox4_Change()
    Value = Me.AutoComboBox4.Value
    If InStr(1, Value, "Reference") <> 0 Then
        Me.Hide
        Value = Tools.AltRefEdit("Cell Reference Selector", "single cell")
        Me.Show
    End If
    Me.AutoComboBox4.Value = Value
    GlobalNewActionArgs(4) = Value
End Sub

Private Sub AutoComboBox5_Change()
    Value = Me.AutoComboBox5.Value
    If InStr(1, Value, "Reference") <> 0 Then
        Me.Hide
        Value = Tools.AltRefEdit("Cell Reference Selector", "single cell")
        Me.Show
    End If
    Me.AutoComboBox5.Value = Value
    GlobalNewActionArgs(5) = Value
End Sub

Private Sub AutoComboBox6_Change()
    Value = Me.AutoComboBox6.Value
    If InStr(1, Value, "Reference") <> 0 Then
        Me.Hide
        Value = Tools.AltRefEdit("Cell Reference Selector", "single cell")
        Me.Show
    End If
    Me.AutoComboBox6.Value = Value
    GlobalNewActionArgs(6) = Value
End Sub

Private Sub AutoComboBox7_Change()
    Value = Me.AutoComboBox7.Value
    If InStr(1, Value, "Reference") <> 0 Then
        Me.Hide
        Value = Tools.AltRefEdit("Cell Reference Selector", "single cell")
        Me.Show
    End If
    Me.AutoComboBox7.Value = Value
    GlobalNewActionArgs(7) = Value
End Sub

Private Sub AutoComboBox8_Change()
    Value = Me.AutoComboBox8.Value
    If InStr(1, Value, "Reference") <> 0 Then
        Me.Hide
        Value = Tools.AltRefEdit("Cell Reference Selector", "single cell")
        Me.Show
    End If
    Me.AutoComboBox8.Value = Value
    GlobalNewActionArgs(8) = Value
End Sub

Private Sub AutoComboBox9_Change()
    Value = Me.AutoComboBox9.Value
    If InStr(1, Value, "Reference") <> 0 Then
        Me.Hide
        Value = Tools.AltRefEdit("Cell Reference Selector", "single cell")
        Me.Show
    End If
    Me.AutoComboBox9.Value = Value
    GlobalNewActionArgs(9) = Value
End Sub

Private Sub AutoComboBox10_Change()
    Value = Me.AutoComboBox10.Value
    If InStr(1, Value, "Reference") <> 0 Then
        Me.Hide
        Value = Tools.AltRefEdit("Cell Reference Selector", "single cell")
        Me.Show
    End If
    Me.AutoComboBox10.Value = Value
    GlobalNewActionArgs(10) = Value
End Sub

Private Sub AutoComboBox11_Change()
    Value = Me.AutoComboBox11.Value
    If InStr(1, Value, "Reference") <> 0 Then
        Me.Hide
        Value = Tools.AltRefEdit("Cell Reference Selector", "single cell")
        Me.Show
    End If
    Me.AutoComboBox11.Value = Value
    GlobalNewActionArgs(11) = Value
End Sub

Private Sub AutoComboBox12_Change()
    Value = Me.AutoComboBox12.Value
    If InStr(1, Value, "Reference") <> 0 Then
        Me.Hide
        Value = Tools.AltRefEdit("Cell Reference Selector", "single cell")
        Me.Show
    End If
    Me.AutoComboBox12.Value = Value
    GlobalNewActionArgs(12) = Value
End Sub

Private Sub AutoTextBox0_Change()
    GlobalNewActionArgs(0) = Me.AutoTextBox0.Value
End Sub

Private Sub AutoTextBox1_Change()
    GlobalNewActionArgs(1) = Me.AutoTextBox1.Value
End Sub

Private Sub AutoTextBox2_Change()
    GlobalNewActionArgs(2) = Me.AutoTextBox2.Value
End Sub

Private Sub AutoTextBox3_Change()
    GlobalNewActionArgs(3) = Me.AutoTextBox3.Value
End Sub

Private Sub AutoTextBox4_Change()
    GlobalNewActionArgs(4) = Me.AutoTextBox4.Value
End Sub

Private Sub AutoTextBox5_Change()
    GlobalNewActionArgs(5) = Me.AutoTextBox5.Value
End Sub

Private Sub AutoTextBox6_Change()
    GlobalNewActionArgs(6) = Me.AutoTextBox6.Value
End Sub

Private Sub AutoTextBox7_Change()
    GlobalNewActionArgs(7) = Me.AutoTextBox7.Value
End Sub

Private Sub AutoTextBox8_Change()
    GlobalNewActionArgs(8) = Me.AutoTextBox7.Value
End Sub

Private Sub AutoTextBox9_Change()
    GlobalNewActionArgs(9) = Me.AutoTextBox7.Value
End Sub

Private Sub AutoTextBox10_Change()
    GlobalNewActionArgs(10) = Me.AutoTextBox7.Value
End Sub

Private Sub AutoTextBox11_Change()
    GlobalNewActionArgs(11) = Me.AutoTextBox7.Value
End Sub

Private Sub AutoTextBox12_Change()
    GlobalNewActionArgs(12) = Me.AutoTextBox7.Value
End Sub
