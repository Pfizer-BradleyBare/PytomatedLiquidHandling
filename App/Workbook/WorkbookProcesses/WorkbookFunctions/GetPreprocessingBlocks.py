from ....Blocks import MergePlates
from ... import BlockTracker, Workbook
from ..WorkbookFunctions import IsDeadBlock


def GetPreprocessingBlocks(WorkbookInstance: Workbook) -> BlockTracker:

    PreprocessingReadyBlocksTrackerInstance = BlockTracker()

    for (
        PreprocessingBlockInstance
    ) in WorkbookInstance.PreprocessingBlocksTrackerInstance.GetObjectsAsList():

        SearchBlockInstance = PreprocessingBlockInstance

        if WorkbookInstance.ExecutedPreprocessingBlocksTrackerInstance.IsTracked(
            SearchBlockInstance.GetName()
        ) or WorkbookInstance.ExecutedBlocksTrackerInstance.IsTracked(
            SearchBlockInstance.GetName()
        ):
            continue
        # This block has already been preprocessed or executed

        if not WorkbookInstance.ContextTrackerInstance.IsTracked(
            SearchBlockInstance.GetContext()
        ):
            continue
        # If the block context is not yet available then we are not going to try to start preprocessing.
        # I want this to change in the future but it is good enough for now

        if IsDeadBlock(WorkbookInstance, SearchBlockInstance):
            WorkbookInstance.ExecutedPreprocessingBlocksTrackerInstance.ManualLoad(
                SearchBlockInstance
            )
            continue
        # If dead then we do not need to preprocess.

        while True:
            SearchBlockInstance = SearchBlockInstance.GetParentNode()

            if SearchBlockInstance is None:
                PreprocessingReadyBlocksTrackerInstance.ManualLoad(
                    PreprocessingBlockInstance
                )
                break
            # We found the root. This means that this preprocessing block is ready to start

            if WorkbookInstance.ExecutedBlocksTrackerInstance.IsTracked(
                SearchBlockInstance.GetName()
            ):
                continue
            # If the block has already been executed then we can skip it.

            if WorkbookInstance.PreprocessingBlocksTrackerInstance.IsTracked(
                SearchBlockInstance.GetName()
            ):
                break
            # There is a preceeding block that needs to be preprocessed. So we will skip this block for now
            # NOTE NOTE NOTE NOTE TODO There is a question if we need to only pay attention to blocks of same type or not. I say not for now

            if type(SearchBlockInstance).__name__ == MergePlates.__name__:
                break
            # We can not start a preprocessing device if an unexecuted merge plates step preceeds it.
        # We are going to walk backward until we find either a merge plates step, a preceeding preprocessing device, or the beginning of the method

    return PreprocessingReadyBlocksTrackerInstance
