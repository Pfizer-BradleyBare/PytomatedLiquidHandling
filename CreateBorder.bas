Attribute VB_Name = "Module3"
Sub CreateBorder(Sheet As String, RowStart As Integer, ColStart As Integer, RowEnd As Integer, ColEnd As Integer)

Sheets(Sheet).Select
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




End Sub
