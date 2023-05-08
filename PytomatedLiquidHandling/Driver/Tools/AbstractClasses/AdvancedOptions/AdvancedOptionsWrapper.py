def AdvancedOptionsWrapper(Class__init__Function):
    def wrapper(*args, **kwargs):
        if kwargs:
            args[0].UpdateItems = kwargs
        return Class__init__Function(*args, **kwargs)

    return wrapper


# This function captures if keywords were passed during instantiation.
