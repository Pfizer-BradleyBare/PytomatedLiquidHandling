from __future__ import annotations

from plh.api import container

a = container.Liquid()
b = container.Liquid()

well = container.Well((a,100),(b,500))



print(well.get_well_property(lambda x: x.polarity))

