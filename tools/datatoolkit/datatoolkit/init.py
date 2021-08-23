import yaml
import os
import os.path, time
import re
from datetime import datetime, date

cur_dir = os.getcwd()



def get_size(start_path = cur_dir):
    total_size = 0
    totalFiles = 0
    totalDir = 0
    date_mod = []
    for dirpath, dirnames, filenames in os.walk(start_path):
        for directories in dirnames:
            totalDir += 1
        for f in filenames:
            if f.endswith("_Project.yaml")==False: 
                totalFiles += 1
                fp = os.path.join(dirpath, f)
                date_mod.append(datetime.fromtimestamp(os.path.getmtime(fp)).strftime('%Y-%m-%d %H:%M:%S'))
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
    
    return total_size, totalFiles, totalDir, max(date_mod) 

def init():
    size, files, dir, date_mod = get_size()
    # Ask for project UID:
    correct = 'n'
    while correct != 'y':
        Project_UID = input("Please Enter Project UID:")
        correct = input("You entered: " + Project_UID + "\n Is this correct (y/n):")
    # Ask for project name:
    correct2 = 'n'
    while correct2 != 'y':
        Project_name = input("Please Enter Project Name:")
        correct2 = input("You entered: " + Project_name + "\n Is this correct (y/n):")
     # Ask for project start date:
    correct3 = 'n'
    while correct3 != 'y':
        Project_startdate = input("Please Enter Project Start Date (yyyy-mm-dd):")
        try:
            year, month, day = map(int, Project_startdate.split('-'))
            Project_date1 = date(year, month, day)
            correct3 = input("You entered: " + str(Project_date1) + "\n Is this correct (y/n):")
        except: 
            print("Your entry is not in correct format (yyyy-mm-dd): "+ Project_startdate + "\nPlease Try again\n")
    dict_file = [
    {'Project UID' : Project_UID},
    {'Project name' : Project_name}, 
    {'Project start date' : str(Project_date1)}, 
    {'Pathologies' : ["Replace this text"]},
    {'Anomalies' : ["Replace this text"]},
    {'Experiments' : ["Replace this text"]},
    {'Last updated' : date_mod},
    {'Project Size (Mb)' : size/1000000},
    {'Number of folders' : dir},
    {'Number of files' : files}
    ]
    file_name = Project_UID + "_" + Project_name +'_Project.yaml'
    file_path = os.path.join(cur_dir, file_name)
    with open(file_path, 'w') as file:
        documents = yaml.dump(dict_file, file)
    print("Yaml file successfully created:\n" + file_path + "\nPlease do not rename or remove '_Project.yaml' from the file name")
'''
size, files, dir = get_size()
dict_file = [{'Project Size (Mb)' : size/1000000},
    {'Number of folders' : dir},
    {'nUmber of files' : files}
    ]
with open(file_path, 'w') as file:
    documents = yaml.dump(dict_file, file)
'''        
    



