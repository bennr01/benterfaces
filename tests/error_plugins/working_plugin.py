"""A error test plugin."""
from zope.interface import Interface, implementer

from benterfaces._test import ITestPlugin


@implementer(ITestPlugin)
class TxtTestImplementation(object):
    """A working test implementation"""

    def get_id(self):
        """return an id string."""
        return "test_error_working_plugin"
