import os, pathlib, subprocess
import json


def CheckValidTask(creator, task): #CheckValidTask is a function which checks if scheduled tasks looks a safe task or a suspicious task.

    allowlist = ["Microsoft", "Mozilla", "Adobe Systems Incorporated"] #This is an allowlist that is linked to the creator scheduled task.
    #So in other terms if a scheduled task creator name starts with one of these strings for example Microsoft then when you run this code it will find if a task
    #creator matched Microsoft.
    extensions = [".exe", ".py", ".dll"]
    #These are a list of file types that the code needs to pay attention for.

    trusted = any(creator.startswith(x) for x in allowlist) #This checks the creators filed and compares between each string in the allowlist.
    #If the creators name starts with one of the allowlist strings (e.g., Microsoft) then it means trusted and gives true but if they are not from the allow list
    #Then it will give false.
    executable = any(ext in task.lower() for ext in extensions)
    #This one is the same thing for creator but the difference is that it is for file extensions.

    if executable:
        exe = task.split(" ")[0] #In here the task is a=the command that the scheduled tasks runs. And task.split("") splits the strings into peaces.
        #[0] The 0 in here means that take the first part which is the path to the program.
        p = os.path.expandvars(exe).lower() #In this code is used to expand the environment variable names in the given path, it replaces substrings
        #of the form %name%. So basically if the scheduled task runs in this format %SystemRoot%, the expandvars() will replace %SystemRoot% with C:/Windows.

        if p.startswith(r"c:\windows\system32") or p.startswith(r"c:\\windows\\system32"):
            return True
        else:
            return trusted
    else:
        return True


output_bytes = subprocess.check_output(
    'schtasks /query /v /fo csv /nh', shell=True
)
output = output_bytes.decode(errors="ignore").splitlines()
results = [o.split(',') for o in output]
#In the above code runs the windows schtasks and lists all the scheduled tasks and then it makes them in readable text.
scheduled_task_snapshot = "scheduled_task_snapshot.json" #This sets the file name where the tasks will be stored
#In Json format.
current_names = [r[1].strip('"') for r in results if len(r) > 8]
#This code will list all the current tasks.
if os.path.exists(scheduled_task_snapshot):
    with open(scheduled_task_snapshot, "r", encoding="utf-8") as f: #This opens file in read mode.
        try:
            baseline_names = json.load(f) #This reads json file contents and converts it into python object.

        except json.JSONDecodeError:
            baseline_names = [] #This means if the JSON file is corrupted or empty, then reset baseline names to an empty list.
else:
    baseline_names = []
    with open(scheduled_task_snapshot, "w", encoding="utf-8") as f:
        json.dump(current_names, f, indent=2)
    print("Snapshot file created (scheduled_task_snapshot.json). Run again to compare against this baseline.")
    exit(0) #This will exit after creating the baseline script.

for res in results:
    result = [x.strip('"') for x in res]
    if len(result) > 8:
        name = result[1]
        creator = result[7]
        task = result[8]
        if not CheckValidTask(creator, task):
            print(f"{name}, {creator}, {task},")

        if name not in baseline_names:
            print(f"New Task Detected since baseline: {name}, {creator}, {task},")

with open(scheduled_task_snapshot, "w", encoding="utf-8") as f:
    json.dump(current_names, f, indent=2) #This will update the snapshot file with latest task names so everytime we run the code it will give back the results and then it can be compared if any new tasks were added
#In this final code it goes through every scheduled task on the system and picks out the task name, creator and the action, and runs them through the security
#check to see if the task looks suspicious. If it is suspicious then it prints it's details. And it will dump all tasks in a json file



