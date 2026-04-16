Set WshShell = CreateObject("WScript.Shell")

' Delete existing tasks
WshShell.Run "schtasks /delete /tn ""CryptoRiskRadar_06"" /f", 0, True
WshShell.Run "schtasks /delete /tn ""CryptoRiskRadar_14"" /f", 0, True
WshShell.Run "schtasks /delete /tn ""CryptoRiskRadar_22"" /f", 0, True

' Create tasks with working directory
' Using /tr with working directory specified in the command
workingDir = "F:\stepclaw\agents\blockchain-analyst"

' CryptoRiskRadar_14 - 02:00 CST
cmd14 = "cmd /c cd /d """ & workingDir & """ && """ & _
        "C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe"" """ & _
        workingDir & "\run_with_notification.py"""
WshShell.Run "schtasks /create /tn ""CryptoRiskRadar_14"" /tr """ & cmd14 & """ /sc daily /st 02:00 /it /f", 0, True

' CryptoRiskRadar_22 - 10:00 CST
cmd22 = "cmd /c cd /d """ & workingDir & """ && """ & _
        "C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe"" """ & _
        workingDir & "\run_with_notification.py"""
WshShell.Run "schtasks /create /tn ""CryptoRiskRadar_22"" /tr """ & cmd22 & """ /sc daily /st 10:00 /it /f", 0, True

' CryptoRiskRadar_06 - 18:00 CST
cmd06 = "cmd /c cd /d """ & workingDir & """ && """ & _
        "C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe"" """ & _
        workingDir & "\run_with_notification.py"""
WshShell.Run "schtasks /create /tn ""CryptoRiskRadar_06"" /tr """ & cmd06 & """ /sc daily /st 18:00 /it /f", 0, True

MsgBox "Tasks recreated with working directory!" & vbCrLf & vbCrLf & _
       "Working directory: " & workingDir & vbCrLf & vbCrLf & _
       "Schedule (CST):" & vbCrLf & _
       "  - 02:00 (CryptoRiskRadar_14)" & vbCrLf & _
       "  - 10:00 (CryptoRiskRadar_22)" & vbCrLf & _
       "  - 18:00 (CryptoRiskRadar_06)", vbInformation, "Crypto Risk Radar"
