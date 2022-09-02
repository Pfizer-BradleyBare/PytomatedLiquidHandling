Attribute VB_Name = "ActionOrganizer"
Public Sub ValidateSteps()
    GlobalOrganizerActionsValidated = True

    Counter = 0
    Do
        StartRow = GlobalOrganizerActionPrintRow(Counter)
        
        If StartRow >= 0 Then
    
            'We need to get the action Name
            ActionName = Replace(GlobalOrganizerActionName(Counter), " - (Click Here to Update)", "")
            ActionName = Replace(ActionName, "DISABLED:", "")
        
            'Lets search for it in our building blocks
            ChoiceIndex = FindInArray(GlobalBuildingBlocksSteps, ActionName)
            
            'Now we can confirm the titles and arguments are acceptable
            NumParamsBuildingBlocks = GlobalBuildingBlocksNumParameters(ChoiceIndex)
            NumParamsSavedAction = GlobalOrgnizerActionNumArgs(Counter)
        
            If NumParamsBuildingBlocks <> NumParamsSavedAction Then
                GlobalOrganizerActionNotAcceptable(Counter) = True
            End If
            'Assume all inputs are valid at the beginning
        
            NumParams = NumParamsBuildingBlocks
            If NumParamsSavedAction > NumParams Then
                NumParams = NumParamsSavedAction
            End If
            'Truncate inputs to length of block input length

            For Counter2 = 0 To NumParams - 1
            
                If GlobalBuildingBlocksParameters(Counter2, ChoiceIndex) <> GlobalOrganizerActionArgsTitles(Counter2, Counter) Then
                    GlobalOrganizerActionArgsTitlesNotAcceptable(Counter2, Counter) = True
                    GlobalOrganizerActionNotAcceptable(Counter) = True
                    GlobalOrganizerActionsValidated = False
                End If
            
                If GlobalBuildingBlocksParametersInputTypes(Counter2, ChoiceIndex) = "ComboBox" Then
                    If FindInArray(Split(GlobalBuildingBlocksParametersComboBoxOptions(Counter2, ChoiceIndex), ","), GlobalOrganizerActionArgs(Counter2, Counter)) = -1 Then
                        GlobalOrganizerActionArgsNotAcceptable(Counter2, Counter) = True
                        GlobalOrganizerActionNotAcceptable(Counter) = True
                        GlobalOrganizerActionsValidated = False
                    End If
                End If
                
                If InStr(1, GlobalOrganizerActionArgs(Counter2, Counter), "#") <> 0 Then
                    GlobalOrganizerActionArgs(Counter2, Counter) = "Reference Bad or Missing"
                End If
                
                If GlobalOrganizerActionArgs(Counter2, Counter) = "Reference Bad or Missing" Then
                    GlobalOrganizerActionArgsNotAcceptable(Counter2, Counter) = True
                    GlobalOrganizerActionNotAcceptable(Counter) = True
                    GlobalOrganizerActionsValidated = False
                End If
                
            Next Counter2
            'Validate the inputs and arguments. Everything really. Always done in real time to save the users
        End If
        
ExitValidateDo:
        Counter = Counter + 1
    Loop While Counter <= GlobalOrganizerNumActions

End Sub

Public Sub DeleteMethod()

    ThisWorkbook.Worksheets("Method").Range(Cells(1, 1), Cells(2000, 100)).Delete

End Sub

Public Sub PlaceSteps(ByVal Index As Integer, ByVal NumSplitPlates As Integer, ByVal Offset As Integer, ByVal Row As Integer, ByVal Column As Integer)

    'This is a doozy. Basically this will attempt to place steps without overlap. This is a recursive function! Each time a split plate step is found the new pathways
    'will call a new PlaceSteps function. Repeat for all pathways

    Counter = Index
    
    While True
        'we can only deal with steps on the same pathway meaning the same offset
        If GlobalOrganizerActionHorizontalOffset(Counter) = Offset Then
            ActionName = GlobalOrganizerActionName(Counter)
    
            If InStr(1, ActionName, "DELETE") Then
                Row = -999
            End If
    
            GlobalOrganizerActionPrintRow(Counter) = Row
            GlobalOrganizerActionPrintCol(Counter) = Column
            Row = Row + GlobalOrgnizerActionNumArgs(Counter) + 4
    
            If InStr(1, ActionName, "Split Plate") <> 0 Then
                If NumSplitPlates + 1 > GlobalOrganizerNumSplitSeperators Then
                    GlobalOrganizerNumSplitSeperators = NumSplitPlates + 1
                End If
    
                
                RowOfInterest = GlobalOrganizerActionRowDetected(Counter) + 5
                Distance = 999
                NewFirstOffset = 999
                Counter2 = 1
                Do
                    If GlobalOrganizerActionRowDetected(Counter + Counter2) = RowOfInterest Then
                        OffsetCalc = Abs(GlobalOrganizerActionHorizontalOffset(Counter + Counter2) - GlobalOrganizerActionHorizontalOffset(Counter))
                        If OffsetCalc < Distance Then
                            Distance = OffsetCalc
                                NewFirstOffset = GlobalOrganizerActionHorizontalOffset(Counter + Counter2)
                        End If
                    End If
                    Counter2 = Counter2 + 1
                Loop While Counter + Counter2 < GlobalOrganizerNumActions + 1
                
                Distance = 999
                NewSecondOffset = 999
                Counter2 = 1
                Do
                    If GlobalOrganizerActionRowDetected(Counter + Counter2) = RowOfInterest And GlobalOrganizerActionHorizontalOffset(Counter + Counter2) <> NewFirstOffset Then
                        OffsetCalc = Abs(GlobalOrganizerActionHorizontalOffset(Counter + Counter2) - GlobalOrganizerActionHorizontalOffset(Counter))
                        If OffsetCalc < Distance Then
                            Distance = OffsetCalc
                                NewSecondOffset = GlobalOrganizerActionHorizontalOffset(Counter + Counter2)
                        End If
                    End If
                    Counter2 = Counter2 + 1
                Loop While Counter + Counter2 < GlobalOrganizerNumActions + 1
            
                'run on both split plate paths
                PlaceSteps Counter + 1, NumSplitPlates + 1, NewFirstOffset, Row - 2, Column - (2 * (GlobalOrganizerNumSplitSeperators - (NumSplitPlates + 1)))
                PlaceSteps Counter + 1, NumSplitPlates + 1, NewSecondOffset, Row - 2, Column + (2 * (GlobalOrganizerNumSplitSeperators - (NumSplitPlates + 1)))

                'exit this loop because we are done with this path
                GoTo ExitPlaceStepsWhile
            ElseIf InStr(1, ActionName, "Finish") <> 0 Then
                'exit this loop because we are done with this path
                GoTo ExitPlaceStepsWhile
            End If
        End If
        
        If Counter = GlobalOrganizerNumActions Then
            'exit because we are out of steps
            GoTo ExitPlaceStepsWhile
        End If
        Counter = Counter + 1
    Wend
ExitPlaceStepsWhile:
End Sub

Public Sub PrintSteps()
    
    GlobalOrganizerNumSplitSeperators = 0
    'This finds the preliminary row and col of our steps. The first call merely counts the numer of split plates on a per pathway basis
    PlaceSteps 0, 0, 0, 2, 4
    
    'I do it twice because it helps with formatting and doesn't cause speed issues. The second call takes into account the number of split plates to perform a proper placement
    GlobalOrganizerNumSplitSeperators = GlobalOrganizerNumSplitSeperators + 1
    PlaceSteps 0, 0, 0, 2, 4
    
    ValidateSteps

    'We need to shift the col if it is less than 2
    SmallestCol = 4
    For Counter = 0 To GlobalOrganizerNumActions
        If GlobalOrganizerActionPrintCol(Counter) < SmallestCol Then
            SmallestCol = GlobalOrganizerActionPrintCol(Counter)
        End If
    Next Counter
    
    Shift = 0
    'Figure out how much to shift
    If SmallestCol < 2 Then
        Shift = 3 - SmallestCol
    End If
    
    For Counter = 0 To GlobalOrganizerNumActions
            GlobalOrganizerActionPrintCol(Counter) = GlobalOrganizerActionPrintCol(Counter) + Shift
    Next Counter

    'Now we can start printing the steps out
    Counter = 0
    Do
    
        NumParams = GlobalOrgnizerActionNumArgs(Counter)
        ActionName = GlobalOrganizerActionName(Counter)
        
        StartCol = GlobalOrganizerActionPrintCol(Counter)
        StartRow = GlobalOrganizerActionPrintRow(Counter)
        
        If StartRow > 0 Then
            SearchActionName = Replace(ActionName, "DISABLED:", "")
            SearchActionName = Replace(SearchActionName, " - (Click Here to Update)", "")
        
            If NumParams = 0 Then
                NumParams = NumParams + 1
            End If
    
            'Find our choice
            ChoiceIndex = FindInArray(GlobalBuildingBlocksSteps, SearchActionName)
        
            'Merge
            Range(Cells(StartRow, StartCol), Cells(StartRow, StartCol + 1)).Merge
            Range(Cells(StartRow + 1, StartCol + 2), Cells(StartRow + NumParams, StartCol + 2)).Merge
            
            'Wrap comments text
            Range(Cells(StartRow + 1, StartCol + 2), Cells(StartRow + NumParams, StartCol + 2)).WrapText = True
    
            'Bold
            Range(Cells(StartRow, StartCol), Cells(StartRow, StartCol + 2)).Font.Bold = True
    
            'Color and Font
            If GlobalBuildingBlocksSupported(ChoiceIndex) = False Then
                GlobalOrganizerActionsValidated = False
                Range(Cells(StartRow, StartCol), Cells(StartRow + NumParams, StartCol + 2)).Interior.Color = HEXCOL2RGB("FF2400")
            Else
                Range(Cells(StartRow, StartCol), Cells(StartRow + NumParams, StartCol + 2)).Interior.Color = HEXCOL2RGB(CStr(GlobalBuildingBlocksColor(ChoiceIndex)))
            End If
            Range(Cells(StartRow, StartCol), Cells(StartRow + NumParams, StartCol + 2)).Font.Size = 11
            Range(Cells(StartRow, StartCol), Cells(StartRow, StartCol + 2)).Font.Size = 12
            Range(Cells(StartRow, StartCol), Cells(StartRow + NumParams, StartCol + 2)).Font.name = "Times New Roman"
    
            'Alignment
            Range(Cells(StartRow, StartCol), Cells(StartRow + NumParams, StartCol + 2)).HorizontalAlignment = xlCenter
            Range(Cells(StartRow, StartCol), Cells(StartRow + NumParams, StartCol + 2)).VerticalAlignment = xlCenter
            Range(Cells(StartRow + 1, StartCol), Cells(StartRow + NumParams, StartCol)).HorizontalAlignment = xlLeft
        
            If GlobalOrganizerActionNotAcceptable(Counter) <> False Then
                Range(Cells(StartRow, StartCol), Cells(StartRow, StartCol)).Interior.Color = HEXCOL2RGB("FF2400")
            End If
        
            'Write the cells
            Cells(StartRow, StartCol).Value = ActionName
            Cells(StartRow, StartCol + 2).Value = "Comments"
            Cells(StartRow + 1, StartCol + 2).Value = GlobalOrganizerActionComments(Counter)
        
            Counter2 = 0
            Do
                Title = GlobalOrganizerActionArgsTitles(Counter2, Counter)
                Arg = GlobalOrganizerActionArgs(Counter2, Counter)
                
                If InStr(1, Arg, "=Method!") <> 0 Then
                    ArgColRow = Replace(Arg, "=Method!", "")
                    ArgColRowArray = Split(ArgColRow, "$")
                    ArgCol = ColLetterToNumber(ArgColRowArray(1))
                    ArgRow = ArgColRowArray(2)
                    
                    'Following the references is a big ole pain, we need to go back and find which step it was referencing, Then we need to see if that step shifted. If so, then we update the row and col
                    NewArgRow = 0
                    For RowCounter = 0 To GlobalOrganizerNumActions
                        RowLowerBound = GlobalOrganizerActionRowDetected(RowCounter)
                        RowUpperBound = RowLowerBound + GlobalOrgnizerActionNumArgs(RowCounter) + 2
                        
                        ColLowerBound = GlobalOrganizerActionColDetected(RowCounter)
                        ColUpperBound = ColLowerBound + 2
                        
                        If CInt(ArgRow) < RowUpperBound And CInt(ArgRow) > RowLowerBound And CInt(ArgCol) < ColUpperBound And CInt(ArgCol) > ColLowerBound Then
                            NewArgRow = ArgRow - GlobalOrganizerActionRowDetected(RowCounter) + GlobalOrganizerActionPrintRow(RowCounter)
                            NewArgCol = ColNumberToLetter(ArgCol - GlobalOrganizerActionColDetected(RowCounter) + GlobalOrganizerActionPrintCol(RowCounter))
                            Exit For
                        End If
                    
                    Next RowCounter

                    NewArg = "=Method!$" & NewArgCol & "$" & CStr(NewArgRow)
                    
                    If NewArgRow = 0 Then
                        NewArg = "Reference Bad or Missing"
                        GlobalOrganizerActionArgsNotAcceptable(Counter2, Counter) = True
                        GlobalOrganizerActionNotAcceptable(Counter) = True
                    End If
                    
                    Arg = NewArg
                End If

                Counter2 = Counter2 + 1
                
                If GlobalOrganizerActionArgsTitlesNotAcceptable(Counter2 - 1, Counter) <> False Then
                    Range(Cells(StartRow + Counter2, StartCol), Cells(StartRow + Counter2, StartCol)).Interior.Color = HEXCOL2RGB("FF2400")
                End If
                
                If GlobalOrganizerActionArgsNotAcceptable(Counter2 - 1, Counter) <> False Then
                    Range(Cells(StartRow + Counter2, StartCol + 1), Cells(StartRow + Counter2, StartCol + 1)).Interior.Color = HEXCOL2RGB("FF2400")
                End If
                  
                Cells(StartRow + Counter2, StartCol).Value = Title
                Cells(StartRow + Counter2, StartCol + 1).Value = Arg
        
                'Borders
                Range(Cells(StartRow + Counter2, StartCol), Cells(StartRow + Counter2, StartCol)).Borders(xlEdgeBottom).LineStyle = xlContinuous
                Range(Cells(StartRow + Counter2, StartCol), Cells(StartRow + Counter2, StartCol)).Borders(xlEdgeLeft).LineStyle = xlContinuous
                Range(Cells(StartRow + Counter2, StartCol), Cells(StartRow + Counter2, StartCol)).Borders(xlEdgeRight).LineStyle = xlContinuous
                Range(Cells(StartRow + Counter2, StartCol), Cells(StartRow + Counter2, StartCol)).Borders(xlEdgeTop).LineStyle = xlContinuous
        
                Range(Cells(StartRow + Counter2, StartCol + 1), Cells(StartRow + Counter2, StartCol + 1)).Borders(xlEdgeBottom).LineStyle = xlContinuous
                Range(Cells(StartRow + Counter2, StartCol + 1), Cells(StartRow + Counter2, StartCol + 1)).Borders(xlEdgeLeft).LineStyle = xlContinuous
                Range(Cells(StartRow + Counter2, StartCol + 1), Cells(StartRow + Counter2, StartCol + 1)).Borders(xlEdgeRight).LineStyle = xlContinuous
                Range(Cells(StartRow + Counter2, StartCol + 1), Cells(StartRow + Counter2, StartCol + 1)).Borders(xlEdgeTop).LineStyle = xlContinuous
        
                Range(Cells(StartRow + Counter2, StartCol + 2), Cells(StartRow + Counter2, StartCol + 2)).Borders(xlEdgeBottom).LineStyle = xlContinuous
                Range(Cells(StartRow + Counter2, StartCol + 2), Cells(StartRow + Counter2, StartCol + 2)).Borders(xlEdgeLeft).LineStyle = xlContinuous
                Range(Cells(StartRow + Counter2, StartCol + 2), Cells(StartRow + Counter2, StartCol + 2)).Borders(xlEdgeRight).LineStyle = xlContinuous
                Range(Cells(StartRow + Counter2, StartCol + 2), Cells(StartRow + Counter2, StartCol + 2)).Borders(xlEdgeTop).LineStyle = xlContinuous
        
            Loop While Counter2 < NumParams

            'Final Borders
            Range(Cells(StartRow, StartCol), Cells(StartRow + NumParams, StartCol + 2)).Borders(xlEdgeBottom).LineStyle = xlContinuous
            Range(Cells(StartRow, StartCol), Cells(StartRow + NumParams, StartCol + 2)).Borders(xlEdgeLeft).LineStyle = xlContinuous
            Range(Cells(StartRow, StartCol), Cells(StartRow + NumParams, StartCol + 2)).Borders(xlEdgeRight).LineStyle = xlContinuous
            Range(Cells(StartRow, StartCol), Cells(StartRow + NumParams, StartCol + 2)).Borders(xlEdgeTop).LineStyle = xlContinuous

            Range(Cells(StartRow, StartCol), Cells(StartRow + NumParams, StartCol + 2)).Borders(xlEdgeBottom).Weight = xlMedium
            Range(Cells(StartRow, StartCol), Cells(StartRow + NumParams, StartCol + 2)).Borders(xlEdgeLeft).Weight = xlMedium
            Range(Cells(StartRow, StartCol), Cells(StartRow + NumParams, StartCol + 2)).Borders(xlEdgeRight).Weight = xlMedium
            Range(Cells(StartRow, StartCol), Cells(StartRow + NumParams, StartCol + 2)).Borders(xlEdgeTop).Weight = xlMedium
        
            Range(Cells(StartRow, StartCol + 2), Cells(StartRow + NumParams, StartCol + 2)).Borders(xlEdgeLeft).Weight = xlMedium

            If InStr(1, ActionName, "Finish") <> 0 Or InStr(1, ActionName, "Split Plate") Then
            Else
                'Add add new action cell
                Range(Cells(StartRow + NumParams + 2, StartCol + 1), Cells(StartRow + NumParams + 2, StartCol + 1)).Font.Size = 16
                Range(Cells(StartRow + NumParams + 2, StartCol + 1), Cells(StartRow + NumParams + 2, StartCol + 1)).Font.name = "Times New Roman"
                Range(Cells(StartRow + NumParams + 2, StartCol + 1), Cells(StartRow + NumParams + 2, StartCol + 1)).Font.Bold = True
                Range(Cells(StartRow + NumParams + 2, StartCol + 1), Cells(StartRow + NumParams + 2, StartCol + 1)).HorizontalAlignment = xlCenter
                Range(Cells(StartRow + NumParams + 2, StartCol + 1), Cells(StartRow + NumParams + 2, StartCol + 1)).VerticalAlignment = xlCenter
                Range(Cells(StartRow + NumParams + 2, StartCol + 1), Cells(StartRow + NumParams + 2, StartCol + 1)).Interior.Color = HEXCOL2RGB("d1d1d1")
    
                Cells(StartRow + NumParams + 2, StartCol + 1).Value = "Add Action (Click Here)"
            End If
        End If
        Counter = Counter + 1
    Loop While Counter <= GlobalOrganizerNumActions

    ThisWorkbook.Worksheets("Method").Range("A1:ZZ1000").WrapText = False

    'formatting stuff... LAME!
    For Col = 1 To 100
        With ThisWorkbook.Worksheets("Method").Columns(Col)
            .ColumnWidth = 20
        End With
    Next Col

    ThisWorkbook.Worksheets("Method").Columns("A:ZZ").AutoFit
    
    For Col = 1 To 100
        With ThisWorkbook.Worksheets("Method").Columns(Col)
            If .ColumnWidth > 40 Then
               .ColumnWidth = 40
            End If
        End With
    Next Col
    
    ThisWorkbook.Worksheets("Method").Range("A1:ZZ1000").WrapText = True

End Sub

Public Sub SaveSteps()

    FirstStepCol = 9999
    SplitStepCount = 0
    NumActions = 0
    NumPlates = 0

    'Create a bunch of big arrays to store our saved steps. This array will be resized when a new step is found
    ReDim GlobalOrganizerActionName(0)
    ReDim GlobalOrgnizerActionNumArgs(0)
    ReDim GlobalOrganizerActionArgsTitles(20, 0)
    ReDim GlobalOrganizerActionArgs(20, 0)
    ReDim GlobalOrganizerActionComments(0)
    ReDim GlobalOrganizerActionHorizontalOffset(0)
    ReDim GlobalOrganizerActionRowDetected(0)
    ReDim GlobalOrganizerActionColDetected(0)

    ReDim GlobalSolutionDetectedPlates(0)

    For Counter = 1 To 10000
        ActionRow = 0
        ActionCol = 0
        'The row and col is important so we know which pathway the step belongs
        
        'We need to iterate until we don't find anything on the row. This allows for steps to be side by side after a split plate step.
        While True
        
            'Find it
            Dim Selection As Range
            Set Selection = ThisWorkbook.Worksheets("Method").Range(Cells(Counter, ActionCol + 3), Cells(Counter, 100)).Find("Comments")
            If Selection Is Nothing Then
                'if we don't find anything anymore then we can leave
                GoTo EndWhile
            Else
                ActionRow = Selection.Row
                ActionCol = Selection.Column - 2
            End If
                
            If FirstStepCol = 9999 Then
                FirstStepCol = ActionCol
            End If
        
            ReDim Preserve GlobalOrganizerActionName(NumActions)
            ReDim Preserve GlobalOrgnizerActionNumArgs(NumActions)
            ReDim Preserve GlobalOrganizerActionArgsTitles(20, NumActions)
            ReDim Preserve GlobalOrganizerActionArgs(20, NumActions)
            ReDim Preserve GlobalOrganizerActionComments(NumActions)
            ReDim Preserve GlobalOrganizerActionHorizontalOffset(NumActions)
            ReDim Preserve GlobalOrganizerActionRowDetected(NumActions)
            ReDim Preserve GlobalOrganizerActionColDetected(NumActions)
            
            ActionName = ThisWorkbook.Worksheets("Method").Cells(ActionRow, ActionCol).Value
            
            If InStr(1, ActionName, "Plate") <> 0 And InStr(1, ActionName, "Split Plate") = 0 Then
                ReDim Preserve GlobalSolutionDetectedPlates(NumPlates)
                GlobalSolutionDetectedPlates(NumPlates) = ThisWorkbook.Worksheets("Method").Cells(ActionRow + 1, ActionCol + 1).Value
                NumPlates = NumPlates + 1
            End If
            
            If InStr(1, ActionName, "DELETE") <> 0 And Not (InStr(1, GlobalNewActionName, "Split Plate") <> 0) Then
                'we will skip this step and not store it
            Else 'in this case it can only be Update or Insert
            
                GlobalOrganizerActionName(NumActions) = ActionName
                GlobalOrganizerActionComments(NumActions) = ThisWorkbook.Worksheets("Method").Cells(ActionRow + 1, ActionCol + 2).Value
            
                'Store Action Arg information
                For Counter2 = 1 To 1000
                    Title = ThisWorkbook.Worksheets("Method").Cells(ActionRow + Counter2, ActionCol).Value
                    Arg = ThisWorkbook.Worksheets("Method").Cells(ActionRow + Counter2, ActionCol + 1).Formula
             
                    If Title = "" Then
                        GlobalOrgnizerActionNumArgs(NumActions) = Counter2 - 1
                        Exit For
                    End If
            
                    GlobalOrganizerActionArgsTitles(Counter2 - 1, NumActions) = Title
                    GlobalOrganizerActionArgs(Counter2 - 1, NumActions) = Arg
                Next Counter2
        
                'Store Offset Info
                GlobalOrganizerActionHorizontalOffset(NumActions) = ActionCol - FirstStepCol
                GlobalOrganizerActionRowDetected(NumActions) = ActionRow
                GlobalOrganizerActionColDetected(NumActions) = ActionCol
            
                If InStr(1, ActionName, "UPDATE") <> 0 Then
                
                    'if it is update then we need to overwrite the current step info
                    GlobalOrganizerActionName(NumActions) = GlobalNewActionName & " - (Click Here to Update)"
                    GlobalOrgnizerActionNumArgs(NumActions) = UBound(GlobalNewActionArgsTitles)
                    
                    DoCounter = 0
                    Do
                        GlobalOrganizerActionArgsTitles(DoCounter, NumActions) = GlobalNewActionArgsTitles(DoCounter)
                        GlobalOrganizerActionArgs(DoCounter, NumActions) = GlobalNewActionArgs(DoCounter)
                        
                        DoCounter = DoCounter + 1
                    Loop While DoCounter < UBound(GlobalNewActionArgsTitles)
                    
                ElseIf InStr(1, ActionName, "INSERT") <> 0 Then
                
                    'if it is insert then we want to insert after
                    GlobalOrganizerActionName(NumActions) = Replace(ActionName, "INSERT", "")
                    
                    If InStr(1, GlobalNewActionName, "Split Plate") <> 0 Then
                        ReDim Preserve GlobalOrganizerActionName(NumActions + 3)
                        ReDim Preserve GlobalOrgnizerActionNumArgs(NumActions + 3)
                        ReDim Preserve GlobalOrganizerActionArgsTitles(20, NumActions + 3)
                        ReDim Preserve GlobalOrganizerActionArgs(20, NumActions + 3)
                        ReDim Preserve GlobalOrganizerActionComments(NumActions + 3)
                        ReDim Preserve GlobalOrganizerActionHorizontalOffset(NumActions + 3)
                        ReDim Preserve GlobalOrganizerActionRowDetected(NumActions + 3)
                        ReDim Preserve GlobalOrganizerActionColDetected(NumActions + 3)
                        
                        GlobalOrganizerActionName(NumActions + 1) = "Split Plate" & " - (Click Here to Update)"
                        GlobalOrganizerActionName(NumActions + 2) = "Plate" & " - (Click Here to Update)"
                        GlobalOrganizerActionName(NumActions + 3) = "Plate" & " - (Click Here to Update)"
                        
                        GlobalOrgnizerActionNumArgs(NumActions + 1) = 3
                        GlobalOrgnizerActionNumArgs(NumActions + 2) = 2
                        GlobalOrgnizerActionNumArgs(NumActions + 3) = 2
                        
                        GlobalOrganizerActionArgsTitles(0, NumActions + 1) = GlobalNewActionArgsTitles(0)
                        GlobalOrganizerActionArgsTitles(1, NumActions + 1) = GlobalNewActionArgsTitles(1)
                        GlobalOrganizerActionArgsTitles(2, NumActions + 1) = GlobalNewActionArgsTitles(2)
                        GlobalOrganizerActionArgs(0, NumActions + 1) = GlobalNewActionArgs(0)
                        GlobalOrganizerActionArgs(1, NumActions + 1) = GlobalNewActionArgs(1)
                        GlobalOrganizerActionArgs(2, NumActions + 1) = GlobalNewActionArgs(2)
                        
                        GlobalOrganizerActionArgsTitles(0, NumActions + 2) = "Name"
                        GlobalOrganizerActionArgsTitles(1, NumActions + 2) = "Type"
                        GlobalOrganizerActionArgs(0, NumActions + 2) = GlobalNewActionArgs(1)
                        GlobalOrganizerActionArgs(1, NumActions + 2) = "96 Well PCR Plate"
                        
                        GlobalOrganizerActionArgsTitles(0, NumActions + 3) = "Name"
                        GlobalOrganizerActionArgsTitles(1, NumActions + 3) = "Type"
                        GlobalOrganizerActionArgs(0, NumActions + 3) = GlobalNewActionArgs(2)
                        GlobalOrganizerActionArgs(1, NumActions + 3) = "96 Well PCR Plate"
                    
                        GlobalOrganizerActionHorizontalOffset(NumActions + 1) = ActionCol - FirstStepCol
                        GlobalOrganizerActionHorizontalOffset(NumActions + 2) = ActionCol - FirstStepCol - 2
                        GlobalOrganizerActionHorizontalOffset(NumActions + 3) = ActionCol - FirstStepCol + 2
                        
                        GlobalOrganizerActionRowDetected(NumActions + 1) = ActionRow
                        GlobalOrganizerActionRowDetected(NumActions + 2) = ActionRow + 5
                        GlobalOrganizerActionRowDetected(NumActions + 3) = ActionRow + 5
                        
                        GlobalOrganizerActionColDetected(NumActions + 1) = ActionCol
                        GlobalOrganizerActionColDetected(NumActions + 2) = ActionCol - 2
                        GlobalOrganizerActionColDetected(NumActions + 3) = ActionCol + 2
                        
                        NumActions = NumActions + 3
                    Else
                        NumActions = NumActions + 1

                        ReDim Preserve GlobalOrganizerActionName(NumActions)
                        ReDim Preserve GlobalOrgnizerActionNumArgs(NumActions)
                        ReDim Preserve GlobalOrganizerActionArgsTitles(20, NumActions)
                        ReDim Preserve GlobalOrganizerActionArgs(20, NumActions)
                        ReDim Preserve GlobalOrganizerActionComments(NumActions)
                        ReDim Preserve GlobalOrganizerActionHorizontalOffset(NumActions)
                        ReDim Preserve GlobalOrganizerActionRowDetected(NumActions)
                        ReDim Preserve GlobalOrganizerActionColDetected(NumActions)
                    
                        GlobalOrganizerActionRowDetected(NumActions) = ActionRow
                    
                        'Add the new step here
                        GlobalOrganizerActionName(NumActions) = GlobalNewActionName & " - (Click Here to Update)"
                        GlobalOrganizerActionHorizontalOffset(NumActions) = ActionCol - FirstStepCol
                        GlobalOrgnizerActionNumArgs(NumActions) = UBound(GlobalNewActionArgsTitles)
                        GlobalOrganizerActionRowDetected(NumActions) = ActionRow
                        GlobalOrganizerActionColDetected(NumActions) = ActionCol
                    
                        DoCounter = 0
                        Do
                            GlobalOrganizerActionArgsTitles(DoCounter, NumActions) = GlobalNewActionArgsTitles(DoCounter)
                            GlobalOrganizerActionArgs(DoCounter, NumActions) = GlobalNewActionArgs(DoCounter)
                        
                            DoCounter = DoCounter + 1
                        Loop While DoCounter < UBound(GlobalNewActionArgsTitles)
                    End If
                End If
                
                'Increment Num Actions
                NumActions = NumActions + 1
            End If
        Wend

EndWhile:
    Next Counter

    GlobalOrganizerNumActions = NumActions - 1
    
    If GlobalOrganizerNumActions = -1 Then
        Application.ScreenUpdating = False
        MsgBox ("Bad! You can't delete all steps. What are you doing? This sheet will be reset... Sharon, is that you??")
        ResetMethod
        SaveSteps
        Application.ScreenUpdating = True
        Exit Sub
    End If
    
    If InStr(1, Replace(GlobalOrganizerActionName(0), " - (Click Here to Update)", ""), "Plate") = 0 Then
        Application.ScreenUpdating = False
        MsgBox ("Bad! A Plate block must always be first in a method... This sheet will be reset... Sharon, is that you??")
        ResetMethod
        SaveSteps
        Application.ScreenUpdating = True
        Exit Sub
    End If
    
    ReDim GlobalOrganizerActionPrintRow(NumActions - 1)
    ReDim GlobalOrganizerActionPrintCol(NumActions - 1)
    ReDim GlobalOrganizerActionArgsNotAcceptable(20, NumActions - 1)
    ReDim GlobalOrganizerActionArgsTitlesNotAcceptable(20, NumActions - 1)
    ReDim GlobalOrganizerActionNotAcceptable(NumActions - 1)

End Sub


