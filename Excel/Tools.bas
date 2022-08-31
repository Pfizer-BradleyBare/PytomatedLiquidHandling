Attribute VB_Name = "Tools"
'Rando Tools I stole from the internet

Public Function FileIsOpen(FullFilePath As String) As Boolean

    Dim ff As Long

    On Error Resume Next

    ff = FreeFile()
    Open FullFilePath For Input Lock Read As #ff
    Close ff
    FileIsOpen = (Err.Number <> 0)

    On Error GoTo 0

End Function

Public Function AltRefEdit(name As String, reftype As String)
  
'Written by Ben Huffman. Thank you Ben!!!
  
Dim var As Variant

On Error Resume Next
var = Application.InputBox("Select a " & reftype & " worksheet reference", name, , , , , , 0)
On Error GoTo 0
  
If TypeName(var) = "String" Then
    AltRefEdit = "=" & CheckAddress(CStr(var))
Else
    AltRefEdit = ""
End If

End Function

Public Function CheckAddress(sAddress As String)
  'Written by Ben Huffman. Thank you Ben!!!
  
  ' changed following advice of Julien steelandt@yahoo.fr
Dim rng As Range
Dim sFullAddress As String

  If Left$(sAddress, 1) = "=" Then sAddress = Mid$(sAddress, 2, 256)
  If Left$(sAddress, 1) = Chr(34) Then sAddress = Mid$(sAddress, 2, 255)
  If Right$(sAddress, 1) = Chr(34) Then sAddress = Left$(sAddress, Len(sAddress) - 1)

  On Error Resume Next
  sAddress = Application.ConvertFormula(sAddress, xlR1C1, xlA1)

  If IsRange(sAddress) Then
    Set rng = Range(sAddress)
  End If

  If Not rng Is Nothing Then
    sFullAddress = rng.Address(, , Application.ReferenceStyle, True)
    If Left$(sFullAddress, 1) = "'" Then
      sAddress = "'"
    Else
      sAddress = ""
    End If
    sAddress = sAddress & Mid$(sFullAddress, InStr(sFullAddress, "]") + 1)
    'rng.Parent.Activate
  End If

CheckAddress = sAddress

End Function

Public Function IsRange(ByVal sRangeAddress As String) As Boolean
    'Written by Ben Huffman. Thank you Ben!!!
    
  Dim TestRange As Range


  IsRange = True
  On Error Resume Next
  Set TestRange = Range(sRangeAddress)
  If Err.Number <> 0 Then
    IsRange = False
  End If
  Err.Clear
  On Error GoTo 0
  Set TestRange = Nothing
  
End Function


Public Sub QuickSort(vArray As Variant, inLow As Long, inHi As Long)
    'Found randomly online. Checked the code and tested. Working.

  Dim pivot   As Variant
  Dim tmpSwap As Variant
  Dim tmpLow  As Long
  Dim tmpHi   As Long

  tmpLow = inLow
  tmpHi = inHi

  pivot = vArray((inLow + inHi) \ 2)

  While (tmpLow <= tmpHi)
     While (vArray(tmpLow) < pivot And tmpLow < inHi)
        tmpLow = tmpLow + 1
     Wend

     While (pivot < vArray(tmpHi) And tmpHi > inLow)
        tmpHi = tmpHi - 1
     Wend

     If (tmpLow <= tmpHi) Then
        tmpSwap = vArray(tmpLow)
        vArray(tmpLow) = vArray(tmpHi)
        vArray(tmpHi) = tmpSwap
        tmpLow = tmpLow + 1
        tmpHi = tmpHi - 1
     End If
  Wend

  If (inLow < tmpHi) Then QuickSort vArray, inLow, tmpHi
  If (tmpLow < inHi) Then QuickSort vArray, tmpLow, inHi
End Sub

Public Function HEXCOL2RGB(ByVal HexColor As String) As Long
   'Found randomly online. Luckily it works
    Dim Red As String, Green As String, Blue As String
    
    HexColor = Replace(HexColor, "#", "")
    Red = Val("&H" & Mid(HexColor, 1, 2))
    Green = Val("&H" & Mid(HexColor, 3, 2))
    Blue = Val("&H" & Mid(HexColor, 5, 2))
     
    HEXCOL2RGB = RGB(Red, Green, Blue)
End Function

Public Sub GetCol(Arr As Variant, ResultArr As Variant, ColumnNumber As Long)
    Dim RowNdx As Long

    Erase ResultArr
    ReDim ResultArr(LBound(Arr, 1) To UBound(Arr, 1))
    For RowNdx = LBound(ResultArr) To UBound(ResultArr)
        ResultArr(RowNdx) = Arr(RowNdx, ColumnNumber)
    Next RowNdx
End Sub

Public Function FindInArray(SearchArray, SearchItem)

    For Counter = 0 To UBound(SearchArray)
        If SearchArray(Counter) = SearchItem Then
            FindInArray = Counter
            Exit Function
        End If
    Next Counter
    
    FindInArray = -1
End Function

Function ColLetterToNumber(Letter)
    ColLetterToNumber = Range(Letter & 1).Column
End Function

Function ColNumberToLetter(Number)
    ColNumberToLetter = Split(Cells(1, Number).Address, "$")(1)
End Function
