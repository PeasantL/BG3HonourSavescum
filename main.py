import shutil
import os
import getpass
import json
from datetime import datetime
import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import time  # Don't forget to import time for the sleep function

# Simplify JSON handling and argparse setup
def setup_argparse():
    parser = argparse.ArgumentParser(description="Backup autosave for Baldur's Gate 3 Honor Mode")
    parser.add_argument('--reselect', help='Reselect save file', action='store_true')
    return parser.parse_args()

def load_or_initialize_config(filename="config.json", default_data={"file_savename": "null"}):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        write_json(filename, default_data)
        return default_data

def write_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"'{filename}' written.")

def select_save_file(directory_path):
    save_list_paths = [os.path.join(directory_path, sd) for sd in os.listdir(directory_path)]
    for idx, path in enumerate(save_list_paths):
        print(f"({idx}) {os.path.basename(path)}")
    user_input = int(input("Select a save file to monitor: "))
    return save_list_paths[user_input]

def backup_save_file(selected_save_path):
    backup_dir_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_path = os.path.join("./backup", backup_dir_name, os.path.basename(selected_save_path))
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    shutil.copytree(selected_save_path, backup_path, dirs_exist_ok=True)  # Ensure dirs_exist_ok=True for repeated backups
    print("\nBackup performed in folder:", backup_dir_name)

class BackupTimer:
    def __init__(self, wait_time, target_function, args=None):
        self._timer = None
        self.wait_time = wait_time
        self.target_function = target_function
        self.args = args if args is not None else []
        self.lock = threading.Lock()

    def _run(self):
        with self.lock:
            self.target_function(*self.args)
            self._timer = None

    def reset(self):
        with self.lock:
            if self._timer is not None:
                self._timer.cancel()
            self._timer = threading.Timer(self.wait_time, self._run)
            self._timer.start()

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, path):
        self.path = path
        # Adjust the wait_time to suit the frequency of file changes
        self.backup_timer = BackupTimer(5, backup_save_file, [path])

    def on_modified(self, event):
        if not event.is_directory:
            self.backup_timer.reset()
def main():
    args = setup_argparse()
    data = load_or_initialize_config()

    username = getpass.getuser()
    directory_path = f"C:\\Users\\{username}\\AppData\\Local\\Larian Studios\\Baldur's Gate 3\\PlayerProfiles\\Public\\Savegames\\Story"
    if not os.path.exists(directory_path):
        print(f"No saves for {username} found.")
        return

    if args.reselect or data["file_savename"] == "null":
        selected_save_path = select_save_file(directory_path)
        data["file_savename"] = os.path.basename(selected_save_path)
        write_json("config.json", data)
    else:
        selected_save_path = os.path.join(directory_path, data['file_savename'])

    # Set up monitoring for modifications
    event_handler = ChangeHandler(selected_save_path)
    observer = Observer()
    observer.schedule(event_handler, path=selected_save_path, recursive=True)
    observer.start()
    print("Monitoring for modifications. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
