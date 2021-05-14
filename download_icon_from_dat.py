import os
import threading
from queue import Queue
import time
import json
import requests
from PIL import Image
from io import BytesIO

# Enable multi-threading queue
q_in = Queue(maxsize=0)
num_worker_threads = 10

def worker(thread_id):
    """Get tasks from queue and execute them"""
    while True:
        root, filename = q_in.get()
        get_icons(root, filename, thread_id)
        q_in.task_done()

def main():
    # Start worker threads
    for i in range(num_worker_threads):
        t = threading.Thread(target=worker, args=(i,))
        t.daemon = True
        t.start()

    # Put each '.dat' file into the queue for download
    for root, dirs, files in os.walk("."):
        for filename in files:
            if filename[-4::] == '.dat':
                q_in.put([root, filename])

    q_in.join()
    print("Complete.")

def get_icons(root, filename, num):
    # Load data file in JSON format
    with open(os.path.join(root, filename)) as json_file:
        data = json.load(json_file)
    # Create working path to store image downloads and logfile
    category = filename[0:-4]
    new_path = os.path.join(root, category)
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    logfile = open("log-" + category + "-" + str(int(time.time())) + ".txt", "w")
           
    # Download all app icons
    log("+ [Thread " + str(num) + "] Started category " + category + ':', logfile, 1)
    for i in range (0, len(data)):
        appId = id_sanitize((data[i])['appId'])
        url = (data[i])['icon']
        installs = (data[i])['installs']
        score = (data[i])['score']
        log("\t[" + str(i + 1) + "/" + str(len(data)) + "] " + "Downloading icon of " + appId, logfile, 0)
        r = requests.get(url, allow_redirects=True)
        # If image malformed or other error, skip
        try:
            icon = Image.open(BytesIO(r.content))
            icon.save(new_path + '\\' + appId + '_' + str(score) + '_' + str(installs) + '.png')
        except Exception as e:
            log("! [Thread " + str(num) + "] ERROR: cat:{" + category + "} appId:{" + appId + "} message:{" + str(e) + "}", logfile, 1)
            logfile.flush()   
    log("- [Thread " + str(num) + "] Finished category " + category + '.', logfile, 1)
    logfile.flush()
                    
def id_sanitize(string):
    """ Ensures appId has valid characters for use as filename in NTFS. """
    string = string.encode("ascii", errors="ignore").decode()
    invalid_chars = {'<','>',':','"','/','\\','|','?','*','_'}
    invalid_substrings = {"CON.", "PRN.", "AUX.", "NUL.", "COM1.", "COM2.", "COM3.", "COM4.", "COM5.", "COM6.", "COM7.",
                         "COM8.", "COM9.", "LPT1.", "LPT2.", "LPT3.", "LPT4.", "LPT5.", "LPT6.", "LPT7.", "LPT8.", "LPT9."}
    for char in invalid_chars:
        string = string.replace(char, '')
    for sub in invalid_substrings:
        string = string.replace(sub, '')
        string = string.replace(sub.lower(), '')
    if len(string) > 127:
        string = string[0:127]
    return string

def log(string, logfile, verbose):
    """ Print to log file. """
    logfile.write(string + '\n')
    if verbose == 1:
        print(string)

main()