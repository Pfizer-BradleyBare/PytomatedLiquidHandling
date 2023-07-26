from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar, Callable, Self


from typing import Generic, TypeVar, cast


N = TypeVar("N", bound="Base.Nested")


class Base(Generic[N]):
    nested_instance: N

    class Nested:
        pass

    def __init__(self) -> None:
        self.nested_instance = cast(N, self.Nested())


class Sub(Base["Sub.Nested"]):
    class Nested(Base.Nested):
        pass


def get_nested(obj: Base[N]) -> N:
    return obj.nested_instance


def assert_instance_of_nested(nested_obj: N, cls: type[Base[N]]) -> None:
    assert isinstance(nested_obj, cls.Nested)


if __name__ == "__main__":
    sub = Sub()
    nested = get_nested(sub)
    assert_instance_of_nested(nested, Sub)

quit()


@dataclass(frozen=True)
class CommandGrouping:
    Execute: Callable[[], None]
    ExecutionTime: Callable[[], float]

    @dataclass
    class Options:
        a: str


@dataclass
class Container(ABC):
    OpenCommand: CommandGrouping = field(init=False)
    CloseCommand: CommandGrouping = field(init=False)

    @abstractmethod
    def _Open(self):
        ...

    @abstractmethod
    def _TimeToOpen(self) -> float:
        ...

    @abstractmethod
    def _Close(self):
        ...

    @abstractmethod
    def _TimeToClose(self) -> float:
        ...

    def __post_init__(self):
        self.OpenCommand = CommandGrouping(self._Open, self._TimeToOpen)
        self.CloseCommand = CommandGrouping(self._Close, self._TimeToClose)


@dataclass
class Tube(Container):
    def _Open(self):
        # do open
        ...

    def _TimeToOpen(self) -> float:
        # Calculate time required to open
        ...

    def _Close(self):
        # do close
        ...

    def _TimeToClose(self) -> float:
        # Calculate time required to close
        ...


TubeInstance = Tube()
TubeInstance.OpenCommand.ExecutionTime()  # Get execution time
TubeInstance.OpenCommand.Execute()  # Execute
TubeInstance.OpenCommand.Options("")

quit()


import matplotlib.pyplot as plt
import networkx

from PytomatedLiquidHandling.API import Scheduler, TestSteps

G = networkx.DiGraph()
G.add_node("Sample", Step=TestSteps.LiquidTransfer("Sample"))
G.add_node("Diluent", Step=TestSteps.LiquidTransfer("Diluent"))
G.add_edge("Sample", "Diluent")

G.add_node("DTT", Step=TestSteps.LiquidTransfer("DTT"))
G.add_edge("Diluent", "DTT")

G.add_node("DTT Incubation", Step=TestSteps.Incubate("DTT Incubation"))
G.add_edge("DTT", "DTT Incubation")

G.add_node("DTT2", Step=TestSteps.LiquidTransfer("DTT2"))
G.add_edge("DTT", "DTT2")

G.add_node("DTT3", Step=TestSteps.LiquidTransfer("DTT3"))
G.add_edge("DTT2", "DTT3")

G.add_node("Continue", Step=TestSteps.LiquidTransfer("Continue"))
G.add_edge("DTT3", "Continue")
G.add_edge("DTT Incubation", "Continue")

G.add_node("Continue2", Step=TestSteps.LiquidTransfer("Continue2"))
G.add_edge("Continue", "Continue2")


Sched = Scheduler.Scheduler("", "")
Sched.QueueMethod(Scheduler.Method.Method("", G, False))

Sched.QueueMethod(Scheduler.Method.Method("1", G, False))
Sched.QueueMethod(Scheduler.Method.Method("2", G, False))
Sched.RescheduleTasks()


quit()

import processscheduler as ps

problem = ps.SchedulingProblem(
    "SoftwareDevelopment", delta_time=timedelta(days=1), start_time=datetime.now()
)

preliminary_design = ps.FixedDurationTask("PreliminaryDesign", duration=1)  # 1 day
core_development = ps.VariableDurationTask("CoreDevelopmenent", work_amount=10)
gui_development = ps.VariableDurationTask("GUIDevelopment", work_amount=15)
integration = ps.VariableDurationTask("Integration", work_amount=3)
tests_development = ps.VariableDurationTask("TestDevelopment", work_amount=8)
release = ps.ZeroDurationTask("ReleaseMilestone")

ps.TaskStartAt(preliminary_design, 0)
ps.TaskPrecedence(preliminary_design, core_development)
ps.TaskPrecedence(preliminary_design, gui_development)
ps.TaskPrecedence(gui_development, tests_development)
ps.TaskPrecedence(core_development, tests_development)
ps.TaskPrecedence(tests_development, integration)
ps.TaskPrecedence(integration, release)

elias = ps.Worker("Elias", productivity=2)  # cost in $/day
louis = ps.Worker("Louis", productivity=2)
elise = ps.Worker("Elise", productivity=3)
justine = ps.Worker("Justine", productivity=2)

preliminary_design.add_required_resources([elias, louis, elise, justine])
core_development.add_required_resources([louis, elise])
gui_development.add_required_resources([elise])
tests_development.add_required_resources([elias, louis])
integration.add_required_resources([justine])
release.add_required_resources([justine])

# solve
solver = ps.SchedulingSolver(problem)
solution = solver.solve()

# print(solution)
# solution.render_gantt_plotly()

# quit()
