"""Automatic Tracert Program by Varoon Doone"""""

import sys
import threading
import os
import subprocess
from tkinter.ttk import Progressbar
from tkinter import *
from tkinter import messagebox


# Declaring variables
programName = "notepad.exe"
google_ip = "-d 8.8.8.8" # "-d"; Do not resolve addresses to hostnames.


def update(msg): # to update progress bar window
    task_progress.set(msg)
    window.update()


def resource_path(relative_path):  # used to get path for cmd_icon.png; program icon
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def tracert():
    cmd = "tracert " + google_ip
    result = subprocess.check_output(cmd, shell=True)
    result = result.decode('UTF-8').rstrip()
    f = open(path, 'w')
    f.write("\nResults for Traceroute to Google's DNS Server Address(8.8.8.8):\n")
    f.write("\n------------------------------------------------------- \n")  # adding a seperator
    f.write(result)
    f.close()  # close file when finish


# root window
window = Tk()
window.title("Automatic Tracert Program")
window.geometry("400x100")
window.resizable(False, False)  # This code helps to disable windows from resizing
window.eval('tk::PlaceWindow . center')

icon = PhotoImage(file=resource_path("cmd_icon.png"))
window.iconphoto(True, icon)  # assign converted image to window

task_progress = StringVar()

# progressbar
pb = Progressbar(window, orient='horizontal', mode='indeterminate', length=280)
# place the progressbar
pb.pack(pady=10)

directory = os.getcwd() # Get current working directory
path = directory.replace("\\", "\\\\") + "\\\\tracert_results.txt" # append text file name to store output

spaceLabel = Label(window)
spaceLabel.pack()

taskLabel = Label(window, textvariable=task_progress)
taskLabel.pack()

try:
    x = threading.Thread(target=tracert)

    pb.start(10)
    update("Running Tracert command to Google's DNS Server Address(8.8.8.8)")
    window.after(500, x.start())
    z = x.is_alive()
    while z:
        window.update()
        z = x.is_alive()
    window.after(1000)
    update("Gathering Results")
    window.after(1000)
    pb.stop()
    pb.config(mode='determinate')
    pb['value'] += 100
    update("Completed")
    window.after(1000)
    subprocess.Popen([programName, path])
    window.after(250, window.destroy)
except Exception as e:
    os.remove(path)

window.mainloop()

