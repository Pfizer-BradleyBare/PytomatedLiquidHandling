from abc import ABC, abstractmethod

# This is an abstract loader class for loading configuration files



class ObjectABC(ABC):
    @abstractmethod
    def GetName(self) -> str | int:
        ...  # this doesn't actually raise an error. This is an abstract method so python will complain

'''This is for Avi and Diane
class myClass(ObjectABC):
    
    def GetName(self):
        return 'my inherited return'

myInstance = myClass()
print(myInstance.GetName())

class myClass1(ObjectABC):
    
    def GetName(self):
        return 'my inherited return1'

class myClass2(ObjectABC):
    
    def GetName(self):
        return 'my inherited return2'

class myClass3(ObjectABC):
    
    def GetName(self):
        return 'my inherited return3'

listOfInstClasses = [myClass1(), myClass2(), myClass3()]
for c in listOfInstClasses:
    print(c.GetName())
'''