import shutil
import os
import getpass
import json
from datetime import datetime
import argparse  # 

# Setup argparse
parser = argparse.ArgumentParser(description='Backup autosave for Baldur\'s Gate 3 Honor Mode')
parser.add_argument('--reselect', help='Reselect save file', action='store_true')
args = parser.parse_args()

# Check save state json
filename = "config.json"

# Data structure
data = {
    "file_savename": "null",
}

def writeJson(data):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
        print(f"'{filename}' written.")

if os.path.exists(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
        print(f"Currently monitored save file: {data['file_savename']}")
else:
    writeJson(data)

username = getpass.getuser()
directory_path = f"C:\\Users\\{username}\\AppData\\Local\\Larian Studios\\Baldur's Gate 3\\PlayerProfiles\\Public\\Savegames\\Story"
if os.path.exists(directory_path):
    print(f"Saves for {username} found.")

# Function to select a save file
def select_save_file():
    save_list_paths = []
    for count, sub_directory in enumerate(os.listdir(directory_path)):
        save_list_paths.append(os.path.join(directory_path, sub_directory))
        print(f"({count}) {sub_directory}")
    
    user_input = input("Select a save file to monitor: ")
    return save_list_paths[int(user_input)]

# Reselect save file if the flag is raised or if file_savename is null
if args.reselect or data["file_savename"] == "null":
    selected_save_path = select_save_file()
    data["file_savename"] = os.path.basename(selected_save_path)
    writeJson(data)
    print("Monitoring save file:", os.path.basename(selected_save_path))
else:
    selected_save_path = os.path.join(directory_path, data['file_savename'])

# Backup the selected save file
backup_directory_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_path = os.path.join("./backup", backup_directory_name, os.path.basename(selected_save_path))
if not os.path.exists(backup_path):
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)  # Ensure the parent directory exists
    shutil.copytree(selected_save_path, backup_path)
    print("\nBackup performed in folder:", backup_directory_name)
