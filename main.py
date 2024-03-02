"""
Auto backups autosave for Baldur's Gate 3 Honor Mode

Intention -> Track each autosave,
             Make a backup each time the game autosaves (ie. When the application is closed)
             Load Save
             Todo: import JSON file for data recording
    
"""

import shutil
import os
import getpass
from pprint import pprint
import json


# Get the current user's login name, for searching if the files exists
username = getpass.getuser()
directory_path = f"C:\\Users\\{username}\\AppData\\Local\\Larian Studios\\Baldur's Gate 3\\PlayerProfiles\\Public\\Savegames\\Story"

if os.path.exists(directory_path):
    print(f"Saves for {username} found.")

#Displaying all avaialbe files
save_list_paths  = []

for count, sub_directory in enumerate(os.listdir(directory_path)):
    
    save_list_paths.append(os.path.join(directory_path, sub_directory))
    print(f"{count}) {sub_directory}")
    
#Backup example 
if os.path.exists( os.path.join("./backup", os.path.basename(save_list_paths[0])) ):
    print("\nBackup already exists for the current save, backup not performed.\n")
else:
    print("\nBackup performed.\n")
    shutil.copytree(save_list_paths[0], os.path.join("./backup", os.path.basename(save_list_paths[0])))
