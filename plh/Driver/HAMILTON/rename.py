import os

for Root, Dirs, Files in os.walk(os.path.dirname(__file__)):
    for File in Files:
        Text = []
        All = []
        if "command.py" in Files:
            All.append('"Command"')
            Text.append("from .command import Command")
        if "response.py" in Files:
            All.append('"Response"')
            Text.append("from .response import Response")
        if "options.py" in Files:
            All.append('"Options"')
            # All.append('"ListedOptions"')
            Text.append("from .options import Options, ListedOptions")

        if "__init__.py" in File and "command.py" in Files:
            init = ""
            init += "\n".join(Text) + "\n\n"
            init += "__all__ = [" + ",".join(All) + ",]"
            file = open(os.path.join(Root, File), mode="w")
            file.write(init)
            file.close()
