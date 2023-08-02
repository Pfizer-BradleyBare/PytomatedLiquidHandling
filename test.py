from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import networkx
import processscheduler as ps


from PytomatedLiquidHandling.API import ExecutionEngine

problem = ps.SchedulingProblem(
    "SoftwareDevelopment", delta_time=timedelta(seconds=1), start_time=datetime.now()
)

preliminary_design = ps.FixedDurationTask("PreliminaryDesign", duration=120)  # 1 day
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

print(solution)
solution.render_gantt_plotly()

# quit()
