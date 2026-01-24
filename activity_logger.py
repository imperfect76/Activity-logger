# Activity logger
# Logs system start/stop and VS Code start/stop events with timestamps

import time
import psutil
import signal
import sys
from datetime import datetime

LOG_FILE = "activity.txt"

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_event(event):
    if not event:
        return
    line = f"{get_timestamp()} | {event}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)

def vscode_is_running():
    for proc in psutil.process_iter(['pid', 'name', 'ppid']):
        if proc.info['name'] == 'code': 
            return True
    return False

def vscode_state_checker(past_state):
    now_state = vscode_is_running()

    if not past_state and now_state:
        return "VSCODE_START"

    elif past_state and not now_state:
        return "VSCODE_STOP"

    return None

def handle_exit(signum, frame):
    log_event("COMPUTER_STOP")
    sys.exit(0)

def main():
    log_event("COMPUTER_START")
    vscode_past_state = False
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    while True:
        event = vscode_state_checker(vscode_past_state)
        if event:
            log_event(event)

        vscode_past_state = vscode_is_running()
        time.sleep(2)

if __name__ == "__main__":
    main()