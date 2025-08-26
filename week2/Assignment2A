import os, random #It's a function to interact with the operating system.
from datetime import datetime, timedelta

if os.system("schtasks /query /tn SecurityScan") == 0: #<<-- schtasks is used to schedule a task
    os.system("schtasks /delete /f /tn SecurityScan")
#/tn: Specifies the task name as SecurityScan
print("I am doing a malicious task, try to delete the task") #The malicious task.

filedir = os.path.join(os.getcwd(),"Scheduling_Malicious_Tasks.py")
#os.path.join this part means to join the directory path and file name together into one valid file path.
#In here the os.getcwd() it means to get the current working directory.
#And the "Scheduling_Malicious_Tasks.py" is the filename that I want to point to.


maxInterval = 1 #This means that the task will schedule again after 1 minute.
#If we raised the maxInterval then it will take longer between the times the task will run again.

interval = 1+(random.random()*(maxInterval-1))
dt = datetime.now() + timedelta(minutes=interval)

#Date and time gets the current date and time of the system
#rom the system clock -- timedelta: Is a function it is used for calculating differences in dates. And it is used for
#Date manipulations.
#The timedelta function allows us to convert our interval into minutes and add it to the current time calculated
#with using datetime.now(). Storing the result in dt.

t = "%s:%s" % (str(dt.hour).zfill(2), str(dt.minute).zfill(2))
d = "%s/%s/%s" % (str(dt.month).zfill(2),str(dt.day).zfill(2),dt.year)
#The above codes are date and time using string operations. The command that has "%s:%s" % (str(dt.hour).zfill(2), str(dt.minute).zfill(2))
#So basically it means taking time and the date, times in hours:minutes abd date in Month/day/Year and passing them into the task which is schtasks /create.

os.system('schtasks /create /tn SecurityScan /tr "%s" /sc once /st %s /sd %s' % (filedir, t, d))
#/tr: Indicates the task to be run at that time (The malicious file)
#/sc: Defines how often the task should be repeated.
#/st: Sets the time at which the task should be run.
#/sd: Sets the date at which the task should be run.
input()

#This code is similar to Logic Bombs attacks where is there is a malicious peace of code that can be triggered after a certain time or under some conditions
#The attackers set.
#To kill this code, please run the following command on command prompt with administrator privilege: schtasks /delete /f /tn SecurityScan
