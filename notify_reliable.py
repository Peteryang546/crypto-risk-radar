#!/usr/bin/env python3
"""
Reliable Notification System
Sends notifications through multiple channels
"""

import json
import sys
import subprocess
from datetime import datetime
from pathlib import Path

sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')

OUTPUT_DIR = Path(r'F:\stepclaw\agents\blockchain-analyst\output')
LOG_FILE = OUTPUT_DIR / 'last_run.json'


def send_notification():
    """Send notification through multiple channels"""
    
    if not LOG_FILE.exists():
        print("[ERROR] No run log found")
        return False
    
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        log = json.load(f)
    
    status = log.get('status', 'unknown')
    ts = log.get('timestamp', 'unknown')[:19]
    details = log.get('details', {})
    
    # Build notification message
    if status == 'success':
        duration = details.get('duration_seconds', 0)
        website = details.get('website', 'https://peteryang546.github.io/crypto-risk-radar/')
        
        # Find latest report
        reports = sorted(OUTPUT_DIR.glob('enhanced_report_*.html'), 
                        key=lambda x: x.stat().st_mtime, reverse=True)
        report_name = reports[0].name if reports else 'N/A'
        
        message = f"""[!] Crypto Risk Radar - Run Complete [OK]

Status: SUCCESS
Time: {ts}
Duration: {duration:.1f} seconds
Report: {report_name}

Website: {website}

Next run: See schedule"""
    else:
        error = details.get('error', 'Unknown error')
        
        message = f"""[!] Crypto Risk Radar - Run Failed [ERR]

Status: FAILED
Time: {ts}
Error: {error}

Please check the system."""
    
    # Method 1: Print to stdout (for OpenClaw capture)
    print("="*70)
    print("NOTIFICATION")
    print("="*70)
    print(message)
    print("="*70)
    
    # Method 2: Save to notification file
    notify_file = OUTPUT_DIR / 'last_notification.txt'
    with open(notify_file, 'w', encoding='utf-8') as f:
        f.write(message)
    
    # Method 3: Create a flag file that can be polled
    flag_file = OUTPUT_DIR / 'notification_ready.flag'
    with open(flag_file, 'w', encoding='utf-8') as f:
        f.write(f"{status}\n{ts}\n{message}")
    
    # Method 4: Windows notification with sound
    try:
        ps_code = f'''
        # Play system sound
        [System.Media.SystemSounds]::Beep.Play()
        
        # Show notification
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.MessageBox]::Show(@"
{message}
"@, "Crypto Risk Radar Notification", "OK", "Information")
        '''
        subprocess.run(
            ["powershell", "-Command", ps_code],
            capture_output=True,
            timeout=10
        )
    except:
        pass  # Windows notification is optional
    
    # Method 5: Windows toast notification (Windows 10+)
    try:
        toast_ps = f'''
        $title = "Crypto Risk Radar"
        $message = "Report generated: {report_name if status == 'success' else 'FAILED'}"
        
        # Try Windows 10 toast notification
        try {{
            [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
            $template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
            $template.SelectSingleNode("//text[@id='1']").AppendChild($template.CreateTextNode($title)) | Out-Null
            $template.SelectSingleNode("//text[@id='2']").AppendChild($template.CreateTextNode($message)) | Out-Null
            $toast = [Windows.UI.Notifications.ToastNotification]::new($template)
            [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Crypto Risk Radar").Show($toast)
        }} catch {{
            # Fallback to balloon tip
            Add-Type -AssemblyName System.Windows.Forms
            $icon = New-Object System.Windows.Forms.NotifyIcon
            $icon.Icon = [System.Drawing.SystemIcons]::Information
            $icon.BalloonTipTitle = $title
            $icon.BalloonTipText = $message
            $icon.Visible = $true
            $icon.ShowBalloonTip(5000)
        }}
        '''
        subprocess.run(
            ["powershell", "-Command", toast_ps],
            capture_output=True,
            timeout=10
        )
    except:
        pass
    
    return True


if __name__ == "__main__":
    send_notification()
