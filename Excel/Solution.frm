VERSION 5.00
Begin {C62A69F0-16DC-11CE-9E98-00AA00574A4F} Solution 
   Caption         =   "Solution Editor"
   ClientHeight    =   9120.001
   ClientLeft      =   120
   ClientTop       =   465
   ClientWidth     =   5730
   OleObjectBlob   =   "Solution.frx":0000
   ShowModal       =   0   'False
   StartUpPosition =   1  'CenterOwner
End
Attribute VB_Name = "Solution"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Sub DeterminePreset()
    
    For Counter = 0 To (UBound(Me.PresetsBox.List) - 1)
            If Me.ComboBox2.Value = GlobalSolutionPresetVolatility(Counter) And Me.ComboBox3.Value = GlobalSolutionPresetViscosity(Counter) And Me.ComboBox4.Value = GlobalSolutionPresetHomogeneity(Counter) And Me.ComboBox5.Value = GlobalSolutionPresetLLD(Counter) Then
                Me.PresetsBox.Value = Me.PresetsBox.List(Counter)
                Exit Sub
            End If
    Next Counter
    
    Me.PresetsBox.Value = "Custom"
    
End Sub

Private Sub CancelButton_Click()
    Me.Hide
End Sub

Private Sub ComboBox2_Change()
    DeterminePreset
End Sub
Private Sub ComboBox3_Change()
    DeterminePreset
End Sub
Private Sub ComboBox4_Change()
    DeterminePreset
End Sub

Private Sub ComboBox5_Change()
    DeterminePreset
End Sub

Private Sub Label5_Click()
    WordTools.OpenWordDocument
    WordTools.GotoBookmark ("MethodCreationSolutionsLoading")
End Sub

Private Sub Label6_Click()
    WordTools.OpenWordDocument
    WordTools.GotoBookmark ("MethodCreationSolutionsHandling")
End Sub

Private Sub PresetsBox_Change()
    Value = Me.PresetsBox.Value

    For Counter = 0 To UBound(GlobalSolutionPresets)
        If Value = GlobalSolutionPresets(Counter) And Value <> "Custom" Then
            Me.ComboBox2.Value = GlobalSolutionPresetVolatility(Counter)
            Me.ComboBox3.Value = GlobalSolutionPresetViscosity(Counter)
            Me.ComboBox4.Value = GlobalSolutionPresetHomogeneity(Counter)
            Me.ComboBox5.Value = GlobalSolutionPresetLLD(Counter)
            Exit Sub
        End If
    Next Counter

End Sub
Private Sub SaveButton_Click()

    Application.ScreenUpdating = False

    ThisWorkbook.Worksheets("Solutions").Cells(GlobalClickLocation.Row + 1, GlobalClickLocation.Column + 1).Value = Me.ComboBox0.Value
    ThisWorkbook.Worksheets("Solutions").Cells(GlobalClickLocation.Row + 2, GlobalClickLocation.Column + 1).Value = Me.ComboBox1.Value
    ThisWorkbook.Worksheets("Solutions").Cells(GlobalClickLocation.Row + 3, GlobalClickLocation.Column + 1).Value = Me.ComboBox2.Value
    ThisWorkbook.Worksheets("Solutions").Cells(GlobalClickLocation.Row + 4, GlobalClickLocation.Column + 1).Value = Me.ComboBox3.Value
    ThisWorkbook.Worksheets("Solutions").Cells(GlobalClickLocation.Row + 5, GlobalClickLocation.Column + 1).Value = Me.ComboBox4.Value
    ThisWorkbook.Worksheets("Solutions").Cells(GlobalClickLocation.Row + 6, GlobalClickLocation.Column + 1).Value = Me.ComboBox5.Value
    Me.Hide

    ThisWorkbook.Worksheets("Solutions").Activate
    SolutionOrganizer.LoadSolutions
    SolutionOrganizer.FindSolutions
    SolutionOrganizer.SaveSolutions
    SolutionOrganizer.DeleteSolutions
    SolutionOrganizer.ValidateSolutions
    SolutionOrganizer.PrintSolutions
    
    Application.ScreenUpdating = True

End Sub

Private Sub SolutionEditorLabel_Click()

End Sub

Public Sub UserForm_Initialize()

    Me.ComboBox0.List = Split(GlobalSolutionCategoryString, ",")

    Me.ComboBox1.List = Split(GlobalSolutionStorageTemperatureString, ",")

    Me.ComboBox2.List = Split(GlobalSolutionVolatilityOptionsString, ",")
    Me.ComboBox3.List = Split(GlobalSolutionViscosityOptionsString, ",")

    Me.ComboBox4.List = Split(GlobalSolutionHomogeneityOptionsString, ",")
    
    Me.ComboBox5.List = Split(GlobalSolutionLLDOptionsString, ",")
    
    Me.PresetsBox.List = GlobalSolutionPresets

    Me.SolutionEditorLabel.Caption = GlobalSolutionName
   
    'This loads user input, there can be errors. If so, we want to skip and continue with default values
    On Error Resume Next
    
    Me.ComboBox0.Value = "General Reagent"
    Me.ComboBox0.Value = ThisWorkbook.Worksheets("Solutions").Cells(GlobalClickLocation.Row + 1, GlobalClickLocation.Column + 1).Value
    
    Me.ComboBox1.Value = "Ambient"
    Me.ComboBox1.Value = ThisWorkbook.Worksheets("Solutions").Cells(GlobalClickLocation.Row + 2, GlobalClickLocation.Column + 1).Value
    
    Me.ComboBox2.Value = "Low"
    Me.ComboBox2.Value = ThisWorkbook.Worksheets("Solutions").Cells(GlobalClickLocation.Row + 3, GlobalClickLocation.Column + 1).Value
    
    Me.ComboBox3.Value = "Medium"
    Me.ComboBox3.Value = ThisWorkbook.Worksheets("Solutions").Cells(GlobalClickLocation.Row + 4, GlobalClickLocation.Column + 1).Value
    
    Me.ComboBox4.Value = "Homogenous"
    Me.ComboBox4.Value = ThisWorkbook.Worksheets("Solutions").Cells(GlobalClickLocation.Row + 5, GlobalClickLocation.Column + 1).Value
    
    Me.ComboBox5.Value = "Normal"
    Me.ComboBox5.Value = ThisWorkbook.Worksheets("Solutions").Cells(GlobalClickLocation.Row + 6, GlobalClickLocation.Column + 1).Value
    
    'Reset Error Handling
    On Error GoTo 0
 
    Me.PresetsBox.Value = "Custom"
    DeterminePreset

End Sub

