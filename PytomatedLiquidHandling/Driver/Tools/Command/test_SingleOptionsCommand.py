import pytest

from ....Tools.AbstractClasses import ObjectABC
from .BaseCommand import ClassDecorator_Command, ExpectedResponseProperty
from .SingleOptionsCommand import SingleOptionsCommand


class Options(ObjectABC):
    def __init__(self, a, b, c):
        ObjectABC.__init__(self)

        self.a = a
        self.b = b
        self.c = c

    def GetName(self):
        return self.a


@ClassDecorator_Command(__file__)
class Command(SingleOptionsCommand[Options]):
    ...

    @ExpectedResponseProperty
    def GetTemperature(self) -> any:  # type:ignore
        ...

    def HandleErrors(self):
        ...


def test():

    CommandInstance = Command("Test", Options("T1", 1, 2), True)

    assert CommandInstance.GetName() == "Test"
    assert CommandInstance.GetCommandName() == "Command"
    assert CommandInstance.GetModuleName() == "Tools"

    assert CommandInstance.GetExpectedResponseProperties() == ["Temperature"]

    assert CommandInstance.ResponseEvent.is_set() == False

    assert CommandInstance.GetCommandParameters() == {
        "a": "T1",
        "b": 1,
        "c": 2,
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
