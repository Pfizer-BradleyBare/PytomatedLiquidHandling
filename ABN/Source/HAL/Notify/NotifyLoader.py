import yaml

from .Notify import EmailTextNotify, NotificationTypes
from .NotifyTracker import NotifyTracker


def LoadYaml(FilePath: str) -> NotifyTracker:
    NotifyTrackerInstance = NotifyTracker()

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for NotifyID in ConfigFile["Notify IDs"]:

        if ConfigFile["Notify IDs"][NotifyID]["Enabled"] is True:

            Type = NotificationTypes(NotifyID)

            if Type == NotificationTypes.EmailText:
                DeviceID = ConfigFile["Notify IDs"][NotifyID]["Device ID"]
                SMTPServer = ConfigFile["Notify IDs"][NotifyID]["SMTP Server"]
                SenderEmail = ConfigFile["Notify IDs"][NotifyID]["Sender Email"]
                AlwaysNotifyEmails = ConfigFile["Notify IDs"][NotifyID][
                    "Always Notify Emails"
                ]

                NotifyTrackerInstance.ManualLoad(
                    EmailTextNotify(
                        DeviceID, SMTPServer, SenderEmail, AlwaysNotifyEmails
                    )
                )
    return NotifyTrackerInstance
