"""
Auto backups autosave for Baldur's Gate 3 Honor Mode

Intention -> Track each autosave,
             Make a backup each time the game autosaves (ie. When the application is closed)
             Load Save
             Todo: import JSON file for data recording 
    
Todo ->

Error checking
Input save manipulation
"""

import shutil
import os
import getpass
import json


#Check save state json
filename = "config.json"

#Data structure -> move to where data is assigned
data = {
        "file_savename": "null",
    }


#Save new config
def writeJson(data):
    with open(filename, 'w') as json_file: 
        json.dump(data, json_file, indent=4)
        print(f"'{filename}' written.")


#Check if the file exists
if os.path.exists(filename):
    # File exists, so open it and read the data
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
        print(f"Currently monitored save file: {data['file_savename']}" )
else:
    writeJson(data)

        
#Get the current user's login name, for searching if the files exists
username = getpass.getuser()
directory_path = f"C:\\Users\\{username}\\AppData\\Local\\Larian Studios\\Baldur's Gate 3\\PlayerProfiles\\Public\\Savegames\\Story"
if os.path.exists(directory_path):
    print(f"Saves for {username} found.")


#Displaying all available files
save_list_paths  = []
for count, sub_directory in enumerate(os.listdir(directory_path)):
    save_list_paths.append(os.path.join(directory_path, sub_directory))
    print(f"({count}) {sub_directory}")
 

#To do, add error catching, logic
if data["file_savename"] == "null": 
    user_input = input("Select a save file to monitor: ")
    data["file_savename"] = os.path.basename(save_list_paths[int(user_input)])
    writeJson(data)
    print("You entered:", os.path.basename(save_list_paths[int(user_input)]))    
    
    
#Backup example 
if os.path.exists( os.path.join("./backup", os.path.basename(save_list_paths[0])) ):
    print("\nBackup already exists for the current save, backup not performed.\n")
else:
    print("\nBackup performed.\n")
    shutil.copytree(save_list_paths[0], os.path.join("./backup", os.path.basename(save_list_paths[0])))