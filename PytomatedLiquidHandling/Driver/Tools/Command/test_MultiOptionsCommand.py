import pytest

from ....Tools.AbstractClasses import NonUniqueObjectTrackerABC, NonUniqueObjectABC
from .BaseCommand import ClassDecorator_Command, ExpectedResponseProperty
from .MultiOptionsCommand import MultiOptionsCommand


class Options(NonUniqueObjectABC):
    def __init__(self, d, e, f):
        NonUniqueObjectABC.__init__(self)

        self.a = d
        self.b = e
        self.c = f

    def GetName(self):
        return self.a


class OptionsTracker(NonUniqueObjectTrackerABC[Options]):
    ...


@ClassDecorator_Command(__file__)
class Command(MultiOptionsCommand[OptionsTracker]):
    ...

    @ExpectedResponseProperty
    def GetTemperature(self) -> int:
        ...

    def HandleErrors(self):
        ...


def test():

    OptionsTrackerInstance = OptionsTracker()

    OptionsTrackerInstance.ManualLoad(Options("T1", 1, 2))
    OptionsTrackerInstance.ManualLoad(Options("T2", 3, 4))
    OptionsTrackerInstance.ManualLoad(Options("T3", 5, 6))

    CommandInstance = Command(OptionsTrackerInstance, True)

    assert CommandInstance.GetCommandName() == "Command"
    assert CommandInstance.GetModuleName() == "Tools"

    assert CommandInstance.GetExpectedResponseProperties() == ["Temperature"]

    assert CommandInstance.ResponseEvent.is_set() == False

    assert CommandInstance.GetCommandParameters() == {
        "a": ["T1", "T2", "T3"],
        "b": [1, 3, 5],
        "c": [2, 4, 6],
    }

    with pytest.raises(Exception):
        CommandInstance.GetResponseState()

    with pytest.raises(Exception):
        CommandInstance.GetResponseMessage()

    with pytest.raises(Exception):
        CommandInstance.GetTemperature()

    CommandInstance.ResponseEvent.set()

    CommandInstance.ResponseState = True
    CommandInstance.ResponseMessage = "Test"
    CommandInstance.ResponseProperties = {"Temperature": 100}

    assert CommandInstance.GetResponseState() == True
    assert CommandInstance.GetResponseMessage() == "Test"
    assert CommandInstance.GetTemperature() == 100
