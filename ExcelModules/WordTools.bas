Attribute VB_Name = "WordTools"
Private Sub CheckIsAlive()

    On Error GoTo Dead
    WordHandle.Visible = True
    Exit Sub
Dead:
    On Error GoTo 0
    Set WordHandle = Nothing

End Sub

Sub OpenWordDocument()
       
    Dim BuildingBlocksHelpPath As String
    ScriptHelpPath = "C:\Program Files (x86)\HAMILTON\BAREB\Script\HamiltonVisualMethodEditor\Help Documents\Methods Help Document.docx"
    BuildingBlocksHelpPath = Environ("USERPROFILE") & "\OneDrive - Pfizer\Documents\_ABN\HelpDocuments\Methods Help Document.docx"

    If Dir(ScriptHelpPath) <> "" Then
        Path = ScriptHelpPath
    ElseIf Dir(BuildingBlocksHelpPath) <> "" Then
        Path = BuildingBlocksHelpPath
    Else
        MsgBox ("The help document is not available on this PC. Please contact a Hamilton SME to correct. Sorry about that...")
        Exit Sub
    End If

    CheckIsAlive

    If WordHandle Is Nothing Then
        OpeningWordDocument.Show
        Set WordHandle = CreateObject("Word.Application")
        WordHandle.Visible = True
      
        Set GlobalHelpDocumentHandle = WordHandle.Documents.Open(Path, ReadOnly:=True)
        OpeningWordDocument.Hide
    End If
    
End Sub

Sub CloseWordDocument()

    CheckIsAlive

    If WordHandle Is Nothing Then
    Else
        WordHandle.Quit
    End If
    Set WordHandle = Nothing

End Sub

Private Sub Maximize()
    CheckIsAlive

    If WordHandle Is Nothing Then
    Else
        WordHandle.Activate
        WordHandle.WindowState = wdWindowStateMaximize
        'This is a partial maximization so the user can still interface with excel and learn
    End If
End Sub

Sub GotoBookmark(Bookmark As String)
    Maximize
 
    CheckIsAlive

    If WordHandle Is Nothing Then
    Else
 
        WordHandle.ScreenUpdating = False
        GlobalHelpDocumentHandle.Bookmarks("Purpose").Select
    
        On Error GoTo Missing
        GlobalHelpDocumentHandle.Bookmarks(Bookmark).Select
        On Error GoTo 0
    
        If Bookmark <> "Purpose" Then
            GlobalHelpDocumentHandle.ActiveWindow.SmallScroll down:=20
        Else
            GlobalHelpDocumentHandle.ActiveWindow.SmallScroll up:=20
        End If
        WordHandle.ScreenUpdating = True
        Exit Sub
    
Missing:
    WordHandle.ScreenUpdating = True
    MsgBox ("Unfortunately your help request was not found in the help document. If you can find it manually then please inform a Hamilton SME to correct. Thanks!")

    End If
End Sub

