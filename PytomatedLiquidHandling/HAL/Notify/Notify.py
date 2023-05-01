from enum import Enum

from ...Tools.AbstractClasses import UniqueObjectABC


class NotificationTypes(Enum):
    EmailText = "Email/Text Notification"


class Notify(UniqueObjectABC):
    def __init__(self, NotificationType: NotificationTypes):
        self.NotificationType: NotificationTypes = NotificationType

    def GetNotificationType(self) -> NotificationTypes:
        return self.NotificationType

    def GetUniqueIdentifier(self) -> str:
        return self.GetNotificationType().value


class EmailTextNotify(Notify):
    def __init__(
        self,
        AutomationDeviceID: str,
        SMTPServer: str,
        SenderEmailAddress: str,
        AlwaysNotifyEmails: list[str],
    ):
        Notify.__init__(self, NotificationTypes.EmailText)
        self.AutomationDeviceID: str = AutomationDeviceID
        self.SMTPServer: str = SMTPServer
        self.SenderEmailAddress: str = SenderEmailAddress
        self.AlwaysNotifyEmails: list[str] = AlwaysNotifyEmails

    def GetAutomationDeviceID(self) -> str:
        return self.AutomationDeviceID

    def GetSMTPServer(self) -> str:
        return self.SMTPServer

    def GetSenderEmailAddress(self) -> str:
        return self.SenderEmailAddress

    def GetAlwaysNotifyEmails(self) -> list[str]:
        return self.AlwaysNotifyEmails
