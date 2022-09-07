from ..HAL import Hal, HalLoader
from ..API.Workbook import WorkbookTracker

WorkbookTrackerInstance: WorkbookTracker
HalInstance: Hal


def Initialize():
    global WorkbookTrackerInstance

    WorkbookTrackerInstance = WorkbookTracker()
    # The workbook tracker will load many difference workbooks over time. Loading does not occur here

    global HalInstance

    HalInstance = Hal()
    HalLoader.Load(HalInstance)
    # The Hal info is loaded only once here
