Set WshShell = CreateObject("WScript.Shell")

' Delete existing tasks
WshShell.Run "schtasks /delete /tn ""CryptoRiskRadar_06"" /f", 0, True
WshShell.Run "schtasks /delete /tn ""CryptoRiskRadar_14"" /f", 0, True
WshShell.Run "schtasks /delete /tn ""CryptoRiskRadar_22"" /f", 0, True

' Create tasks with current user (no password required for interactive user)
WshShell.Run "schtasks /create /tn ""CryptoRiskRadar_06"" /tr """"C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe"" ""F:\stepclaw\agents\blockchain-analyst\run_with_notification.py"""" /sc daily /st 18:00 /it /f", 0, True
WshShell.Run "schtasks /create /tn ""CryptoRiskRadar_14"" /tr """"C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe"" ""F:\stepclaw\agents\blockchain-analyst\run_with_notification.py"""" /sc daily /st 02:00 /it /f", 0, True
WshShell.Run "schtasks /create /tn ""CryptoRiskRadar_22"" /tr """"C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe"" ""F:\stepclaw\agents\blockchain-analyst\run_with_notification.py"""" /sc daily /st 10:00 /it /f", 0, True

MsgBox "Tasks recreated successfully!" & vbCrLf & vbCrLf & _
       "Schedule (CST):" & vbCrLf & _
       "  - 02:00 (CryptoRiskRadar_14)" & vbCrLf & _
       "  - 10:00 (CryptoRiskRadar_22)" & vbCrLf & _
       "  - 18:00 (CryptoRiskRadar_06)", vbInformation, "Crypto Risk Radar"
