import os

for Root, Dirs, Files in os.walk(os.path.dirname(__file__)):
    for File in Files:
        if "Exceptions.py" in File:
            os.rename(os.path.join(Root, File), os.path.join(Root, File.lower()))
