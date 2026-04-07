# You are supposed to create FOLDERS from today's date
# to till 31/12/2026
# Each Folder must have 3 files
# <DDMMYYYY>.txt
# <DDMMYYYY>.json
# <DDMMYYYY>.py
#
# Inside each file you are required to write text
# "File was created at <DD-MM-YYY TIME>

import os
from datetime import datetime, timedelta
os.chdir("D:\prectice\pythonProject\Date_Folder")
start_date = datetime.today().date()


end_date = datetime(2026, 12, 31).date()

current_date = start_date

while current_date <= end_date:

    folder_name = current_date.strftime("%d%m%Y")
    file_date_format = current_date.strftime("%d-%m-%Y")
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


    os.makedirs(folder_name, exist_ok=True)


    txt_file = os.path.join(folder_name, f"{folder_name}.txt")
    json_file = os.path.join(folder_name, f"{folder_name}.json")
    py_file = os.path.join(folder_name, f"{folder_name}.py")

    content = f"File was created at {timestamp}"


    for file in [txt_file, json_file, py_file]:
        with open(file, "w") as f:
            f.write(content)


    current_date += timedelta(days=1)

print("All folders and files created successfully!")
