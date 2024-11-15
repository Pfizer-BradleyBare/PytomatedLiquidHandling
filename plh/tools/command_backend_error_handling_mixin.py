import dataclasses


@dataclasses.dataclass(kw_only=True)
class CommandBackendErrorHandlingMixin:
    """Mixin for command.
    This gives your command the ability to have errors handled by the user in the backend software.
    """

    backend_error_handling: bool
