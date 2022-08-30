import yaml
from .NotifyTracker import NotifyTracker
from .Notify import EmailTextNotify, NotificationTypes


def LoadYaml(NotifyTrackerInstance: NotifyTracker, FilePath: str):
    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for NotifyID in ConfigFile["Notify IDs"]:
        Enabled = ConfigFile["Notify IDs"][NotifyID]["Enabled"]

        Type = NotificationTypes(NotifyID)

        if Type == NotificationTypes.EmailText:
            DeviceID = ConfigFile["Notify IDs"][NotifyID]["Device ID"]
            SMTPServer = ConfigFile["Notify IDs"][NotifyID]["SMTP Server"]
            SenderEmail = ConfigFile["Notify IDs"][NotifyID]["Sender Email"]
            AlwaysNotifyEmails = ConfigFile["Notify IDs"][NotifyID][
                "Always Notify Emails"
            ]

            NotifyTrackerInstance.LoadManual(
                EmailTextNotify(
                    Enabled, DeviceID, SMTPServer, SenderEmail, AlwaysNotifyEmails
                )
            )
