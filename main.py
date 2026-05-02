# IMPORT REQUIRED MODULES
import json
from datetime import datetime, timedelta
import os
import shutil
import sys


# ADD MINS
def add_min(TIME, MINS):
    TEMP_TIME = datetime.strptime(TIME, "%H:%M:%S")
    NEW_TIME = TEMP_TIME + timedelta(minutes=MINS)
    END_TIME = NEW_TIME.strftime("%H:%M:%S")
    return END_TIME


# FETCH DATA
def fetch_data(FILENAME):
    # CASE 1: FILE NOT EXISTS
    if not os.path.exists(FILENAME):
        with open(FILENAME, "x") as file:
            json.dump(DEFAULT, file, indent=4)
        print("NOTE: New file created!")

    with open(FILENAME, "r") as file:
        content = file.read()

    # CASE 2: FILE IS EMPTY
    if not content.strip():
        print("NOTE: File is empty, loadind defaults!")
        return DEFAULT
    try:
        loaded_content = json.loads(content)

        # WRONG TYPE (LIST, STR, NONE ETC.)
        if not isinstance(loaded_content, dict):
            print("NOTE: File has unexpected structure, loading defaults!")
            return DEFAULT

        # ALL RIGHT BUT TODAY'S DATE MISSING
        if DATE not in loaded_content:
            loaded_content[DATE] = {}
            print(f"NOTE: New date {DATE} added!")

        return loaded_content

    # BROKEN OR CORRUPTED JSON
    except json.JSONDecodeError:
        # SAVE BROKEN FILE BEFORE OVERWRITING
        print(f"NOTE: '{FILENAME}' is broken or corrupted!")
        user_choice = input("Overwrite with defaults? (y/n): ").lower().strip()
        if user_choice == "y":
            broken_dir = ".trash"
            os.makedirs(broken_dir, exist_ok=True)

            broken_file = os.path.join(broken_dir, "broken.json")

            shutil.copy2(FILENAME, broken_file)
            print(f"NOTE: Broken file saved as '{broken_file}'")

            # LOAD DEFAULT
            print("NOTE: Defaults loaded!")
            return DEFAULT
        else:
            sys.exit("Operation cancelled. Fix the JSON manually.")


# SHOW ALL DATA
def show_logs(data, type):
    if type == "all":
        for date, entries in data.items():
            print(f"{date}")
            for time, entry in entries.items():
                print(f"\t{time}  -  {entry['TASK']}  -  {entry["MINS"]} mins")
    elif type == "today":
        print(DATE)
        for time, entry in data.get(DATE, {}).items():
            print(f"\t{time}  -  {entry['TASK']}  -  {entry["MINS"]} mins")


if __name__ == "__main__":
    # GET TIME
    now = datetime.now()
    DATE = now.strftime("%Y-%m-%d")
    TIME = now.strftime("%H:%M:%S")

    # CONFIGURABLE TWEAKS
    DEFAULT = {DATE: {}}
    FILENAME = "timelog.json"

    # GET FILE DATA
    data = fetch_data(FILENAME)

    # GET USER DATA
    TASK = input("TASK: ")
    TAG = input("TAG: ")
    MINS = int(input("MINS: "))
    NOTE = input("NOTE: ")
    END_TIME = add_min(TIME, MINS)

    # DATA
    my_data = {
        TIME: {
            "TASK": TASK,
            "TAG": TAG,
            "MINS": MINS,
            "NOTE": NOTE,
            "END_TIME": END_TIME,
        }
    }

    # MODIFY/APPEND DATA
    data[DATE].update(my_data)

    # WRITE MODIFIED DATA
    with open(FILENAME, "w") as file:
        json.dump(data, file, indent=4)

    # SHOW LOGS (today, all)
    show_logs(data, "today")
