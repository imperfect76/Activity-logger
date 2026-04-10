# Activity logger
# Logs system start/stop and process start/stop events with timestamps

import time
import psutil
import signal
import sys
import argparse
import json
from datetime import datetime

parser = argparse.ArgumentParser(description="Process activity logger")
parser.add_argument("process", help="Process name for logging")
args = parser.parse_args()
LOG_FILE = "activity.json"
process_name = args.process

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_event(event):
    if not event:
        return
    line = {"timestamp": get_timestamp(), "event": event, "process": process_name}
    json_line = json.dumps(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json_line + "\n")

def process_is_running(process_name):
    for proc in psutil.process_iter(['pid', 'name', 'ppid']):
        if proc.info['name'] == process_name: 
            return True
    return False

def process_state_checker(past_state):
    now_state = process_is_running(process_name)

    if not past_state and now_state:
        return "PROCESS_STARTED"

    elif past_state and not now_state:
        return "PROCESS_STOPPED"

    return None

def handle_exit(signum, frame):
    log_event("LOGGER_STOPPED")
    sys.exit(0)

def main():
    log_event("LOGGER_STARTED")
    if process_is_running(process_name):
        log_event("PROCESS_RUNNING")
    process_past_state = process_is_running(process_name)
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    while True:
        event = process_state_checker(process_past_state)
        if event:
            log_event(event)

        process_past_state = process_is_running(process_name)
        time.sleep(2)

if __name__ == "__main__":
    main()