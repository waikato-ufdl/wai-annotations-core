class Annotation:
    """
    The base class for the dependent annotation-type of items in a data-set
    of a particular domain. Should be sub-typed by specific domains
    to represent items in that domain, e.g. labels for classification-based domains.
    Provides no semantics except that annotation-types extend this class.
    """
    pass
