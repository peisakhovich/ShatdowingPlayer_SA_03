Set WshShell = CreateObject("WScript.Shell")

url = "http://127.0.0.1:8000/"
bat = "C:\Users\liudm\SadowingApp\SA_03\SA_03\run_docs.bat"

Set http = CreateObject("MSXML2.XMLHTTP")

' Проверяем, запущен ли MkDocs
On Error Resume Next
http.Open "GET", url, False
http.Send

If http.Status = 200 Then

    ' MkDocs уже работает
    WshShell.Run url

Else

    ' Запускаем MkDocs скрыто
    WshShell.Run """" & bat & """", 0, False

    ' Ждём запуска сервера
    started = False

    For i = 1 To 20

        WScript.Sleep 500

        http.Open "GET", url, False
        http.Send

        If http.Status = 200 Then
            started = True
            Exit For
        End If

    Next

    ' Открываем браузер только если сервер запустился
    If started Then
        WshShell.Run url
    End If

End If

On Error GoTo 0