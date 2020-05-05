import shutil
import os.path
from watchdog.observers import Observer
import time
from watchdog.events import FileSystemEventHandler
import os
import re


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        moveFiles()


def moveFiles():
    i = 0
    fileList = os.listdir(folder_to_track)
    #while i < (len(os.listdir(folder_to_track)) - len(notToMove)):
    for fileName in fileList:
        if notToMove.count(str(fileName)) > 0:
            print("Cant/shouldn't move file: " + fileName)
        else:
            destination_folder = decideFolder(getExtension(fileName))
            print(fileName + " --> " + destination_folder)
            src = folder_to_track + "/" + fileName
            new_destination = destination_folder + "/" + fileName
            try:
                shutil.move(src, new_destination)
            except:
                print("Couldn't move file")
                fileList.remove(fileName)
                notToMove.append(fileName)
        i = i + 1


def getExtension(filename):
    pattern = re.compile(".")
    if (pattern.match(filename)):
        filename = filename.split(".")
        print(filename)
        return filename[len(filename) - 1]
    else:
        return filename


def decideFolder(fileExtension):
    fileExtension.lower
    i = 0
    while i < (len(extensions) - 1):
        if (extensions[i] != extensions[len(extensions) - 1][0]):
            try:
                if extensions[i][1].count(str(fileExtension)) > 0:
                    return os.getcwd() + "/" + extensions[i][0]
            except:
                return os.getcwd() + "/" + extensions[len(extensions) - 1][0]
                print("Something went wrong with checking for directory")

        i = i + 1
    time.sleep(1)
    return os.getcwd() + "/" + extensions[len(extensions) - 1][0]


def checkFolder(folder):
    dirToMake = os.getcwd() + "/" + folder
    try:
        os.mkdir(dirToMake)
        print("Folder made: " + dirToMake)
    except FileExistsError:
        print("Folder exist already: " + dirToMake)
    except:
        print("Couldn't create folder: " + dirToMake)


def runTool():
    print("Tool started")
    moveFiles()
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_to_track, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


notToMove = [".DS_Store", ".crdownload"]
extensions = [["01 images", ["png", "ico", "tiff", "jpg", "jpeg", "gif"]],
              ["02 docs", ["doc", "docx", "pdf"]],
              ["03 compressed", ["zip", "tgz", "rar"]],
              ["04 applications", ["dmg", "exe", "py", "jar", "app"]],
              ["05 web", ["html", "php", "css", "js"]],
              ["99 remainders"]]

folder_to_track = '/Users/dante/Downloads'

for folder in extensions:
    checkFolder(folder[0])

runTool()
