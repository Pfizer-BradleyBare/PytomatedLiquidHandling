from ..Steps import Steps as STEPS
from ..Labware import Plates as PLATES
from ...General import Log as LOG
from ...User import Samples as SAMPLES
from ...General import HamiltonIO as HAMILTONIO
from ...Hamilton.Commands import Pipette as PIPETTE

TITLE = "Serial Dilution"
SOURCE = "Source"
DILUENT = "Diluent"
STARTING_CONC = "Starting Concentration (mg/mL)"
TARGET_CONC = "Target Concentration (mg/mL)"
TARGET_VOL = "Target Volume (uL)"
FACTOR = "Max Dilution Factor (x)"
METHOD = "Dilution Method"

import json

IsUsedFlag = True

def IsUsed():
	return IsUsedFlag

#This function may modify the Mutable list if required
def Init(MutableStepsList):
	pass

def Step(step):
    
    ParentPlate = step.GetParentPlateName()

    Params = step.GetParameters()
    Sources = SAMPLES.Column(Params[SOURCE])
    Diluents = SAMPLES.Column(Params[DILUENT])
    StartConcs = SAMPLES.Column(Params[STARTING_CONC])
    EndConcs = SAMPLES.Column(Params[TARGET_CONC])
    Volumes = SAMPLES.Column(Params[TARGET_VOL])
    Factors = SAMPLES.Column(Params[FACTOR])
    Methods = SAMPLES.Column(Params[METHOD])

	#########################
	#########################
	#########################
	#### INPUT VALIDATION ###
	#########################
	#########################
	#########################
    
    MethodComments = []
        
    if len(MethodComments) != 0:
        LOG.LogMethodComment(step,MethodComments)

	#########################
	#########################
	#########################
	#### INPUT VALIDATION ###
	#########################
	#########################
	#########################

    StepSequences = PLATES.LABWARE.GetContextualSequences(step.GetContext())
    StepFactors = PLATES.LABWARE.GetContextualFactors(step.GetContext())

    SerialDilutionDict = {}
    for Index in range(0,len(StepFactors)):
        if StepFactors[Index] != 0:
            SequenceNumber = str(StepSequences[Index])
            if SequenceNumber in SerialDilutionDict.keys():
                SerialDilutionDict[SequenceNumber].append(Index + 1)
            else:
                SerialDilutionDict[SequenceNumber] = [Index + 1]
    #Figure out what samples are going to be diluted based on the factors, if the factor is not 0 then we assume that sample should be dilution in some form

    for Key in SerialDilutionDict:
        Item = SerialDilutionDict[Key]
        
        if Factors[Item[0]] == "Follow Starting and Target Concentration":
            for Well in Item[:]:
                Item.remove(Well)
                Item.append({"Destination Well Position":Well,"Starting Concentration":int(StartConcs[Well-1]), "Ending Concentration": int(EndConcs[Well-1])})
        else:
            ConcentrationIndex = Item[0] - 1
            StartingConcentration = StartConcs[ConcentrationIndex]
            TargetConcentration = EndConcs[ConcentrationIndex]
            #Get start and target, it is easy because in this case they must all be the same
                
            NumWells = len(Item)
            if StartingConcentration / (Factors[ConcentrationIndex] ** NumWells) > TargetConcentration:
                #We need to throw an error here
                pass
            
            if Methods[ConcentrationIndex] == "Use All Wells":
                ActualFactor = (StartingConcentration/TargetConcentration) ** (1/NumWells)

                Conc = StartingConcentration
                for Well in Item[:]:
                    Item.remove(Well)
                    Item.append({"Destination Well Position":Well,"Starting Concentration":Conc, "Ending Concentration": Conc/ActualFactor})
                    Conc = Conc / ActualFactor
                #Now lets determine the concentrations for each entry in the list

            else:
                FactorsList = []

                Conc = StartingConcentration
                for Index in range(0,NumWells):
                    Factor = Factors[ConcentrationIndex]
                    
                    if (Conc / Factor) <= TargetConcentration:
                        FactorsList.append(Conc / TargetConcentration)
                        break
                    FactorsList.append(Factor)
                    Conc = Conc / Factor
                
                NumFactors = len(FactorsList)
                ActualFactor = (StartingConcentration/TargetConcentration) ** (1/NumFactors)
                for Index in range(0,len(FactorsList)):
                    FactorsList[Index] = ActualFactor
                #Spread the dilution factor across all wells equally

                InsertNum = NumWells - NumFactors
                InsertPos = NumFactors - 1
                if InsertNum != 0:
                    for i in range(0,InsertNum):
                        FactorsList.insert(InsertPos,0)
                #Insert zeros into wells we will not use

                Conc = StartingConcentration
                for Well, Factor in zip(Item[:], FactorsList):
                    Item.remove(Well)
                    if Factor != 0:
                        Item.append({"Destination Well Position":Well,"Starting Concentration":Conc, "Ending Concentration": Conc/Factor})
                        Conc = Conc / Factor
                #Now lets determine the concentrations for each entry in the list
    #Whew! What a pain!

    for Key in SerialDilutionDict:
        for Item in SerialDilutionDict[Key]:
            Index = Item["Destination Well Position"] - 1

            if SerialDilutionDict[Key].index(Item) == 0:
                Item["Sample Source"] = Sources[Index]
                Item["Source Well Position"] = int(Key)
            else:
                Item["Sample Source"] = ParentPlate
                Item["Source Well Position"] = PreviousWellPosition

            Item["Sample Destination"] = ParentPlate

            Item["Diluent Source"] = Diluents[Index]
            Item["Diluent Destination"] = ParentPlate

            SampleVolume = Item["Ending Concentration"] * Volumes[Index] / Item["Starting Concentration"]
            Item["Sample Volume"] = SampleVolume
            Item["Diluent Volume"] = Volumes[Index] - SampleVolume

            PreviousWellPosition = Item["Destination Well Position"]
    #Now we need to figure out the dilution scheme given the target volume.
    #Also we are going to figure out the source and destination plate

    LiquidTransfer2DArray = []
    while True:
        LiquidTransfer = []
        for Key in SerialDilutionDict:
            try:
                LiquidTransfer.append(SerialDilutionDict[Key].pop(0))
            except:
                pass
        
        if len(LiquidTransfer) == 0:
            break
        LiquidTransfer2DArray.append(LiquidTransfer)
    #Create a 2D array of liquid transfers

    DestinationTransferSequences = []
    SourceTransferSequences = []

    FirstTransferSources = []
    FirstTransferDestinations = []
    FirstTransferVolumes = []

    SecondTransferSources = []
    SecondTransferDestinations = []
    SecondTransferVolumes = []

    for LiquidTransfer in LiquidTransfer2DArray:
        DestinationTransferSequences.append([Dict["Destination Well Position"] for Dict in LiquidTransfer])
        SourceTransferSequences.append([Dict["Source Well Position"] for Dict in LiquidTransfer])
        
        FirstTransferSources.append([Dict["Sample Source"] for Dict in LiquidTransfer])
        FirstTransferDestinations.append([Dict["Sample Destination"] for Dict in LiquidTransfer])
        FirstTransferVolumes.append([Dict["Sample Volume"] for Dict in LiquidTransfer])

        SecondTransferSources.append([Dict["Diluent Source"] for Dict in LiquidTransfer])
        SecondTransferDestinations.append([Dict["Diluent Destination"] for Dict in LiquidTransfer])
        SecondTransferVolumes.append([Dict["Diluent Volume"] for Dict in LiquidTransfer])
    #Alright well that was easy, now we just need to transfer the volumes.

    for Index2D in range(0,len(FirstTransferSources)):
        for Index1D in range(0,len(FirstTransferSources[Index2D])):
            if SecondTransferVolumes[Index2D][Index1D] > FirstTransferVolumes[Index2D][Index1D]:
                SourceSwap = SecondTransferSources[Index2D][Index1D]
                DestinationSwap = SecondTransferDestinations[Index2D][Index1D]
                VolumeSwap = SecondTransferVolumes[Index2D][Index1D]

                SecondTransferSources[Index2D][Index1D] = FirstTransferSources[Index2D][Index1D]
                SecondTransferDestinations[Index2D][Index1D] = FirstTransferDestinations[Index2D][Index1D]
                SecondTransferVolumes[Index2D][Index1D] = FirstTransferVolumes[Index2D][Index1D]

                FirstTransferSources[Index2D][Index1D] = SourceSwap
                FirstTransferDestinations[Index2D][Index1D] = DestinationSwap
                FirstTransferVolumes[Index2D][Index1D] = VolumeSwap
    #I want to swap the lowest volume and transfer that first. It makes liquid transfers more robust

    for Index in range(0,len(FirstTransferSources)):
        
        FirstSources = FirstTransferSources[Index]
        FirstSourceContextualStrings = PLATES.LABWARE.GetContextualStringsList(step,FirstSources)
        FirstSourceContextualStringsSerialDilution = ["__SERIAL_DILUTION_SOURCE__:" + Context if Context is not None else None for Context in FirstSourceContextualStrings]
        FirstDestinations = FirstTransferDestinations[Index]
        FirstDestinationsContextualStrings = PLATES.LABWARE.GetContextualStringsList(step,FirstDestinations)
        FirstDestinationsContextualStringsSerialDilution = ["__SERIAL_DILUTION_DESTINATION__:" + Context if Context is not None else None for Context in FirstDestinationsContextualStrings]
        FirstVolumes = FirstTransferVolumes[Index]

        SecondSources = SecondTransferSources[Index]
        SecondSourceContextualStrings = PLATES.LABWARE.GetContextualStringsList(step,SecondSources)
        SecondSourceContextualStringsSerialDilution = ["__SERIAL_DILUTION_SOURCE__:" + Context if Context is not None else None for Context in SecondSourceContextualStrings]
        SecondDestinations = SecondTransferDestinations[Index]
        SecondDestinationsContextualStrings = PLATES.LABWARE.GetContextualStringsList(step,SecondDestinations)
        SecondDestinationsContextualStringsSerialDilution = ["__SERIAL_DILUTION_DESTINATION__:" + Context if Context is not None else None for Context in SecondDestinationsContextualStrings]
        SecondVolumes = SecondTransferVolumes[Index]

        for SourceContext, SourceContextSerial, DestinationContext, DestinationContextSerial in zip(FirstSourceContextualStrings,FirstSourceContextualStringsSerialDilution,FirstDestinationsContextualStrings,FirstDestinationsContextualStringsSerialDilution):
            if SourceContext != None:
                PLATES.LABWARE.SetContextualSequences(SourceContextSerial,SourceTransferSequences[Index])
                PLATES.LABWARE.SetContextualFactors(SourceContextSerial,PLATES.LABWARE.GetContextualFactors(SourceContext))
                PLATES.LABWARE.AddContextualFlag(SourceContextSerial,PLATES.LABWARE.GetContextualFlags(SourceContext))

            if DestinationContext != None:
                PLATES.LABWARE.SetContextualSequences(DestinationContextSerial,DestinationTransferSequences[Index])
                PLATES.LABWARE.SetContextualFactors(DestinationContextSerial,PLATES.LABWARE.GetContextualFactors(DestinationContext))
                PLATES.LABWARE.AddContextualFlag(DestinationContextSerial,PLATES.LABWARE.GetContextualFlags(DestinationContext))

        for SourceContext, SourceContextSerial, DestinationContext, DestinationContextSerial in zip(SecondSourceContextualStrings,SecondSourceContextualStringsSerialDilution,SecondDestinationsContextualStrings,SecondDestinationsContextualStringsSerialDilution):
            if SourceContext != None:
                PLATES.LABWARE.SetContextualSequences(SourceContextSerial,SourceTransferSequences[Index])
                PLATES.LABWARE.SetContextualFactors(SourceContextSerial,PLATES.LABWARE.GetContextualFactors(SourceContext))
                PLATES.LABWARE.AddContextualFlag(SourceContextSerial,PLATES.LABWARE.GetContextualFlags(SourceContext))

            if DestinationContext != None:
                PLATES.LABWARE.SetContextualSequences(DestinationContextSerial,DestinationTransferSequences[Index])
                PLATES.LABWARE.SetContextualFactors(DestinationContextSerial,PLATES.LABWARE.GetContextualFactors(DestinationContext))
                PLATES.LABWARE.AddContextualFlag(DestinationContextSerial,PLATES.LABWARE.GetContextualFlags(DestinationContext))

        FirstSequences = PLATES.CreatePipetteSequence(FirstDestinationsContextualStringsSerialDilution, FirstDestinations, FirstSourceContextualStringsSerialDilution, FirstSources, FirstVolumes,SAMPLES.Column(0),SAMPLES.Column(0))

        SecondSequences = PLATES.CreatePipetteSequence(SecondDestinationsContextualStringsSerialDilution, SecondDestinations, SecondSourceContextualStringsSerialDilution, SecondSources, SecondVolumes,SAMPLES.Column(0),SAMPLES.Column(10))

        FirstSeqFlag = False
        if FirstSequences.GetNumSequencePositions() != 0:

            TransferVolumes = FirstSequences.GetTransferVolumes()

            HAMILTONIO.AddCommand(PIPETTE.GetLiquidClassStrings({"TransferVolumes":TransferVolumes,"LiquidCategories":FirstSequences.GetSourceLiquidClassStrings()}),False)
            HAMILTONIO.AddCommand(PIPETTE.GetLiquidClassStrings({"TransferVolumes":TransferVolumes,"LiquidCategories":FirstSequences.GetDestinationLiquidClassStrings()}),False)
            HAMILTONIO.AddCommand(PIPETTE.GetTipSequenceStrings({"TransferVolumes":TransferVolumes}),False)
            FirstSeqFlag = True

        SecondSeqFlag = False
        if SecondSequences.GetNumSequencePositions() != 0:

            TransferVolumes = SecondSequences.GetTransferVolumes()

            HAMILTONIO.AddCommand(PIPETTE.GetLiquidClassStrings({"TransferVolumes":TransferVolumes,"LiquidCategories":SecondSequences.GetSourceLiquidClassStrings()}),False)
            HAMILTONIO.AddCommand(PIPETTE.GetLiquidClassStrings({"TransferVolumes":TransferVolumes,"LiquidCategories":SecondSequences.GetDestinationLiquidClassStrings()}),False)
            HAMILTONIO.AddCommand(PIPETTE.GetTipSequenceStrings({"TransferVolumes":TransferVolumes}),False)
            SecondSeqFlag = True

        Response = HAMILTONIO.SendCommands()

        if Response == False:
            if FirstSeqFlag == True:
                FirstSourceLiquidClassStrings = []
                FirstDestinationLiquidClassStrings = []
                FirstTipSequenceStrings = []

            if SecondSeqFlag == True:
                SecondSourceLiquidClassStrings = []
                SecondDestinationLiquidClassStrings = []
                SecondTipSequenceStrings = []
        else:

            if FirstSeqFlag == True:
                FirstSourceLiquidClassStrings = Response.pop(0)["Response"].split(HAMILTONIO.GetDelimiter())
                FirstDestinationLiquidClassStrings = Response.pop(0)["Response"].split(HAMILTONIO.GetDelimiter())
                FirstTipSequenceStrings = Response.pop(0)["Response"].split(HAMILTONIO.GetDelimiter())

            if SecondSeqFlag == True:
                SecondSourceLiquidClassStrings = Response.pop(0)["Response"].split(HAMILTONIO.GetDelimiter())
                SecondDestinationLiquidClassStrings = Response.pop(0)["Response"].split(HAMILTONIO.GetDelimiter())
                SecondTipSequenceStrings = Response.pop(0)["Response"].split(HAMILTONIO.GetDelimiter())

        if FirstSeqFlag == True:
            TransferArgumentsDict = {\
                "SequenceClass":FirstSequences,\
                "SourceLiquidClasses":FirstSourceLiquidClassStrings,\
                "DestinationLiquidClasses":FirstDestinationLiquidClassStrings,\
                "TipSequences":FirstTipSequenceStrings,\
                "KeepTips":"False",\
                "DestinationPipettingOffset":0}


            HAMILTONIO.AddCommand(PIPETTE.Transfer(TransferArgumentsDict))
            Response = HAMILTONIO.SendCommands()

        if SecondSeqFlag == True:
            TransferArgumentsDict = {\
                "SequenceClass":SecondSequences,\
                "SourceLiquidClasses":SecondSourceLiquidClassStrings,\
                "DestinationLiquidClasses":SecondDestinationLiquidClassStrings,\
                "TipSequences":SecondTipSequenceStrings,\
                "KeepTips":"False",\
                "DestinationPipettingOffset":0}

            HAMILTONIO.AddCommand(PIPETTE.Transfer(TransferArgumentsDict))
            Response = HAMILTONIO.SendCommands()
        
