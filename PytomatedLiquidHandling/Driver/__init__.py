"""
Driver layer facilitates raw command execution on a system.

The driver layer is designed as a execute, wait, response system. Only one command can be queued at any given time on a backend. In some cases (Hamilton), there may
be multiple command types per backend. In that case you are allowed to execute each command type at the same time.

The driver layer is not exclusive to automation platforms. UV readers, tube openers, freezers, etc. are all in scope of the driver layer.

You are expected to handle raw errors from the system in the driver layer. Those error are grouped with each command as applicable.

The following base classes (found in tools) are provided to create new drivers:
    BackendABC

    SimpleBackendABC

    ServerBackendABC

    CommandABC

    CommandOptions

    CommandOptionsListed

    OptionsABC
    
    ResponseABC
"""

from . import Hamilton, UnchainedLabs
