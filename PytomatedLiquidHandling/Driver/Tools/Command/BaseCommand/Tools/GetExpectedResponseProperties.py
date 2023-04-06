def GetExpectedResponseProperties(ClassInstance: object) -> list[str]:
    """Extracts the response properties, which are decorated in the class definition, from the class

    Args:
        cls (object): Any object that inherits from Command

    Returns:
        list[str]: A list of response properties as strings
    """
    Out = list()

    for Name in dir(ClassInstance):
        if hasattr(getattr(ClassInstance, Name), "Decorated_ExpectedResponseProperty"):
            Out.append(Name.replace("Get", ""))

    return Out
