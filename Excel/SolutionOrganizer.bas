Attribute VB_Name = "SolutionOrganizer"
'Same as building blocks loader basically. Look at that and infer the purpose of this.

Public Sub LoadSolutions()

    If ThisWorkbook.Worksheets("BuildingBlocks").Cells(3, 6).Value <> "Categories" Then
        MsgBox ("Categories does not follow Solutions in the building blocks for " & StepString & ". Please contact an SME to repair the building blocks source.")
        GlobalBuildingBlockWorkingStatus = False
        Exit Sub
    End If
    GlobalSolutionCategoryString = ThisWorkbook.Worksheets("BuildingBlocks").Cells(3, 7).Value
    
    If ThisWorkbook.Worksheets("BuildingBlocks").Cells(4, 6).Value <> "Storage Temperatures" Then
        MsgBox ("Storage Temperatures does not follow Categories in the building blocks for " & StepString & ". Please contact an SME to repair the building blocks source.")
        GlobalBuildingBlockWorkingStatus = False
        Exit Sub
    End If
    GlobalSolutionStorageTemperatureString = ThisWorkbook.Worksheets("BuildingBlocks").Cells(4, 7).Value
    
    If ThisWorkbook.Worksheets("BuildingBlocks").Cells(5, 6).Value <> "Volatility Options" Then
        MsgBox ("Volatility Options does not follow Storage Temperatures in the building blocks for " & StepString & ". Please contact an SME to repair the building blocks source.")
        GlobalBuildingBlockWorkingStatus = False
        Exit Sub
    End If
    GlobalSolutionVolatilityOptionsString = ThisWorkbook.Worksheets("BuildingBlocks").Cells(5, 7).Value
'    GlobalSolutionVolatilityOptionsString = "Low,Medium,High,Very High"
    
    If ThisWorkbook.Worksheets("BuildingBlocks").Cells(6, 6).Value <> "Viscosity Options" Then
        MsgBox ("Viscosity Options does not follow Volatility Options in the building blocks for " & StepString & ". Please contact an SME to repair the building blocks source.")
        GlobalBuildingBlockWorkingStatus = False
        Exit Sub
    End If
    GlobalSolutionViscosityOptionsString = ThisWorkbook.Worksheets("BuildingBlocks").Cells(6, 7).Value
'    GlobalSolutionViscosityOptionsString = "Low,Medium,High,Very High"
    
    If ThisWorkbook.Worksheets("BuildingBlocks").Cells(7, 6).Value <> "Homogeneity Options" Then
        MsgBox ("Homogeneity Options does not follow Viscosity Options in the building blocks for " & StepString & ". Please contact an SME to repair the building blocks source.")
        GlobalBuildingBlockWorkingStatus = False
        Exit Sub
    End If
    GlobalSolutionHomogeneityOptionsString = ThisWorkbook.Worksheets("BuildingBlocks").Cells(7, 7).Value
'    GlobalSolutionHomogeneityOptionsString = "Homogenous,Heterogenous,Suspension,Emulsion"

    If ThisWorkbook.Worksheets("BuildingBlocks").Cells(8, 6).Value <> "Liquid Level Detection Options" Then
        MsgBox ("Liquid Level Detection Options does not follow Homogeneity Options in the building blocks for " & StepString & ". Please contact an SME to repair the building blocks source.")
        GlobalBuildingBlockWorkingStatus = False
        Exit Sub
    End If
    GlobalSolutionLLDOptionsString = ThisWorkbook.Worksheets("BuildingBlocks").Cells(8, 7).Value
'    GlobalSolutionHomogeneityOptionsString = "Normal,Organic"

    'First thing I want to do is pull the user options

    ReDim GlobalSolutionPresets(0)
    ReDim GlobalSolutionPresetVolatility(0)
    ReDim GlobalSolutionPresetViscosity(0)
    ReDim GlobalSolutionPresetHomogeneity(0)
    ReDim GlobalSolutionPresetLLD(0)
    
    SolutionPresetsCounter = 0
    For Counter = 1 To 1000
    
        If ThisWorkbook.Worksheets("BuildingBlocks").Cells(Counter, 6).Value = "Preset" Then
        
            ReDim Preserve GlobalSolutionPresets(SolutionPresetsCounter)
            ReDim Preserve GlobalSolutionPresetVolatility(SolutionPresetsCounter)
            ReDim Preserve GlobalSolutionPresetViscosity(SolutionPresetsCounter)
            ReDim Preserve GlobalSolutionPresetHomogeneity(SolutionPresetsCounter)
            ReDim Preserve GlobalSolutionPresetLLD(SolutionPresetsCounter)
            
            GlobalSolutionPresets(SolutionPresetsCounter) = ThisWorkbook.Worksheets("BuildingBlocks").Cells(Counter, 7).Value
        
            If ThisWorkbook.Worksheets("BuildingBlocks").Cells(Counter + 1, 6).Value <> "Volatility" Then
                MsgBox ("Volatility does not follow Preset in the building blocks for " & StepString & ". Please contact an SME to repair the building blocks source.")
                GlobalBuildingBlockWorkingStatus = False
                Exit Sub
            End If
            GlobalSolutionPresetVolatility(SolutionPresetsCounter) = ThisWorkbook.Worksheets("BuildingBlocks").Cells(Counter + 1, 7).Value

            If ThisWorkbook.Worksheets("BuildingBlocks").Cells(Counter + 2, 6).Value <> "Viscosity" Then
                MsgBox ("Viscosity does not follow Volatility in the building blocks for " & StepString & ". Please contact an SME to repair the building blocks source.")
                GlobalBuildingBlockWorkingStatus = False
                Exit Sub
            End If
            GlobalSolutionPresetViscosity(SolutionPresetsCounter) = ThisWorkbook.Worksheets("BuildingBlocks").Cells(Counter + 2, 7).Value

            If ThisWorkbook.Worksheets("BuildingBlocks").Cells(Counter + 3, 6).Value <> "Homogeneity" Then
                MsgBox ("Homogeneity does not follow Viscosity in the building blocks for " & StepString & ". Please contact an SME to repair the building blocks source.")
                GlobalBuildingBlockWorkingStatus = False
                Exit Sub
            End If
            GlobalSolutionPresetHomogeneity(SolutionPresetsCounter) = ThisWorkbook.Worksheets("BuildingBlocks").Cells(Counter + 3, 7).Value
            
            If ThisWorkbook.Worksheets("BuildingBlocks").Cells(Counter + 4, 6).Value <> "Liquid Level Detection" Then
                MsgBox ("Liquid Level Detection does not follow Homogeneity in the building blocks for " & StepString & ". Please contact an SME to repair the building blocks source.")
                GlobalBuildingBlockWorkingStatus = False
                Exit Sub
            End If
            GlobalSolutionPresetLLD(SolutionPresetsCounter) = ThisWorkbook.Worksheets("BuildingBlocks").Cells(Counter + 4, 7).Value
            
            SolutionPresetsCounter = SolutionPresetsCounter + 1
        End If
    
    Next Counter
    
    ReDim Preserve GlobalSolutionPresets(SolutionPresetsCounter)
    ReDim Preserve GlobalSolutionPresetVolatility(SolutionPresetsCounter)
    ReDim Preserve GlobalSolutionPresetViscosity(SolutionPresetsCounter)
    ReDim Preserve GlobalSolutionPresetHomogeneity(SolutionPresetsCounter)
    
    GlobalSolutionPresets(SolutionPresetsCounter) = "Custom"
    
End Sub


Public Sub DeleteSolutions()
    ThisWorkbook.Worksheets("Solutions").Range(Cells(1, 1), Cells(2000, 100)).Delete
End Sub

Sub FindSolutions()
    ReDim GlobalDetectedSolutionNames(0)
    GlobalDetectedSolutionsCounter = 0

    For Counter = 0 To GlobalOrganizerNumActions
        ActionName = GlobalOrganizerActionName(Counter)
        SearchableActionName = Replace(ActionName, "DISABLED:", "")
        SearchableActionName = Replace(SearchableActionName, " - (Click Here to Update)", "")
        
        StepIndex = FindInArray(GlobalBuildingBlocksSteps, SearchableActionName)
    
        For Counter2 = 0 To GlobalBuildingBlocksNumParameters(StepIndex)

            If GlobalBuildingBlocksParametersIsSolution(Counter2, StepIndex) = True Then
                ReDim Preserve GlobalDetectedSolutionNames(GlobalDetectedSolutionsCounter)
                SolutionName = GlobalOrganizerActionArgs(Counter2, Counter)
                
                If InStr(1, GlobalOrganizerActionArgs(Counter2, Counter), "=") <> 0 Then
                    ThisWorkbook.Worksheets("Solutions").Cells(1, 1).Formula = GlobalOrganizerActionArgs(Counter2, Counter)
                    SolutionName = ThisWorkbook.Worksheets("Solutions").Cells(1, 1).Value
                End If

                'This bologna prevents duplicates
                SolutionName = CStr(SolutionName)
                SolutionIndex = FindInArray(GlobalDetectedSolutionNames, SolutionName)
                GlobalDetectedSolutionNames(GlobalDetectedSolutionsCounter) = SolutionName
                GlobalDetectedSolutionsCounter = GlobalDetectedSolutionsCounter + 1
                If SolutionIndex <> -1 Then
                    GlobalDetectedSolutionsCounter = GlobalDetectedSolutionsCounter - 1
                End If
                
            End If
        Next Counter2
    Next Counter
    
End Sub

Sub SaveSolutions()

    GlobalSolutionsValidated = True

    NumSolutions = 0
    ReDim GlobalStoredSolutionNames(0)
    ReDim GlobalStoredSolutionComments(0)
    ReDim GlobalStoredSolutionParams(20, 0)
    ReDim GlobalStoredSolutionArgsNotAcceptable(20, 0)
    ReDim GlobalStoredSolutionNotAcceptable(0)

    For Counter = 1 To 10000
        SolutionRow = 0
        SolutionCol = 0
        
        'We need to iterate until we don't find anything on the row. This allows for steps to be side by side after a split plate step.
        While True
        
            'Find it
            Dim Selection As Range
            Set Selection = ThisWorkbook.Worksheets("Solutions").Range(Cells(Counter, SolutionCol + 3), Cells(Counter, 100)).Find("Comments")
            If Selection Is Nothing Then
                'if we don't find anything anymore then we can leave
                GoTo EndSolutionsWhile
            Else
                SolutionRow = Selection.Row
                SolutionCol = Selection.Column - 2
            End If
            
            ReDim Preserve GlobalStoredSolutionNames(NumSolutions)
            ReDim Preserve GlobalStoredSolutionComments(NumSolutions)
            ReDim Preserve GlobalStoredSolutionParams(20, NumSolutions)
            ReDim Preserve GlobalStoredSolutionArgsNotAcceptable(20, NumSolutions)
            ReDim Preserve GlobalStoredSolutionNotAcceptable(NumSolutions)

            
            GlobalStoredSolutionNames(NumSolutions) = Replace(ThisWorkbook.Worksheets("Solutions").Cells(SolutionRow, SolutionCol).Value, " - (Click Here to Update)", "")
            GlobalStoredSolutionComments(NumSolutions) = ThisWorkbook.Worksheets("Solutions").Cells(SolutionRow + 1, SolutionCol + 2).Value
            GlobalStoredSolutionNotAcceptable(NumSolutions) = False

            
            'Category
            GlobalStoredSolutionParams(0, NumSolutions) = ThisWorkbook.Worksheets("Solutions").Cells(SolutionRow + 1, SolutionCol + 1).Value
            GlobalStoredSolutionArgsNotAcceptable(0, NumSolutions) = False
            If InStr(1, GlobalSolutionCategoryString, GlobalStoredSolutionParams(0, NumSolutions)) = 0 Then
                GlobalStoredSolutionArgsNotAcceptable(0, NumSolutions) = True
                GlobalStoredSolutionNotAcceptable(NumSolutions) = True
                GlobalSolutionsValidated = False
            End If
            
            'Temperature
            GlobalStoredSolutionParams(1, NumSolutions) = ThisWorkbook.Worksheets("Solutions").Cells(SolutionRow + 2, SolutionCol + 1).Value
            GlobalStoredSolutionArgsNotAcceptable(1, NumSolutions) = False
            If InStr(1, GlobalSolutionStorageTemperatureString, GlobalStoredSolutionParams(1, NumSolutions)) = 0 Then
                GlobalStoredSolutionArgsNotAcceptable(1, NumSolutions) = True
                GlobalStoredSolutionNotAcceptable(NumSolutions) = True
                GlobalSolutionsValidated = False
            End If
            
            'Volatility
            GlobalStoredSolutionParams(2, NumSolutions) = ThisWorkbook.Worksheets("Solutions").Cells(SolutionRow + 3, SolutionCol + 1).Value
            GlobalStoredSolutionArgsNotAcceptable(2, NumSolutions) = False
            If InStr(1, GlobalSolutionVolatilityOptionsString, GlobalStoredSolutionParams(2, NumSolutions)) = 0 Then
                GlobalStoredSolutionArgsNotAcceptable(2, NumSolutions) = True
                GlobalStoredSolutionNotAcceptable(NumSolutions) = True
                GlobalSolutionsValidated = False
            End If
            
            'Viscosity
            GlobalStoredSolutionParams(3, NumSolutions) = ThisWorkbook.Worksheets("Solutions").Cells(SolutionRow + 4, SolutionCol + 1).Value
            GlobalStoredSolutionArgsNotAcceptable(3, NumSolutions) = False
            If InStr(1, GlobalSolutionViscosityOptionsString, GlobalStoredSolutionParams(3, NumSolutions)) = 0 Then
                GlobalStoredSolutionArgsNotAcceptable(3, NumSolutions) = True
                GlobalStoredSolutionNotAcceptable(NumSolutions) = True
                GlobalSolutionsValidated = False
            End If
            
            'Homogeneity
            GlobalStoredSolutionParams(4, NumSolutions) = ThisWorkbook.Worksheets("Solutions").Cells(SolutionRow + 5, SolutionCol + 1).Value
            GlobalStoredSolutionArgsNotAcceptable(4, NumSolutions) = False
            If InStr(1, GlobalSolutionHomogeneityOptionsString, GlobalStoredSolutionParams(4, NumSolutions)) = 0 Then
                GlobalStoredSolutionArgsNotAcceptable(4, NumSolutions) = True
                GlobalStoredSolutionNotAcceptable(NumSolutions) = True
                GlobalSolutionsValidated = False
            End If
            
            'LLD
            GlobalStoredSolutionParams(5, NumSolutions) = ThisWorkbook.Worksheets("Solutions").Cells(SolutionRow + 6, SolutionCol + 1).Value
            GlobalStoredSolutionArgsNotAcceptable(5, NumSolutions) = False
            If InStr(1, GlobalSolutionLLDOptionsString, GlobalStoredSolutionParams(5, NumSolutions)) = 0 Then
                GlobalStoredSolutionArgsNotAcceptable(5, NumSolutions) = True
                GlobalStoredSolutionNotAcceptable(NumSolutions) = True
                GlobalSolutionsValidated = False
            End If
            
            NumSolutions = NumSolutions + 1
        Wend
EndSolutionsWhile:
    Next Counter
End Sub

Sub ValidateSolutions()

'I'm not sure I need to validate honestly
'This is instead performed in the save solutions step

End Sub

Sub PrintSolutions()

    Call QuickSort(GlobalDetectedSolutionNames, 0, UBound(GlobalDetectedSolutionNames) - 1)

    PrintRow = 2
    PrintCol = 2

    Counter = 0
    
    While Counter < GlobalDetectedSolutionsCounter
    
        'Merge
        Range(Cells(PrintRow, PrintCol), Cells(PrintRow, PrintCol + 1)).Merge
        Range(Cells(PrintRow + 1, PrintCol + 2), Cells(PrintRow + 6, PrintCol + 2)).Merge
        
        'Wrap comments text
        Range(Cells(PrintRow + 1, PrintCol + 2), Cells(PrintRow + 6, PrintCol + 2)).WrapText = True
    
        'Bold
        Range(Cells(PrintRow, PrintCol), Cells(PrintRow, PrintCol + 2)).Font.Bold = True
    
        'Font
        Range(Cells(PrintRow, PrintCol), Cells(PrintRow + 6, PrintCol + 2)).Font.Size = 11
        Range(Cells(PrintRow, PrintCol), Cells(PrintRow, PrintCol + 2)).Font.Size = 12
        Range(Cells(PrintRow, PrintCol), Cells(PrintRow + 6, PrintCol + 2)).Font.name = "Times New Roman"

        'Alignment
        Range(Cells(PrintRow, PrintCol), Cells(PrintRow + 6, PrintCol + 2)).HorizontalAlignment = xlCenter
        Range(Cells(PrintRow, PrintCol), Cells(PrintRow + 6, PrintCol + 2)).VerticalAlignment = xlCenter
        Range(Cells(PrintRow + 1, PrintCol), Cells(PrintRow + 6, PrintCol)).HorizontalAlignment = xlLeft
            
        ThisWorkbook.Worksheets("Solutions").Cells(PrintRow, PrintCol).Value = GlobalDetectedSolutionNames(Counter) & " - (Click Here to Update)"
        ThisWorkbook.Worksheets("Solutions").Cells(PrintRow, PrintCol + 2).Value = "Comments"
            
        ThisWorkbook.Worksheets("Solutions").Cells(PrintRow + 1, PrintCol).Value = "Solution Category"
        ThisWorkbook.Worksheets("Solutions").Cells(PrintRow + 2, PrintCol).Value = "Storage Temperature"
        ThisWorkbook.Worksheets("Solutions").Cells(PrintRow + 3, PrintCol).Value = "Volatility"
        ThisWorkbook.Worksheets("Solutions").Cells(PrintRow + 4, PrintCol).Value = "Viscosity"
        ThisWorkbook.Worksheets("Solutions").Cells(PrintRow + 5, PrintCol).Value = "Homogeneity"
        ThisWorkbook.Worksheets("Solutions").Cells(PrintRow + 6, PrintCol).Value = "Liquid Level Detection"
    
        Index = FindInArray(GlobalStoredSolutionNames, GlobalDetectedSolutionNames(Counter))
        PlateIndex = FindInArray(GlobalSolutionDetectedPlates, GlobalDetectedSolutionNames(Counter))
    
        If Index = -1 Then 'Not found
            ThisWorkbook.Worksheets("Solutions").Cells(PrintRow + 1, PrintCol + 1).Value = "General Reagent/Plate"
            ThisWorkbook.Worksheets("Solutions").Cells(PrintRow + 2, PrintCol + 1).Value = "Ambient"
            ThisWorkbook.Worksheets("Solutions").Cells(PrintRow + 3, PrintCol + 1).Value = "Low"
            ThisWorkbook.Worksheets("Solutions").Cells(PrintRow + 4, PrintCol + 1).Value = "Medium"
            ThisWorkbook.Worksheets("Solutions").Cells(PrintRow + 5, PrintCol + 1).Value = "Homogenous"
            ThisWorkbook.Worksheets("Solutions").Cells(PrintRow + 6, PrintCol + 1).Value = "Normal"
            ThisWorkbook.Worksheets("Solutions").Cells(PrintRow + 1, PrintCol + 2).Value = ""
        Else
            If GlobalStoredSolutionNotAcceptable(Index) <> False Then
                Range(Cells(PrintRow, PrintCol), Cells(PrintRow, PrintCol)).Interior.Color = HEXCOL2RGB("FF2400")
            End If
      
            ThisWorkbook.Worksheets("Solutions").Cells(PrintRow + 1, PrintCol + 1).Value = GlobalStoredSolutionParams(0, Index)
            If GlobalStoredSolutionArgsNotAcceptable(0, Index) <> False Then
                Range(Cells(PrintRow + 1, PrintCol + 1), Cells(PrintRow + 1, PrintCol + 1)).Interior.Color = HEXCOL2RGB("FF2400")
            End If
            ThisWorkbook.Worksheets("Solutions").Cells(PrintRow + 2, PrintCol + 1).Value = GlobalStoredSolutionParams(1, Index)
            If GlobalStoredSolutionArgsNotAcceptable(1, Index) <> False Then
                Range(Cells(PrintRow + 2, PrintCol + 1), Cells(PrintRow + 2, PrintCol + 1)).Interior.Color = HEXCOL2RGB("FF2400")
            End If
            ThisWorkbook.Worksheets("Solutions").Cells(PrintRow + 3, PrintCol + 1).Value = GlobalStoredSolutionParams(2, Index)
            If GlobalStoredSolutionArgsNotAcceptable(2, Index) <> False Then
                Range(Cells(PrintRow + 3, PrintCol + 1), Cells(PrintRow + 3, PrintCol + 1)).Interior.Color = HEXCOL2RGB("FF2400")
            End If
            ThisWorkbook.Worksheets("Solutions").Cells(PrintRow + 4, PrintCol + 1).Value = GlobalStoredSolutionParams(3, Index)
            If GlobalStoredSolutionArgsNotAcceptable(3, Index) <> False Then
                Range(Cells(PrintRow + 4, PrintCol + 1), Cells(PrintRow + 4, PrintCol + 1)).Interior.Color = HEXCOL2RGB("FF2400")
            End If
            ThisWorkbook.Worksheets("Solutions").Cells(PrintRow + 5, PrintCol + 1).Value = GlobalStoredSolutionParams(4, Index)
            If GlobalStoredSolutionArgsNotAcceptable(4, Index) <> False Then
                Range(Cells(PrintRow + 5, PrintCol + 1), Cells(PrintRow + 5, PrintCol + 1)).Interior.Color = HEXCOL2RGB("FF2400")
            End If
            ThisWorkbook.Worksheets("Solutions").Cells(PrintRow + 6, PrintCol + 1).Value = GlobalStoredSolutionParams(5, Index)
            If GlobalStoredSolutionArgsNotAcceptable(5, Index) <> False Then
                Range(Cells(PrintRow + 6, PrintCol + 1), Cells(PrintRow + 6, PrintCol + 1)).Interior.Color = HEXCOL2RGB("FF2400")
            End If
            ThisWorkbook.Worksheets("Solutions").Cells(PrintRow + 7, PrintCol + 1).Value = GlobalStoredSolutionParams(6, Index)
            If GlobalStoredSolutionArgsNotAcceptable(6, Index) <> False Then
                Range(Cells(PrintRow + 7, PrintCol + 1), Cells(PrintRow + 7, PrintCol + 1)).Interior.Color = HEXCOL2RGB("FF2400")
            End If
            ThisWorkbook.Worksheets("Solutions").Cells(PrintRow + 1, PrintCol + 2).Value = GlobalStoredSolutionComments(Index)
        End If
        
        For Counter2 = 1 To 6
            'Borders
            Range(Cells(PrintRow + Counter2, PrintCol), Cells(PrintRow + Counter2, PrintCol)).Borders(xlEdgeBottom).LineStyle = xlContinuous
            Range(Cells(PrintRow + Counter2, PrintCol), Cells(PrintRow + Counter2, PrintCol)).Borders(xlEdgeLeft).LineStyle = xlContinuous
            Range(Cells(PrintRow + Counter2, PrintCol), Cells(PrintRow + Counter2, PrintCol)).Borders(xlEdgeRight).LineStyle = xlContinuous
            Range(Cells(PrintRow + Counter2, PrintCol), Cells(PrintRow + Counter2, PrintCol)).Borders(xlEdgeTop).LineStyle = xlContinuous
        
            Range(Cells(PrintRow + Counter2, PrintCol + 1), Cells(PrintRow + Counter2, PrintCol + 1)).Borders(xlEdgeBottom).LineStyle = xlContinuous
            Range(Cells(PrintRow + Counter2, PrintCol + 1), Cells(PrintRow + Counter2, PrintCol + 1)).Borders(xlEdgeLeft).LineStyle = xlContinuous
            Range(Cells(PrintRow + Counter2, PrintCol + 1), Cells(PrintRow + Counter2, PrintCol + 1)).Borders(xlEdgeRight).LineStyle = xlContinuous
            Range(Cells(PrintRow + Counter2, PrintCol + 1), Cells(PrintRow + Counter2, PrintCol + 1)).Borders(xlEdgeTop).LineStyle = xlContinuous
        
            Range(Cells(PrintRow + Counter2, PrintCol + 2), Cells(PrintRow + Counter2, PrintCol + 2)).Borders(xlEdgeBottom).LineStyle = xlContinuous
            Range(Cells(PrintRow + Counter2, PrintCol + 2), Cells(PrintRow + Counter2, PrintCol + 2)).Borders(xlEdgeLeft).LineStyle = xlContinuous
            Range(Cells(PrintRow + Counter2, PrintCol + 2), Cells(PrintRow + Counter2, PrintCol + 2)).Borders(xlEdgeRight).LineStyle = xlContinuous
            Range(Cells(PrintRow + Counter2, PrintCol + 2), Cells(PrintRow + Counter2, PrintCol + 2)).Borders(xlEdgeTop).LineStyle = xlContinuous
        Next Counter2

        'Final Borders
        Range(Cells(PrintRow, PrintCol), Cells(PrintRow + 6, PrintCol + 2)).Borders(xlEdgeBottom).LineStyle = xlContinuous
        Range(Cells(PrintRow, PrintCol), Cells(PrintRow + 6, PrintCol + 2)).Borders(xlEdgeLeft).LineStyle = xlContinuous
        Range(Cells(PrintRow, PrintCol), Cells(PrintRow + 6, PrintCol + 2)).Borders(xlEdgeRight).LineStyle = xlContinuous
        Range(Cells(PrintRow, PrintCol), Cells(PrintRow + 6, PrintCol + 2)).Borders(xlEdgeTop).LineStyle = xlContinuous

        Range(Cells(PrintRow, PrintCol), Cells(PrintRow + 6, PrintCol + 2)).Borders(xlEdgeBottom).Weight = xlMedium
        Range(Cells(PrintRow, PrintCol), Cells(PrintRow + 6, PrintCol + 2)).Borders(xlEdgeLeft).Weight = xlMedium
        Range(Cells(PrintRow, PrintCol), Cells(PrintRow + 6, PrintCol + 2)).Borders(xlEdgeRight).Weight = xlMedium
        Range(Cells(PrintRow, PrintCol), Cells(PrintRow + 6, PrintCol + 2)).Borders(xlEdgeTop).Weight = xlMedium
        
        Range(Cells(PrintRow, PrintCol + 2), Cells(PrintRow + 6, PrintCol + 2)).Borders(xlEdgeLeft).Weight = xlMedium
        
        PrintCol = PrintCol + 4
        If PrintCol > 10 Then
            PrintCol = 2
            PrintRow = PrintRow + 8
        End If
    Counter = Counter + 1
    Wend
    
    For Col = 1 To 100
        With ThisWorkbook.Worksheets("Solutions").Columns(Col)
            .ColumnWidth = 5
        End With
    Next Col
    
    'Autofit cells so words fit
    ThisWorkbook.Worksheets("Solutions").Columns("A:ZZ").AutoFit
End Sub
