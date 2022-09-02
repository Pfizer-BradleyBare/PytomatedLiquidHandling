Attribute VB_Name = "GlobalVariables"
Global WordHandle As Object
Global GlobalHelpDocumentHandle As Object

Global GlobalClickLocation As Range
Global GlobalIsNewAction As Boolean

Global OldUnchangedActionName As String

Global GlobalOldActionName As String
Global GlobalOldActionArgs() As String
Global GlobalOldStepIsEnabled As String

Global GlobalNewActionName As String
Global GlobalNewActionArgs() As String
Global GlobalNewActionArgsTitles() As String
Global GlobalNewStepIsEnabled As String

Global GlobalOrganizerActionsValidated As Boolean
Global GlobalOrganizerActionName() As String
Global GlobalOrgnizerActionNumArgs() As Integer
Global GlobalOrganizerActionArgsTitles() As String
Global GlobalOrganizerActionArgs() As String
Global GlobalOrganizerActionComments() As String
Global GlobalOrganizerActionArgsTitlesNotAcceptable() As Boolean
Global GlobalOrganizerActionArgsNotAcceptable() As Boolean
Global GlobalOrganizerActionNotAcceptable() As Boolean
Global GlobalOrganizerActionHorizontalOffset() As Integer
Global GlobalOrganizerActionRowDetected() As Integer
Global GlobalOrganizerActionColDetected() As Integer
Global GlobalOrganizerActionPrintRow() As Integer
Global GlobalOrganizerActionPrintCol() As Integer
Global GlobalOrganizerNumActions As Integer
Global GlobalOrganizerNumSplitSeperators As Integer

Global GlobalBuildingBlockWorkingStatus As Boolean
Global GlobalBuildingBlocksSteps() As String
Global GlobalBuildingBlocksStepHelpBookmarks() As String
Global GlobalBuildingBlocksPathway() As String
Global GlobalBuildingBlocksDisableable() As Boolean
Global GlobalBuildingBlocksColor() As String
Global GlobalBuildingBlocksSupported() As Boolean
Global GlobalBuildingBlocksNumParameters() As Integer
Global GlobalBuildingBlocksParameters() As String
Global GlobalBuildingBlocksParametersInputTypes() As String
Global GlobalBuildingBlocksParametersComboBoxOptions() As String
Global GlobalBuildingBlocksParametersInitialValues() As String
Global GlobalBuildingBlocksParametersIsSolution() As Boolean

Global GlobalSolutionDetectedPlates() As String

Global GlobalSolutionsValidated As Boolean
Global GlobalSolutionName As String
Global GlobalSolutionCategoryString As String
Global GlobalSolutionStorageTemperatureString As String
Global GlobalSolutionVolatilityOptionsString As String
Global GlobalSolutionViscosityOptionsString As String
Global GlobalSolutionHomogeneityOptionsString As String
Global GlobalSolutionLLDOptionsString As String
Global GlobalSolutionPresets() As String
Global GlobalSolutionPresetVolatility() As String
Global GlobalSolutionPresetViscosity() As String
Global GlobalSolutionPresetHomogeneity() As String
Global GlobalSolutionPresetLLD() As String
Global GlobalDetectedSolutionNames() As String
Global GlobalDetectedSolutionsCounter As Integer
Global GlobalStoredSolutionNames() As String
Global GlobalStoredSolutionComments() As String
Global GlobalStoredSolutionParams() As String
Global GlobalStoredSolutionArgsNotAcceptable() As Boolean
Global GlobalStoredSolutionNotAcceptable() As Boolean
