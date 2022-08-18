Attribute VB_Name = "BuildingBlocksLoader"
Public Sub LoadBuildingBlocks()

    'This loads the buildingblocks into variables and validates them. Variables for speed.

    ReDim GlobalBuildingBlocksSteps(0)

    StepCounter = 0
    For Counter = 1 To 1000
    
        If ThisWorkbook.Worksheets("BuildingBlocks").Cells(Counter, 2).Value = "Step" Then
            ReDim Preserve GlobalBuildingBlocksSteps(StepCounter)
                
            GlobalBuildingBlocksSteps(StepCounter) = ThisWorkbook.Worksheets("BuildingBlocks").Cells(Counter, 3).Value
                
            StepCounter = StepCounter + 1
        End If
    Next Counter
    
    StepCounter = StepCounter - 1
    
    If StepCounter = -1 Then
        GlobalBuildingBlockWorkingStatus = False
        Exit Sub
    End If
    
    Call QuickSort(GlobalBuildingBlocksSteps, 0, UBound(GlobalBuildingBlocksSteps))

    ReDim GlobalBuildingBlocksPathway(StepCounter)
    ReDim GlobalBuildingBlocksDisableable(StepCounter)
    ReDim GlobalBuildingBlocksColor(StepCounter)
    ReDim GlobalBuildingBlocksSupported(StepCounter)
    ReDim GlobalBuildingBlocksNumParameters(StepCounter)
    ReDim GlobalBuildingBlocksParameters(20, StepCounter)
    ReDim GlobalBuildingBlocksParametersInputTypes(20, StepCounter)
    ReDim GlobalBuildingBlocksParametersComboBoxOptions(20, StepCounter) As String
    ReDim GlobalBuildingBlocksParametersInitialValues(20, StepCounter)
    ReDim GlobalBuildingBlocksParametersIsSolution(20, StepCounter)
    ReDim GlobalBuildingBlocksStepHelpBookmarks(StepCounter)

    For Counter = 0 To UBound(GlobalBuildingBlocksSteps)
        StepString = GlobalBuildingBlocksSteps(Counter)
    
        Dim ChoiceLocation As Range
        Set ChoiceLocation = ThisWorkbook.Worksheets("BuildingBlocks").Range("C:C").Find(StepString, LookIn:=xlValues)
        ChoiceLocationRow = ChoiceLocation.Row
        ChoiceLocationCol = ChoiceLocation.Column - 1
        
        
        'Block descriptor parameters must go in a specific order. This is confirming that order
        If ThisWorkbook.Worksheets("BuildingBlocks").Cells(ChoiceLocationRow + 1, ChoiceLocationCol).Value <> "Category" Then
            MsgBox ("Disableable does not follow Step in the building blocks for " & StepString & ". Please contact an SME to repair the building blocks source.")
            GlobalBuildingBlockWorkingStatus = False
            Exit Sub
        End If
        GlobalBuildingBlocksPathway(Counter) = ThisWorkbook.Worksheets("BuildingBlocks").Cells(ChoiceLocationRow + 1, ChoiceLocationCol + 1).Value

        If ThisWorkbook.Worksheets("BuildingBlocks").Cells(ChoiceLocationRow + 2, ChoiceLocationCol).Value <> "Disableable" Then
            MsgBox ("Disableable does not follow Step in the building blocks for " & StepString & ". Please contact an SME to repair the building blocks source.")
            GlobalBuildingBlockWorkingStatus = False
            Exit Sub
        End If
        GlobalBuildingBlocksDisableable(Counter) = ThisWorkbook.Worksheets("BuildingBlocks").Cells(ChoiceLocationRow + 2, ChoiceLocationCol + 1).Value
        
        If ThisWorkbook.Worksheets("BuildingBlocks").Cells(ChoiceLocationRow + 3, ChoiceLocationCol).Value <> "Color (Hex Only)" Then
            MsgBox ("Color does not follow Disableable in the building blocks for " & StepString & ". Please contact an SME to repair the building blocks source.")
            GlobalBuildingBlockWorkingStatus = False
            Exit Sub
        End If
        GlobalBuildingBlocksColor(Counter) = ThisWorkbook.Worksheets("BuildingBlocks").Cells(ChoiceLocationRow + 3, ChoiceLocationCol + 1).Value
        
        If ThisWorkbook.Worksheets("BuildingBlocks").Cells(ChoiceLocationRow + 4, ChoiceLocationCol).Value <> "Supported?" Then
            MsgBox ("Supported does not follow Color in the building blocks for " & StepString & ". Please contact an SME to repair the building blocks source.")
            GlobalBuildingBlockWorkingStatus = False
            Exit Sub
        End If
        GlobalBuildingBlocksSupported(Counter) = ThisWorkbook.Worksheets("BuildingBlocks").Cells(ChoiceLocationRow + 4, ChoiceLocationCol + 1).Value
        
        If ThisWorkbook.Worksheets("BuildingBlocks").Cells(ChoiceLocationRow + 5, ChoiceLocationCol).Value <> "BookmarkName" Then
            MsgBox ("Bookmark Name does not follow Supported in the building blocks for " & StepString & ". Please contact an SME to repair the building blocks source.")
            GlobalBuildingBlockWorkingStatus = False
            Exit Sub
        End If
        GlobalBuildingBlocksStepHelpBookmarks(Counter) = ThisWorkbook.Worksheets("BuildingBlocks").Cells(ChoiceLocationRow + 5, ChoiceLocationCol + 1).Value
    
        ParameterCounter = 0
        For Counter2 = 1 To 1000 'This works but really should be dynamic. I'll fix it eventually. LOW Priority.
            
            'This reads in the acceptable inputs for a given parameter. Same deal, must be in a specific order.
            If ThisWorkbook.Worksheets("BuildingBlocks").Cells(ChoiceLocationRow + Counter2, ChoiceLocationCol).Value = "Parameter" Then
                
                ParameterString = ThisWorkbook.Worksheets("BuildingBlocks").Cells(ChoiceLocationRow + Counter2, ChoiceLocationCol + 1).Value
                
                GlobalBuildingBlocksParameters(ParameterCounter, Counter) = ParameterString
                
                If ThisWorkbook.Worksheets("BuildingBlocks").Cells(ChoiceLocationRow + Counter2 + 1, ChoiceLocationCol).Value <> "Input Type" Then
                    MsgBox ("Input Type does not follow Parameter in the building blocks for " & StepString & "->" & ParameterString & ". Please contact an SME to repair the building blocks source.")
                    GlobalBuildingBlockWorkingStatus = False
                    Exit Sub
                End If

                GlobalBuildingBlocksParametersInputTypes(ParameterCounter, Counter) = ThisWorkbook.Worksheets("BuildingBlocks").Cells(ChoiceLocationRow + Counter2 + 1, ChoiceLocationCol + 1).Value
                GlobalBuildingBlocksParametersComboBoxOptions(ParameterCounter, Counter) = ThisWorkbook.Worksheets("BuildingBlocks").Cells(ChoiceLocationRow + Counter2 + 1, ChoiceLocationCol + 2).Value

                If ThisWorkbook.Worksheets("BuildingBlocks").Cells(ChoiceLocationRow + Counter2 + 2, ChoiceLocationCol).Value <> "Initial Value" Then
                    MsgBox ("Initial Value does not follow Input Type in the building blocks for " & StepString & "->" & ParameterString & ". Please contact an SME to repair the building blocks source.")
                    GlobalBuildingBlockWorkingStatus = False
                    Exit Sub
                End If

                GlobalBuildingBlocksParametersInitialValues(ParameterCounter, Counter) = ThisWorkbook.Worksheets("BuildingBlocks").Cells(ChoiceLocationRow + Counter2 + 2, ChoiceLocationCol + 1).Value

                If ThisWorkbook.Worksheets("BuildingBlocks").Cells(ChoiceLocationRow + Counter2 + 3, ChoiceLocationCol).Value <> "Is Argument Solution?" Then
                    MsgBox ("Is Argument Solution? does not follow Initial Value in the building blocks for " & StepString & "->" & ParameterString & ". Please contact an SME to repair the building blocks source.")
                    GlobalBuildingBlockWorkingStatus = False
                    Exit Sub
                End If
                
                GlobalBuildingBlocksParametersIsSolution(ParameterCounter, Counter) = ThisWorkbook.Worksheets("BuildingBlocks").Cells(ChoiceLocationRow + Counter2 + 3, ChoiceLocationCol + 1).Value
                
                ParameterCounter = ParameterCounter + 1
            End If
            
            If ThisWorkbook.Worksheets("BuildingBlocks").Cells(ChoiceLocationRow + Counter2, ChoiceLocationCol).Value = "Step" Then
                Exit For
            End If
            
        Next Counter2
        
        GlobalBuildingBlocksNumParameters(Counter) = ParameterCounter
        
    Next Counter
    
    GlobalBuildingBlockWorkingStatus = True
End Sub
