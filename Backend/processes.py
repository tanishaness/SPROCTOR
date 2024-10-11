import wmi
import time

# Start the timer
start = time.time()

# Initializing the WMI constructor
f = wmi.WMI()

# List of not allowed applications
notAllowed = [
    "Discord",
    "Whatsapp",
    "Telegram",
    "Zoom",
    "Skype"
]

print("Name                          Id")
print("-------------------------------")

# Fetching all running processes
try:
    processes = f.Win32_Process()
    # Loop through each process
    for process in processes:
        for name in notAllowed:
            # Check if the process name matches any of the not allowed names
            if name.lower() in process.Name.lower():
                print(f"{process.Name:<30} {process.ProcessId}")

    print("\nFound {} processes".format(len(processes)))

except Exception as e:
    print("An error occurred: ", str(e))

# Calculate execution time
end = time.time()
print("Executed in {:.2f} seconds".format(end - start))
