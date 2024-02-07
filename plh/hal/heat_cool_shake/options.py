from __future__ import annotations

from pydantic import dataclasses

from plh.hal import layout_item as li


@dataclasses.dataclass(kw_only=True)
class HeatCoolShakeOptions:
    layout_item: li.LayoutItemBase | None
    temperature: None | float
    rpm: None | int
