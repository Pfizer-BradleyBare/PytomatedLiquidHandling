import yaml
from .__TemplateTracker import _TemplateTracker


def LoadYaml(_TemplateTrackerInstance: _TemplateTracker, FilePath: str):
    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for _TemplateID in ConfigFile["__Template IDs"]:
        pass
