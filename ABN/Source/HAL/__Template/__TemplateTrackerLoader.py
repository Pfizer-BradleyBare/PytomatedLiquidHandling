import yaml

from .__TemplateTracker import _TemplateTracker


def LoadYaml(FilePath: str) -> _TemplateTracker:
    _TemplateTrackerInstance = _TemplateTracker()

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for _TemplateID in ConfigFile["__Template IDs"]:
        pass

    return _TemplateTrackerInstance
