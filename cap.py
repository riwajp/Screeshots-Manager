from pynput.keyboard import Key, KeyCode, Controller, Listener
import pyautogui
import os
import time
import sys
import shutil
from subprocess import Popen, PIPE
import json
import signal
import psutil

PATH = os.path.dirname(sys.executable)
# os.chdir(PATH)
base_path = "./"
args = sys.argv
errors = {101: "Hot keys and folder names is not set.",
          202: "Path for the screenshot folders is not set.",
          303: "No such directory to create path."}

folders = []


def error(code):
    sys.exit(errors[code])


def start():
    if (not status(0)):
        readPath()
        readFolders()
        flag = 0
        if (len(folders) == 0):
            error(101)
        current = {"base_path": base_path, "folders": folders}

        with open(PATH+"/"+"current.txt", 'w') as file:
            file.write(json.dumps(current))
        os.system("start /b capCapturer")
        print("Cap is running.")
        time.sleep(2)
        sys.exit()
    else:
        print("Cap is already running.")


def stop():

    for i in psutil.process_iter():
        if (i.name() == "capCapturer.exe"):
            os.kill(i.pid, signal.SIGTERM)
            break


def restart():

    if (status(print_status=0)):
        print("Restarting........")
        stop()
        start()


def run(command):

    commands[command]()


def readFolders():

    global folders
    try:
        settings = open(PATH+"/"+"settings.txt", "r")
    except:
        settings = open(PATH+"/"+"settings.txt", "w")
        settings.close()
        settings = open(PATH+"/"+"settings.txt", "r")

    lines = settings.readlines()

    folders = [line.rstrip() for line in lines if not line.isspace()]

    return folders


def setFolders(folder_list=[]):
    global folders
    readPath()
    if (len(folder_list) == 0):

        folders = args[2:]
    settings = open(PATH+"/"+"settings.txt", "w")

    for i, folder in enumerate(folders):
        settings.write(folder+"\n")
        try:
            os.mkdir(base_path+"/"+folder)
        except:
            continue

    settings.close()
    restart()


def setPath():
    global base_path
    readPath(0)
    config = open(PATH+"/"+"path.txt", "w")

    previous_base_path = base_path
    base_path = args[2]
    try:
        os.mkdir(args[2])
        config.write(args[2])
    except:

        error(303)
        pass
    config.close()

    readFolders()
    if (len(folders) > 0):
        print("The following folders already exist in previous path:")
        for i in folders:
            print(i+"       ")
        print("\n")
        c = input("Move these folders into new path? (y/n): ")
        if (c.lower() == "y"):
            for i in folders:

                shutil.move(os.path.abspath(previous_base_path+"/"+i),
                            os.path.abspath(base_path))
            shutil.rmtree(os.path.abspath(previous_base_path))
        else:
            setFolders(folders)
    restart()


def readPath(exit_mode=1):
    global base_path
    try:
        config = open(PATH+"/"+"path.txt", "r")
        base_path = config.readline()
    except:

        if (exit_mode):
            error(202)

    if (base_path.isspace() or base_path == ""):
        error(202)

    return base_path


def starter():

    #process = Popen(['python', 'indx.py', 'start'])
    start()


def status(print_status=1):

    processes = []
    for i in psutil.process_iter():
        processes.append(i.name())

    if ("capCapturer.exe" in processes):
        if (print_status):
            print("Cap is running.")
        return True
    else:
        if (print_status):
            print("Cap is not running.")
        return False


commands = {"start": starter, "set-folder": setFolders,
            "set-path": setPath, "stop": stop, "status": status}
if (len(args) == 1):
    print("Installing Cap.....")
    os.system("setx /M PATH \"%PATH%;"+PATH+";\"")
    print("setx /M PATH \"%PATH%;"+PATH+";\"")
    os.system("chmod +x cap")
    print("\n Cap installed succssfully! Now you can access cap from Command Line with command 'cap'.")
    input()
else:
    run(args[1])
