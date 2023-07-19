import treelib

from PytomatedLiquidHandling.API import Scheduler, TestSteps

Tree = treelib.Tree()

Tree.create_node(identifier="Sample", data=TestSteps.LiquidTransfer("Sample"))
Tree.create_node(
    identifier="Diluent", parent="Sample", data=TestSteps.LiquidTransfer("Diluent")
)
Tree.create_node(
    identifier="DTT", parent="Sample", data=TestSteps.LiquidTransfer("DTT")
)

Tree.show()

print(Scheduler.Method.MethodABC("Method", True, Tree).StartingTaskList)


quit()
