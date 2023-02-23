from abc import ABC, abstractmethod


# should log block, comments for a block, commands for a block
# Block contains comments and generates commands
# Block object will have comments and commands as members
class LoggerCommand:
    ...


class LoggerComment:
    def __init__(self, Comment: str):
        self.Comment: str = Comment


class LoggerBlock(ABC):
    def __init__(self):
        self.ListOfComments: list[LoggerComment] = list()
        self.ListOfCommands: list[LoggerCommand] = list()

    @abstractmethod
    def GetUniqueKey(self) -> str:
        ...

    def AddComment(self, CommentInstance: LoggerComment):
        self.ListOfComments.append(CommentInstance)

    @abstractmethod
    def IsSame(self, LoggerBlockInstance: Self):
        if self == LoggerBlockInstance:
            return True
        return False

    @abstractmethod
    def GetBlockInformation(self) -> dict[str, str]:
        ...


class ExampleBlock(LoggerBlock):
    def GetBlockInformation(self) -> dict[str, str]:
        return {"str": "str"}


class Logger:
    def __init__(self):
        self.ListOfLoggerBlocks: list[LoggerBlock] = list()

    def AddLoggerBlock(self, LoggerBlockInstance: LoggerBlock):
        self.ListOfLoggerBlocks.append(LoggerBlockInstance)

    def PrintLog(self):
        for Block in self.ListOfLoggerBlocks:
            print(Block.GetBlockInformation())
            for Comment in Block.ListOfComments:
                print(Comment.Comment)


LoggerInstance = Logger()

LoggerBlockInstance = ExampleBlock()
LoggerInstance.AddLoggerBlock(LoggerBlockInstance)
# Created then added a logger block to our logger

LoggerBlockInstance.AddComment(LoggerComment("Success Comment"))
# block 1


LoggerInstance.AddLoggerBlock(ExampleBlock())
# Created then added a logger block to our logger
# block 2

LoggerInstance.AddLoggerBlock(ExampleBlock())
# Created then added a logger block to our logger
# block 3

LoggerInstance.AddLoggerBlock(ExampleBlock())
# Created then added a logger block to our logger
# block 4

LoggerInstance.PrintLog()
