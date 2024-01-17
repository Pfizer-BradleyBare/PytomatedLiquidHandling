from __future__ import annotations

import dataclasses
from collections import defaultdict
from enum import Enum
from typing import Any, TypeVar

from plh.driver.tools import (
    CommandBase,
    CommandOptionsListMixin,
    CommandOptionsMixin,
)

CommandSelf = TypeVar("CommandSelf", bound="HamiltonCommandBase")


@dataclasses.dataclass(kw_only=True)
class HamiltonCommandBase(CommandBase):
    def serialize_options(self: HamiltonCommandBase) -> dict[str, Any]:
        if isinstance(self, CommandOptionsMixin):
            output = vars(self.options)

            for key, value in output.items():
                if isinstance(value, Enum):
                    output[key] = value.value
                else:
                    output[key] = value

            return output

        if isinstance(self, CommandOptionsListMixin):
            output = defaultdict(list)

            for options in self.options:
                options_dict = vars(options)

                for key, value in options_dict.items():
                    if isinstance(value, Enum):
                        output[key].append(value.value)
                    else:
                        output[key].append(value)

            if not isinstance(self.options, list):
                output = output | vars(self.options)
            # custom list type so we need to get extra options.

            for key, value in output.items():
                if isinstance(value, Enum):
                    output[key] = value.value
                else:
                    output[key] = value

            return dict(output)

        return {}
