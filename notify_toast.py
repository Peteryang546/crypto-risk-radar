#!/usr/bin/env python3
"""
Windows Toast Notification
Works even when running from Task Scheduler
"""

import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')

OUTPUT_DIR = Path(r'F:\stepclaw\agents\blockchain-analyst\output')
LOG_FILE = OUTPUT_DIR / 'last_run.json'


def send_toast_notification():
    """Send Windows toast notification"""
    
    if not LOG_FILE.exists():
        return False
    
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        log = json.load(f)
    
    status = log.get('status', 'unknown')
    ts = log.get('timestamp', 'unknown')[:19]
    
    # Build notification
    if status == 'success':
        title = "Crypto Risk Radar - Success"
        message = f"Report published at {ts}"
    else:
        title = "Crypto Risk Radar - Failed"
        message = f"Run failed at {ts}"
    
    # Try different notification methods
    
    # Method 1: win10toast (if installed)
    try:
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast(
            title,
            message,
            icon_path=None,
            duration=10,
            threaded=True
        )
        return True
    except:
        pass
    
    # Method 2: Windows Script Host
    try:
        import subprocess
        ps_script = f'''
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
        $template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
        $template.SelectSingleNode("//text[@id='1']").AppendChild($template.CreateTextNode("{title}")) | Out-Null
        $template.SelectSingleNode("//text[@id='2']").AppendChild($template.CreateTextNode("{message}")) | Out-Null
        $toast = [Windows.UI.Notifications.ToastNotification]::new($template)
        [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Crypto Risk Radar").Show($toast)
        '''
        subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            timeout=10
        )
        return True
    except:
        pass
    
    # Method 3: Simple beep + print
    try:
        import winsound
        winsound.Beep(1000, 500)
    except:
        pass
    
    print(f"[{status.upper()}] {title}: {message}")
    return True


if __name__ == "__main__":
    send_toast_notification()
