from unicodedata import name
import wmi
import time
start= time.time()
# Initializing the wmi constructor
f = wmi.WMI()

notAllowed = [
    "Discord",
    "Whatsapp",
    "Telegram",
    "Zoom",
    "Skype"
]
print("Name         Id")
x = f.Win32_Process()
for process in x:
    for name in notAllowed:
        if name.lower() in process.Name.lower():
            print(process.Name,process.ProcessId)

print("Found {} processes".format(len(x)))
end = time.time()
print("Executed in {} seconds".format(end-start))