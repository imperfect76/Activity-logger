import time
import json
import argparse
from datetime import datetime, timedelta


#parser = argparse.ArgumentParser(description="Process activity analyzer")
#parser.add_argument("process", help="Process name for analisys")
#args = parser.parse_args()
LOG_FILE = "activity.json"
#process_name = args.process

def read_log():
    start, stop = None, None
    duration = timedelta()
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            if data["event"] == "PROCESS_STARTED" or data["event"] == "PROCESS_RUNNING":
                start = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S")
            if data["event"] == "PROCESS_STOPPED" or data["event"] == "LOGGER_STOPPED":
                stop = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S")
                if start is not None:
                    duration += stop - start
                    start = None
        print(duration)

def main():
    read_log()

if __name__ == "__main__":
    main()