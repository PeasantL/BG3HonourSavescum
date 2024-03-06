import shutil
import os
import getpass
import json
from datetime import datetime
import argparse

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
    shutil.copytree(selected_save_path, backup_path)
    print("\nBackup performed in folder:", backup_dir_name)

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

    print("Currently monitoring: " + data['file_savename'])

    backup_save_file(selected_save_path)

if __name__ == "__main__":
    main()
