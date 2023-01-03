from enum import Enum


class ContextStates(Enum):
    def __init__(self, a, b):
        self.State = a
        self.Reason = b

    Running = (
        "Running",
        "Method is running normally. No interaction from the user is required.",
    )

    WaitingPaused = (
        "Waiting: Paused",
        "User paused this method manually. Method will not proceed until unpaused.",
    )

    WaitingDeckLoading = (
        "Waiting: Deck Loading",
        "The method is ready to run but the deck must be loaded first. Please proceed to load the deck.",
    )

    WaitingTimer = (
        "Waiting: Timer",
        "The method is running correctly but no contexts are active. Most likely waiting on a timer of some sort.",
    )

    WaitingNotification = (
        "Waiting: Notification",
        "A notification was fired that waits on the user before proceeding. Please confirm the notification to continue.",
    )

    WaitingError = (
        "Waiting: Error",
        "An error occured. Please correct.",  # TODO
    )

    Aborted = (
        "Aborted",
        "User has aborted this method manually. Only deck unloading is allowed.",
    )
    # The user stopped the method but it is still in the list. This allows the user to remove plates and all that jazz

    Complete = (
        "Complete",
        "Method execution is complete. Only deck unloading is allowed.",
    )
    # The user stopped the method but it is still in the list. This allows the user to remove plates and all that jazz

    Dequeued = (
        "Dequeued",
        "Method no longer 'exists' in the system. This is here for book keeping only. User will never see this state.",
    )
    # The user stopped the method but it is still in the list. This allows the user to remove plates and all that jazz
