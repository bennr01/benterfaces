"""decorators for interfaces."""
from zope.interface import implementedBy
from zope.interface.verify import verifyClass


def verify_implementation(cls):
    """
    Verifies the implementation of the Interfaces implemented by cls.
    Raises a zope.interfaces.verify.BrokenImplementation if it does not
    implement all of the Interfaces correctly.
    Returns cls.
    This function should be used as an decorator.
    """
    interfaces = list(implementedBy(cls))
    for i in interfaces:
        verifyClass(i, cls)
    return cls
