def GetExpectedResponseProperties(cls) -> list[str]:
    Out = list()

    for Name in dir(cls):
        if hasattr(getattr(cls, Name), "Decorated_ExpectedResponseProperty"):
            Out.append(Name.replace("Get", ""))

    return Out
