import yaml
from .__TemplateTracker import __TemplateTracker


def LoadYaml(_TemplateTrackerInstance: __TemplateTracker, FilePath: str):
    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for _TemplateID in ConfigFile["__Template IDs"]:
        pass
