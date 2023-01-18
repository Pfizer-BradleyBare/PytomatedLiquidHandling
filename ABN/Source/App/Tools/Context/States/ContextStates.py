from enum import Enum


class ContextStates(Enum):
    Running = "Running"

    Waiting = "Waiting"

    Aborted = "Aborted"

    Complete = "Complete"

    Dequeued = "Dequeued"
