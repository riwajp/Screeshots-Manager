from pynput.keyboard import Key, KeyCode, Controller, Listener
import pyautogui
import time
import json
import os
import sys


PATH = os.path.dirname(sys.executable)


def start():
    flag = 0
    current = open(PATH+"/"+"current.txt", 'r')
    data = json.loads(current.readline())
    folders = data["folders"]
    base_path = data["base_path"]

    def onPress(key):

        global flag

        if (key == Key.print_screen):
            flag = 1
        else:
            try:
                num = key.char
            except:

                return

            if (key.char.isnumeric() and int(key.char) <= len(folders) and flag == 1):
                screenshot = pyautogui.screenshot()
                screenshot.save(
                    base_path+"/"+folders[int(key.char)-1]+f"/{time.time()}.png")
                print("save ss")
                flag = 0
            else:
                flag = 0

    listener = Listener(on_press=onPress)

    listener.start()


start()
statusfile = open(PATH+"/"+"status.txt", "w")
ctime = time.time()
print(ctime)
statusfile.write(str(os.getpid()))

while True:
    '''
    if (time.time()-ctime >= 5):
        statusfile.write(str(id)+"\n"+str(ctime))
        print(ctime)

        ctime = time.time()
        '''
    pass
statusfile.close()
