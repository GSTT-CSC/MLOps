import yaml
import glob, os
import re

from prettytable import PrettyTable
from datetime import datetime

cur_dir = os.getcwd()
#file_name = 'Experiment' + re.findall(".+\/(.+)$", cur_dir)[0] +'.csv'
folders = next(os.walk(cur_dir))[1]
#file_path = os.path.join(cur_dir, file_name)

def view():
    yaml_files = []
    for folder in folders:
        total_size = 0
        totalFiles = 0
        totalDir = 0
        date_mod = []
        project_path = os.path.join(cur_dir, folder)
        os.chdir(project_path)

        for dirpath, dirnames, filenames in os.walk(project_path):
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
        
        for yfile in glob.glob("*_Project.yaml"):
            #print(yfile)
                #if f.endswith("_Project.yaml"):
            yaml_path = os.path.join(project_path, yfile)
            yaml_files.append(yaml_path)
            with open(yfile) as file:
                doc = yaml.load(file, Loader=yaml.FullLoader)
            #print(doc)
            if len(date_mod) > 0:
                date_modified = max(date_mod)
            else:
                date_modified = "not found"
            doc[6]= {"Last updated" : date_modified}
            doc[7]= {'Project Size (Mb)' : total_size/1000000}
            doc[8]= {'Number of folders' : totalDir}
            doc[9]= {'Number of files' : totalFiles}
            #print(doc)
            with open(yfile, 'w') as file:
                documents = yaml.dump(doc, file)
            print("Yaml file successfully updated:\n" + yaml_path )
    os.chdir(cur_dir)                
    t = PrettyTable(['Project UID', 
        'Project name', 
        'Project start date',
        'Pathologies', 
        'Anomalies', 
        'Experiments', 
        'Last updated', 
        'Project Size (Mb)',
        'Number of folders',
        'Number of files'
        ])
    for file in yaml_files:
        print(file)
        with open(file) as file:
            doc = yaml.load(file, Loader=yaml.FullLoader)
        data1 = doc[0].get("Project UID")
        data2 = doc[1].get("Project name")
        data3 = doc[2].get("Project start date")
        data4 = doc[3].get("Pathologies")
        data5 = doc[4].get("Anomalies")
        data6 = doc[5].get("Experiments")
        data7 = doc[6].get("Last updated")
        data8 = doc[7].get("Project Size (Mb)")
        data9 = doc[8].get("Number of folders")
        data10 = doc[9].get("Number of files")
        t.add_row([data1, data2, data3, data4, data5, data6, data7, data8, data9, data10])
    print(t)
