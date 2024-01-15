from __future__ import annotations

if True:
    pass
# This MUST come first so the if statement ensures that it does not get reordered by a formatter


identifier = str
devices: dict[identifier, Base.PipetteABC] = {}
