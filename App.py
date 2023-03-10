import sys

sys.dont_write_bytecode = True

from App.Handler import Handler
from App.Tools.Excel import CloseHidden

if __name__ == "__main__":

    while CloseHidden() != 0:
        ...
    # This ensures that all non visible excel apps are closed.
    # Books will automatically be saved then closed before the app is killed.

    HandlerInstance = Handler()

    HandlerInstance.StartServer()
    HandlerInstance.WaitForKill()
